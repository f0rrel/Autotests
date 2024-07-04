import asyncio
import websockets
import json
from pprint import pprint

async def test_websocket(uri):
    output = []  # This will store all our output
    try:
        async with websockets.connect(uri) as websocket:
            # Receive the initial authentication message
            auth_response = await websocket.recv()
            output.append(f"Auth response received: {auth_response}")

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
            # Receive the first response
            first_response = await websocket.recv()
            # Parse the first response and extract the gameSessionId
            first_response_data = json.loads(first_response)
            game_session_id = first_response_data.get("input", {}).get("game", {}).get("gameSessionId")
            if not game_session_id:
                raise ValueError("gameSessionId not found in the response")
            
            output.append(f"Game session ID: {game_session_id}")

            # Send the "action" message 100 times
            for i in range(100):
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
                # Receive the second response
                second_response = await websocket.recv()
                response_data = json.loads(second_response)
                # Extract only specified fields
                extracted_data = {key: response_data.get("input", {}).get("game", {}).get(key)
                                  for key in ["wager", "win", "winDescription"]}
                # Add any other outcomes (e.g., errors) to the extracted data
                for key, value in response_data.items():
                    if key not in ["input", "output"]:
                        extracted_data[key] = value
                    elif key == "input":
                        for subkey, subvalue in value.items():
                            if subkey not in ["game"]:
                                extracted_data[subkey] = subvalue
                output.append(f"Received response {i + 1}:")
                output.append(json.dumps(extracted_data, indent=2))
    except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake) as e:
        output.append(f"Connection to {uri} failed: {e}")
    except Exception as e:
        output.append(f"An error occurred: {e}")
    
    # Write all output to a file
    with open('output.txt', 'w') as f:
        f.write('\n'.join(output))

# Configuration
websocket_uri = "wss://goddessofwater-be.staging.wicked.games/rgs?token=InRva2VuPTMwZWNkOTdlLTgwYzQtNGY1ZS1iOWJhLTAxZGI0OTFmZjUyZSZjb3VudHJ5PU1FJmN1cnJlbmN5PUVVUiZ0ZXN0cGxheWVyPTAmcGxheWVyaWQ9YmFkOWU2ODYtMjEwOC00MDg0LTg0YjYtNDkwYzk1YmRkZTcxJmxhbmd1YWdlPUVOJmhvbWV1cmw9aHR0cHM6Ly93aWNrZWQuZ2FtZXMmdXJsPWh0dHBzOi8vd2FsbGV0LnN0YWdpbmcud2lja2VkLmdhbWVzL3Rlc3QmYXBpa2V5PWFwaV9rZXkmc2l0ZWlkPXdpY2tlZGdhbWVzIg==&?gameId=9007"

# Run the test
asyncio.run(test_websocket(websocket_uri))
