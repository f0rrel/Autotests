import os
import requests
import json

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
    except Exception as e:
        output_content = f"Error reading output.txt: {str(e)}"

    # Prepare the message
    message = {
        "text": f"Workflow: {workflow_name}\nStatus: {job_status}\nEvent: {event_type}\nCommit: {commit_message}\n\nOutput:\n```\n{output_content}\n```"
    }

    # Send the message
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        print("Message sent successfully")
        print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {str(e)}")

    # Write debug information to a file
    debug_info = f"""
    Webhook URL: {webhook_url}
    Workflow Name: {workflow_name}
    Job Status: {job_status}
    Event Type: {event_type}
    Commit Message: {commit_message}
    Output Content: {output_content}
    """
    with open('debug_info.txt', 'w') as debug_file:
        debug_file.write(debug_info)

if __name__ == "__main__":
    send_slack_message()
