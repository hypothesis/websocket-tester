# websocket-tester

Tools for testing the Hypothesis [Real Time API](https://h.readthedocs.io/en/latest/api/realtime/).

## Installation

This project uses [Pipenv](https://pipenv.pypa.io). To install dependencies,
run:

```sh
pipenv install
```

## Usage

To run tests, you need to specify the WebSocket endpoint that you want to test
against. The WebSocket endpoint for a particular instance of H can be obtained
from the `/api/links` endpoint:

```sh
$ curl -s https://hypothes.is/api/links | jq .websocket 

"wss://h-websocket.hypothes.is/ws"
```

Run the tool with:

```sh
pipenv run python -m websocket_tester --endpoint <url>
```
