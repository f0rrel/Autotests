import requests
import json
import os

def read_output_file():
    try:
        with open('output.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "No output.txt file found."

webhook_url = os.environ['SLACK_WEBHOOK_URL']
workflow_name = os.environ['WORKFLOW_NAME']
job_status = os.environ['JOB_STATUS']
event_type = os.environ['EVENT_TYPE']
commit_message = os.environ['COMMIT_MESSAGE']
output_content = read_output_file()

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
                "text": f"*Output:*\n```{output_content}```"
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
    raise ValueError(f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}')
else:
    print('Message posted successfully')
