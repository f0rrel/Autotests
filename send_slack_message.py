import re
import json

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
        # Find the last occurrence of the account information
        last_account_info = re.findall(r'"account":\s*{[^}]+}', content)[-1]
        
        # Extract balance, currency, and playerId from the last account info
        balance_match = re.search(r'"balance":\s*\d+.*?"balance":\s*(\d+)', last_account_info)
        currency_match = re.search(r'"currency":\s*"(\w+)"', last_account_info)
        
        # Extract win and wager from the last game info
        win_match = re.search(r'"win":\s*(\d+)', content)
        wager_match = re.search(r'"wager":\s*(\d+)', content)
        
        if all([balance_match, win_match, currency_match, wager_match]):
            key_info.append("Bet made successfully")
            key_info.append(f"balance after bet: {balance_match.group(1)}")
            key_info.append(f"win after bet: {win_match.group(1)}")
            key_info.append(f"currency: {currency_match.group(1)}")
            key_info.append(f"wager: {wager_match.group(1)}")
    except (IndexError, AttributeError) as e:
        key_info.append(f"Error extracting bet information: {str(e)}")
    
    return '\n'.join(key_info)
