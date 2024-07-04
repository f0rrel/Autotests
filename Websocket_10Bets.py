name: Making 100 Bets (STG)
on:
  schedule:
    - cron: '0 0 * * *'  # This runs daily at midnight UTC
  workflow_dispatch:  # This allows manual triggering

jobs:
  run_script:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install websockets requests
      continue-on-error: true

    - name: Run script
      run: python Websocket_10Bets.py
      timeout-minutes: 30

    - name: Display Python script logs
      run: cat output.txt
      if: always()

    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: script-output
        path: |
          output.txt
          key_info.txt
      if: always()

    - name: Check for script output
      run: |
        if [ ! -f output.txt ]; then
          echo "output.txt was not created."
          exit 1
        fi
        if [ ! -f key_info.txt ]; then
          echo "key_info.txt was not created."
          exit 1
        fi
      if: always()

    - name: Send Slack message
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
        WORKFLOW_NAME: ${{ github.workflow }}
        JOB_STATUS: ${{ job.status }}
        EVENT_TYPE: ${{ github.event_name == 'workflow_dispatch' && 'Manually triggered' || 'Scheduled run' }}
        COMMIT_MESSAGE: ${{ github.event.head_commit.message }}
      run: python send_slack_message.py
      continue-on-error: true
