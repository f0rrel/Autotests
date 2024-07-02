import requests
import json
import os

def read_output_file():
    try:
        with open('output.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No output.txt file found."

def extract_key_info(content):
    lines = content.split('\n')
    key_info = []
    for line in lines:
        if any(keyword in line for keyword in ['Connected to', 'Sent:', 'Extracted gameSessionId:', 'isWin:', 'win:', 'wager:', 'balance:']):
            key_info.append(line.strip())
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
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "For full details, please check the workflow run in GitHub Actions."
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
