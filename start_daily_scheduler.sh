#!/bin/bash

# Kijiji Daily Scheduler Launch Script
# This script starts the automated daily posting at 9:00 AM

echo "🚀 Starting Kijiji Daily Scheduler..."
echo "================================================"

# Change to the project directory
cd /Volumes/T7/Kijiji/KijijiBot

# Activate the virtual environment
source venv/bin/activate

# Start the daily scheduler at 9:00 AM
# Change the time if you want a different schedule
python daily_scheduler.py schedule 09:00

# Note: This will run continuously until you press Ctrl+C