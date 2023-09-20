from argparse import ArgumentParser, BooleanOptionalAction
import json
import ssl
import time

from websockets.sync.client import connect


# See response to https://hypothes.is/api/links for WebSocket endpoint.
def run_test(endpoint="wss://h-websocket.hypothes.is/ws", ssl_verify=True):
    print(f"Connecting to {endpoint}...")

    max_attempts = 100
    n_successes = 0
    n_timeouts = 0
    next_msg_id = 0
    timeout = 3

    if not ssl_verify:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    else:
        ssl_context = None  # Use default

    for n_attempt in range(max_attempts):
        next_msg_id += 1
        print(f"Attempt {n_attempt} of {max_attempts}..")
        with connect(endpoint, ssl_context=ssl_context) as websocket:
            # Simple ping-pong test, to verify the connection was established.
            try:
                pong_event = websocket.ping()
                pong_event.wait(timeout=timeout)
            except TimeoutError:
                print("Ping timed out")
                n_timeouts += 1
                continue

            # Send a "whoami" message. On the H websocket this involves the
            websocket.send(json.dumps({"type": "whoami", "id": next_msg_id}))
            try:
                recv_start = time.time()
                message = websocket.recv(timeout=timeout)
                recv_elapsed = time.time() - recv_start
                print(f"Received response {message} in {recv_elapsed:.2f}s")
                n_successes += 1
            except TimeoutError:
                print('"whoami" request timed out')
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
    parser.add_argument(
        "--ssl-verify",
        action=BooleanOptionalAction,
        help="Whether to enable SSL verification",
        default=True,
    )
    args = parser.parse_args()

    run_test(args.endpoint, ssl_verify=args.ssl_verify)


main()
