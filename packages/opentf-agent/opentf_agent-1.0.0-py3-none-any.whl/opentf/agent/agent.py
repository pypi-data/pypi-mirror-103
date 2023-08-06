# Copyright 2021 Henix, henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""OpenTestFactory Agent"""

import argparse
import logging
from time import sleep
import subprocess
import sys
import os

import requests


REGISTRATION = {
    "apiVersion": "opentestfactory.org/v1alpha1",
    "kind": "AgentRegistration",
    "metadata": {"name": "test agent"},
    "spec": {
        "tags": [],
        "encoding": "utf-8",
        "script_path": "",
    },
}

DEFAULT_POLLING_DELAY = 5
DEFAULT_PORT = 24368
DEFAULT_RETRY = 5

REGISTRATION_URL_TEMPLATE = "{server}/agents"
ENDPOINT_TEMPLATE = "{server}/agents/{agent_id}"
FILE_URL_TEMPLATE = "{server}/agents/{agent_id}/files/{file_id}"

STATUS_REGISTRATION_FAILED = 2
STATUS_KEYBOARD_INTERRUPT = 0
STATUS_EXCEPTION = 1

########################################################################
# Helpers


def download_file(url, local_filename, headers):
    """Download file to local_filename."""
    response = requests.get(url, stream=True, headers=headers)
    with open(
        os.path.join(REGISTRATION["spec"]["script_path"], local_filename), "wb"
    ) as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)


def post(endpoint, json, headers, retry, delay):
    """Query endpoint, retrying if connection failed.

    If `retry` is `0`, retry forever.
    """
    count = retry
    while True:
        try:
            return requests.post(endpoint, json=json, headers=headers)
        except Exception:
            if count <= 0 and retry != 0:
                break
        logging.info("Could not reach %s, retrying.", endpoint)
        count -= 1
        sleep(delay)

    raise Exception(f"Could not reach {endpoint}, aborting.")


########################################################################
# Handlers


def register_and_handle(args, headers):
    """Register to host and process commands.

    Returns 0 if interrupted by keyboard interrupt, 2 if registration
    failed and 1 if something else occurred.
    """
    stripped_prefix = args.path_prefix.strip("/")
    server = f"{args.host}:{args.port}/{stripped_prefix}".strip("/")
    registration_url = REGISTRATION_URL_TEMPLATE.format(server=server)
    logging.info("Registering agent on %s.", registration_url)
    try:
        response = post(
            registration_url,
            json=REGISTRATION,
            headers=headers,
            retry=args.retry,
            delay=args.polling_delay,
        )
    except Exception as err:
        logging.error("Failed to register to server: %s", err)
        return STATUS_REGISTRATION_FAILED
    try:
        REGISTRATION["spec"]["workspace_dir"] = (
            args.workspace_dir.rstrip(os.sep) + os.sep
        )
        uuid = response.json()["details"]["uuid"]
        logging.info("Agent ready, will poll every %d seconds.", args.polling_delay)
    except Exception as err:
        logging.error("Unexpected server response: %s.", response.text)
        return STATUS_REGISTRATION_FAILED

    endpoint = ENDPOINT_TEMPLATE.format(server=server, agent_id=uuid)
    try:
        while True:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 204:
                sleep(args.polling_delay)
                continue

            try:
                body = response.json()
            except Exception as err:
                logging.error("Command is not JSON: %s.", err)
                continue

            if "details" not in body:
                logging.error("Invalid command, .details not found.")
                continue
            kind = body["details"].get("kind")
            if kind not in KINDS_HANDLERS:
                logging.error("Unexpected command kind %s, ignoring.", kind)
                continue

            KINDS_HANDLERS[kind](uuid, body["details"], server, headers)
    except Exception as err:
        logging.error("An exception occurred: %s.", err)
        return STATUS_EXCEPTION
    except KeyboardInterrupt:
        logging.info("^C")
        return STATUS_KEYBOARD_INTERRUPT
    finally:
        try:
            requests.delete(endpoint, headers=headers)
            logging.info("Agent successfully deregistered.")
        except Exception as err:
            logging.error("Could not deregister agent: %s.", err)


def process_exec(agent_id, command, server, headers):
    """Process exec command."""
    try:
        instruction = command["command"]
        logging.debug("Will run %s", instruction)
        process = subprocess.run(
            command["command"],
            cwd=REGISTRATION["spec"]["workspace_dir"],
            shell=True,
            capture_output=True,
            check=False,
        )
        result = requests.post(
            ENDPOINT_TEMPLATE.format(agent_id=agent_id, server=server),
            json={
                "stdout": str(
                    process.stdout,
                    encoding=REGISTRATION["spec"]["encoding"],
                    errors="backslashreplace",
                ).splitlines(),
                "stderr": str(
                    process.stderr,
                    encoding=REGISTRATION["spec"]["encoding"],
                    errors="backslashreplace",
                ).splitlines(),
                "exit_status": process.returncode,
            },
            headers=headers,
        )
        if result.status_code != 200:
            logging.error("Failed to push command result: %d.", result.status_code)
    except Exception as err:
        logging.error("Failed to run command: %s.", err)


