from argparse import ArgumentParser
import json
import time

from websockets.sync.client import connect


# See response to https://hypothes.is/api/links for WebSocket endpoint.
def run_test(endpoint="wss://h-websocket.hypothes.is/ws"):
    print(f"Connecting to {endpoint}...")

    max_attempts = 100
    n_successes = 0
    n_timeouts = 0
    next_msg_id = 0

    for n_attempt in range(max_attempts):
        next_msg_id += 1
        print(f"Attempt {n_attempt} of {max_attempts}..")
        with connect(endpoint) as websocket:
            websocket.send(json.dumps({"type": "whoami", "id": next_msg_id}))
            try:
                message = websocket.recv(timeout=3)
                print(f"Received response {message}")
                n_successes += 1
            except TimeoutError:
                print("Timed out")
                n_timeouts += 1

    print(
        f"{max_attempts} attempts. {n_successes} connections OK {n_timeouts} timed out"
    )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--endpoint",
        type=str,
        help="H WebSocket endpoint",
        default="wss://h-websocket.hypothes.is/ws",
    )
    args = parser.parse_args()

    run_test(args.endpoint)


main()
