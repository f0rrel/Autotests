import requests
import json
import os
import re

def read_output_file():
    try:
        with open('output.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No output.txt file found."

def extract_key_info(content):
    key_info = []
    
    # Check for successful authentication
    if "Received authentication message:" in content:
        key_info.append("Authorization successful")
    
    # Check for gameSessionId extraction
    if "Extracted gameSessionId:" in content:
        key_info.append("gameSessionId extracted successfully")
    
    # Extract bet information
    balance_match = re.search(r'"balance": (\d+)', content)
    win_match = re.search(r'"win": (\d+)', content)
    currency_match = re.search(r'"currency": "(\w+)"', content)
    wager_match = re.search(r'"wager": (\d+)', content)
    
    if all([balance_match, win_match, currency_match, wager_match]):
        key_info.append("Bet made successfully")
        key_info.append(f"balance after bet: {balance_match.group(1)}")
        key_info.append(f"win after bet: {win_match.group(1)}")
        key_info.append(f"currency: {currency_match.group(1)}")
        key_info.append(f"wager: {wager_match.group(1)}")
    
    return '\n'.join(key_info)

webhook_url = os.environ['SLACK_WEBHOOK_URL']
workflow_name = os.environ['WORKFLOW_NAME']
job_status = os.environ['JOB_STATUS']
event_type = os.environ['EVENT_TYPE']
commit_message = os.environ['COMMIT_MESSAGE']
output_content = read_output_file()

summary = extract_key_info(output_content)

payload = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Workflow:* {workflow_name}\n*Status:* {job_status}\n*Event:* {event_type}\n*Commit:* {commit_message}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Summary:*\n```{summary}```"
            }
        }
    ]
}

response = requests.post(
    webhook_url,
    data=json.dumps(payload),
    headers={'Content-Type': 'application/json'}
)

if response.status_code != 200:
    print(f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}')
else:
    print('Message posted successfully')
