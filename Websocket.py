import asyncio
import websockets
import json
import re

def extract_key_info(content):
    key_info = []
    
    # Check for successful authentication
    if "Received authentication message:" in content:
        key_info.append("Authorization successful")
    
    # Check for gameSessionId extraction
    if "Extracted gameSessionId:" in content:
        key_info.append("gameSessionId extracted successfully")
    
    # Extract bet information
    try:
        # Find all occurrences of account information
        account_infos = re.findall(r'"account":\s*{[^}]+}', content)
        
        if account_infos:
            # Use the last account info
            last_account_info = account_infos[-1]
            
            # Extract balance, currency, and playerId from the last account info
            balance_match = re.search(r'"balance":\s*(\d+)', last_account_info)
            currency_match = re.search(r'"currency":\s*"(\w+)"', last_account_info)
            
            # Extract win and wager from the last game info
            win_matches = re.findall(r'"win":\s*(\d+)', content)
            wager_matches = re.findall(r'"wager":\s*(\d+)', content)
            
            if all([balance_match, currency_match]) and win_matches and wager_matches:
                key_info.append("Bet made successfully")
                key_info.append(f"balance after bet: {balance_match.group(1)}")
                key_info.append(f"win after bet: {win_matches[-1]}")  # Use the last win value
                key_info.append(f"currency: {currency_match.group(1)}")
                key_info.append(f"wager: {wager_matches[-1]}")  # Use the last wager value
        else:
            key_info.append("No account information found")
    except (IndexError, AttributeError) as e:
        key_info.append(f"Error extracting bet information: {str(e)}")
    
    return '\n'.join(key_info)

async def test_websocket(uri):
    output = []  # Define output list here
    try:
        async with websockets.connect(uri) as websocket:
            def log(message):
                print(message)
                output.append(message)

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

    # Write full output to output.txt
    with open('output.txt', 'w') as f:
        f.write('\n'.join(output))

    # Extract key info and write to key_info.txt
    key_info = extract_key_info('\n'.join(output))
    with open('key_info.txt', 'w') as f:
        f.write(key_info)

if __name__ == "__main__":
    websocket_uri = "wss://goddessofwater-be.dev.wicked.games/demo?gameId=9007"
    asyncio.run(test_websocket(websocket_uri))
