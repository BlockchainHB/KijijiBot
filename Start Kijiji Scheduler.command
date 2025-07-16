#!/bin/bash

# Kijiji Daily Scheduler - Double Click to Launch
# This will open Terminal and start the daily scheduler

clear
echo "🤖 KIJIJI DAILY AUTOMATION SCHEDULER"
echo "===================================="
echo ""
echo "This will post your 2 room rental ads"
echo "every day at 9:00 AM automatically."
echo ""
echo "Press Ctrl+C to stop at any time."
echo ""
echo "===================================="
echo ""

# Change to the script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start the scheduler
python daily_scheduler.py schedule 09:00