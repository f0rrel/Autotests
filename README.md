# RGS Automated Bet Tests

Automated test suite for RGS (Remote Gaming Server) that simulates 
betting sessions via WebSocket connections, runs on a daily schedule, 
and reports results directly to a Slack channel.

## What it does

- Connects to RGS via WebSocket protocol
- Simulates a predefined number of bets (10 or 100) per run
- Saves results to `output.txt`
- Sends a status report to Slack after every run (success or failure)
- Runs automatically every day at midnight UTC via GitHub Actions

## Workflows

| Workflow | Bets | Environment | Schedule |
|---|---|---|---|
| Making 100 Bets (STG) | 100 | Staging | Daily 00:00 UTC |
| Making 10 Bets (QA) | 10 | QA | Daily 00:00 UTC |

Each workflow can also be triggered manually via `workflow_dispatch`.

## Tech stack

- Python 3.x
- websockets
- GitHub Actions (CI/CD + scheduling)
- Slack Incoming Webhooks

## Setup

### 1. Clone the repo
git clone https://github.com/f0rrel/Autotests.git
cd Autotests

### 2. Install dependencies
pip install websockets

### 3. Run locally
python Websocket_10Bets.py
python Websocket_100Bets.py

## GitHub Actions secrets required

| Secret | Description |
|---|---|
| SLACK_WEBHOOK | Incoming webhook URL for Slack notifications |

## Output

Each run generates `output.txt` with bet results, 
uploaded as a GitHub Actions artifact and summarised in Slack.

## Purpose

These scripts were written to automate repetitive regression checks 
on RGS integrations — verifying that bet requests and responses 
conform to expected behaviour across environments.
