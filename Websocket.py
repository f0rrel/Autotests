import asyncio
import websockets
import json
from pprint import pprint

async def test_websocket(uri):
    try:
        async with websockets.connect(uri) as websocket:
            with open('output.txt', 'w') as f:
                def log(message):
                    print(message)
                    f.write(message + '\n')
                    f.flush()  # Ensure the content is written immediately

                log(f"Connected to {uri}")
                
                auth_response = await websocket.recv()
                log("Received authentication message:")
                log(json.dumps(json.loads(auth_response), indent=2))

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
                
                first_message_json = json.dumps(first_message)
                await websocket.send(first_message_json)
                log(f"Sent: {first_message_json}")

                first_response = await websocket.recv()
                log("Received:")
                log(json.dumps(json.loads(first_response), indent=2))

                first_response_data = json.loads(first_response)
                game_session_id = first_response_data.get("input", {}).get("game", {}).get("gameSessionId")
                if not game_session_id:
                    raise ValueError("gameSessionId not found in the response")
                log(f"Extracted gameSessionId: {game_session_id}")

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
                
                second_message_json = json.dumps(second_message)
                await websocket.send(second_message_json)
                log(f"Sent: {second_message_json}")

                second_response = await websocket.recv()
                log("Received:")
                log(json.dumps(json.loads(second_response), indent=2))

    except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake) as e:
        log(f"Connection to {uri} failed: {e}")
    except Exception as e:
        log(f"An error occurred: {e}")

websocket_uri = "wss://goddessofwater-be.dev.wicked.games/demo?gameId=9007"
asyncio.run(test_websocket(websocket_uri))
