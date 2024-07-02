import os
import requests

def send_slack_message():
    webhook_url = os.environ['SLACK_WEBHOOK_URL']
    workflow_name = os.environ['WORKFLOW_NAME']
    job_status = os.environ['JOB_STATUS']
    event_type = os.environ['EVENT_TYPE']
    commit_message = os.environ['COMMIT_MESSAGE']

    # Read the content of output.txt
    try:
        with open('output.txt', 'r') as file:
            output_content = file.read()
    except FileNotFoundError:
        output_content = "output.txt file not found"

    # Read the content of key_info.txt
    try:
        with open('key_info.txt', 'r') as file:
            key_info = file.read()
    except FileNotFoundError:
        key_info = "key_info.txt file not found"

    # Prepare the message
    message = {
        "text": f"Workflow: {workflow_name}\nStatus: {job_status}\nEvent: {event_type}\nCommit: {commit_message}\n\nKey Information:\n{key_info}\n\nFull Output:\n```\n{output_content}\n```"
    }

    # Send the message
    response = requests.post(webhook_url, json=message)
    response.raise_for_status()
    print("Message sent successfully")

if __name__ == "__main__":
    send_slack_message()
