import requests
import json
import os

def read_output_file():
    try:
        with open('output.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No output.txt file found."

def chunk_message(message, max_length=3000):
    return [message[i:i+max_length] for i in range(0, len(message), max_length)]

webhook_url = os.environ['SLACK_WEBHOOK_URL']
workflow_name = os.environ['WORKFLOW_NAME']
job_status = os.environ['JOB_STATUS']
event_type = os.environ['EVENT_TYPE']
commit_message = os.environ['COMMIT_MESSAGE']
output_content = read_output_file()

header = f"*Workflow:* {workflow_name}\n*Status:* {job_status}\n*Event:* {event_type}\n*Commit:* {commit_message}"

chunks = chunk_message(output_content)

for i, chunk in enumerate(chunks):
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": header if i == 0 else f"*Output (continued {i+1}/{len(chunks)}):*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"```{chunk}```"
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
        print(f'Message part {i+1}/{len(chunks)} posted successfully')
