import asyncio
import websockets
import json
import re
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        account_infos = re.findall(r'"account":\s*{[^}]+}', content)
        
        if account_infos:
            last_account_info = account_infos[-1]
            
            balance_match = re.search(r'"balance":\s*(\d+)', last_account_info)
            currency_match = re.search(r'"currency":\s*"(\w+)"', last_account_info)
            
            win_matches = re.findall(r'"win":\s*(\d+)', content)
            wager_matches = re.findall(r'"wager":\s*(\d+)', content)
            
            if all([balance_match, currency_match]) and win_matches and wager_matches:
                key_info.append("Bet made successfully")
                key_info.append(f"balance after bet: {balance_match.group(1)}")
                key_info.append(f"win after bet: {win_matches[-1]}")
                key_info.append(f"currency: {currency_match.group(1)}")
                key_info.append(f"wager: {wager_matches[-1]}")
        else:
            key_info.append("No account information found")
    except (IndexError, AttributeError) as e:
        key_info.append(f"Error extracting bet information: {str(e)}")
    
    return '\n'.join(key_info)

async def make_bet(websocket, bet_number):
    output = []

    def log(message):
        logging.info(f"Bet {bet_number}: {message}")
        output.append(f"Bet {bet_number}: {message}")

    try:
        log("Starting bet")
        
        auth_response = await asyncio.wait_for(websocket.recv(), timeout=30)
        log("Received authentication message")
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
        
        first_response = await asyncio.wait_for(websocket.recv(), timeout=30)
        log("Received first response")
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
        
        second_response = await asyncio.wait_for(websocket.recv(), timeout=30)
        log("Received second response")
        log(json.dumps(json.loads(second_response), indent=2))

        log("Bet completed successfully")

    except asyncio.TimeoutError:
        log("Timeout occurred while waiting for a response")
    except Exception as e:
        log(f"An error occurred: {str(e)}")

    return '\n'.join(output)

async def test_websocket(uri):
    try:
        async with websockets.connect(uri) as websocket:
            logging.info(f"Connected to {uri}")
            
            all_output = []
            for i in range(100):
                logging.info(f"Making bet {i+1}")
                bet_output = await make_bet(websocket, i+1)
                all_output.append(bet_output)
                
                await asyncio.sleep(1)

            full_output = '\n\n'.join(all_output)

            with open('output.txt', 'w') as f:
                f.write(full_output)
            logging.info("output.txt created successfully")

            key_info = extract_key_info(full_output)
            with open('key_info.txt', 'w') as f:
                f.write(key_info)
            logging.info("key_info.txt created successfully")

    except (websockets.exceptions.InvalidURI, websockets.exceptions.InvalidHandshake) as e:
        logging.error(f"Connection to {uri} failed: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    websocket_uri = "wss://goddessofwater-be.dev.wicked.games/demo?gameId=9007"
    asyncio.run(test_websocket(websocket_uri))
