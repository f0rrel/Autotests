import asyncio
import websockets
import json
from pprint import pprint

async def test_websocket(uri):
    output = []  # Initialize an empty list to store output lines
    try:
        async with websockets.connect(uri) as websocket:
            output.append(f"Connected to {uri}")

            # Receive the initial authentication message
            auth_response = await websocket.recv()
            output.append("Received authentication message:")
            output.append(pprint.pformat(json.loads(auth_response)))

            # First message to send
            first_message = {
                "path": "init",
                "input": {
                    "gameInput": {
                        "actionType": "play",
                        "actionInput": {}
                    },
                    "gameSessionId": "67bfe6c0-2345-11ef-8338-59bd33860811"
                }
            }

            # Convert the first message to a JSON string
            first_message_json = json.dumps(first_message)

            # Send the first message
            await websocket.send(first_message_json)
            output.append(f"Sent: {first_message_json}")

            # Receive the first response
            first_response = await websocket.recv()
            output.append("Received:")
            output.append(pprint.pformat(json.loads(first_response)))

            # Parse the first response and extract the gameSessionId
            first_response_data = json.loads(first_response)
            game_session_id = first_response_data.get("input", {}).get("game", {}).get("gameSessionId")

            if not game_session_id:
                raise ValueError("gameSessionId not found in the response")

            output.append(f"Extracted gameSessionId: {game_session_id}")

            # Second message to send
            second_message = {
                "path": "action",
                "input": {
                    "gameInput": {
                        "actionType": "play",
                        "actionInput": {}
                    },
                    "gameSessionId": game_session_id
                }
            }

            # Convert the second message to a JSON string
            second_message_json = json.dumps(second_message)

            # Send the second message
            await websocket.send(second_message_json)
            output.append(f"Sent: {second_message_json}")

            # Receive the second response
            second_response = await websocket.recv()
            output.append("Received:")
            output.append(pprint.pformat(json.loads(second_response)))

    except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake) as e:
        output.append(f"Connection to {uri} failed: {e}")
    except Exception as e:
        output.append(f"An error occurred: {e}")

    # Write all output to a file
    with open('output.txt', 'w') as f:
        f.write('\n'.join(output))

# Configuration
websocket_uri = "wss://goddessofwater-be.dev.wicked.games/demo?gameId=9007"

# Run the test
asyncio.run(test_websocket(websocket_uri))
