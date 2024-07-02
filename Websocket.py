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
    # ... (keep your existing WebSocket code here)
    
    # After the WebSocket communication is complete:
    key_info = extract_key_info('\n'.join(output))
    with open('key_info.txt', 'w') as f:
        f.write(key_info)

if __name__ == "__main__":
    websocket_uri = "wss://goddessofwater-be.dev.wicked.games/demo?gameId=9007"
    asyncio.run(test_websocket(websocket_uri))