def process_put(agent_id, command, server, headers):
    """Process put command."""
    if "path" not in command:
        logging.error("No path specified in command.")
    if "file_id" not in command:
        logging.error("No file_id specified in command.")
    try:
        download_file(
            FILE_URL_TEMPLATE.format(
                agent_id=agent_id, file_id=command["file_id"], server=server
            ),
            command["path"],
            headers,
        )
        logging.debug("File successfully downloaded to %s", command["path"])
    except Exception as err:
        logging.error("An error occurred while downloading file: %s.", err)


def process_get(agent_id, command, server, headers):
    """Process get command."""
    if "path" not in command:
        logging.error("No path specified in command.")
        return
    if "file_id" not in command:
        logging.error("No file_id specified in command.")
        return

    try:
        with open(command["path"], "rb") as file:
            requests.post(
                FILE_URL_TEMPLATE.format(
                    agent_id=agent_id, file_id=command["file_id"], server=server
                ),
                data=file,
                headers=headers,
            )
    except OSError as err:
        file_path = command["path"]
        result = requests.post(
            ENDPOINT_TEMPLATE.format(agent_id=agent_id, server=server),
            json={
                "stdout": "",
                "stderr": str(f"Failed to fetch file {file_path}. {err}").splitlines(),
                "exit_status": 2,
            },
            headers=headers,
        )
        if result.status_code != 200:
            logging.error("Failed to push command result: %d.", result.status_code)


KINDS_HANDLERS = {"exec": process_exec, "put": process_put, "get": process_get}


########################################################################
# Main


def main():
    """Start agent."""
    parser = argparse.ArgumentParser(description="OpenTestFactory Agent")
    parser.add_argument(
        "--tags",
        help="a comma-separated list of tags (e.g., windows,robotframework)",
        required=True,
    )
    parser.add_argument(
        "--host",
        help="target host with protocol (e.g., https://example.local)",
        required=True,
    )
    parser.add_argument(
        "--port",
        help=f"target port (default to {DEFAULT_PORT})",
        default=DEFAULT_PORT,
        type=int,
    )
    parser.add_argument(
        "--path_prefix",
        help="target context path (default to no context path)",
        default="",
    )
    parser.add_argument("--token", help="token")
    parser.add_argument(
        "--encoding",
        help="encoding on the console side (defaults to utf-8)",
        default="utf-8",
    )
    parser.add_argument(
        "--script_path",
        help="where to put temporary files (defaults to current directory)",
        default=os.getcwd(),
    )
    parser.add_argument(
        "--workspace_dir",
        help="where to put workspaces (defaults to current directory)",
        default=".",
    )
    parser.add_argument(
        "--name",
        help='agent name (defaults to "test agent")',
    )
    parser.add_argument(
        "--polling_delay",
        help=f"polling delay in seconds (default to {DEFAULT_POLLING_DELAY})",
        default=DEFAULT_POLLING_DELAY,
        type=int,
    )
    parser.add_argument(
        "--liveness_probe",
        help="liveness probe in seconds (default to 300 seconds)",
        type=int,
    )
    parser.add_argument(
        "--retry",
        help=f"how many times to try joining host (default to {DEFAULT_RETRY}, 0 = try forever)",
        default=DEFAULT_RETRY,
        type=int,
    )
    parser.add_argument(
        "--debug", help="whether to log debug information.", action="store_true"
    )

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    if args.tags:
        REGISTRATION["spec"]["tags"] = args.tags.split(",")
    if args.encoding:
        REGISTRATION["spec"]["encoding"] = args.encoding
    if args.script_path:
        REGISTRATION["spec"]["script_path"] = args.script_path.rstrip(os.sep)
    if args.name:
        REGISTRATION["metadata"]["name"] = args.name
    if args.liveness_probe:
        REGISTRATION["spec"]["liveness_probe"] = args.liveness_probe
    if args.token:
        headers = {"Authorization": f"Bearer {args.token}"}
    else:
        headers = None

    while True:
        status = register_and_handle(args, headers)
        if status in (STATUS_KEYBOARD_INTERRUPT, STATUS_REGISTRATION_FAILED):
            sys.exit(status)


if __name__ == "__main__":
    main()
