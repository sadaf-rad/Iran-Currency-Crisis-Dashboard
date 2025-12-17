#!/bin/bash

# Daily Auto-Update Script for Currency Crisis Dashboard
# This script runs the data update and can be scheduled with cron

echo "🚀 Starting Currency Crisis Dashboard Auto-Update"
echo "Time: $(date)"

# Navigate to project directory
cd /Users/sadaf/Desktop/da/first

# Activate virtual environment
source venv/bin/activate

# Run update script
python3 auto_update.py

# Log completion
echo "✅ Update completed at $(date)"
echo "----------------------------------------"

# Optional: Restart Streamlit (if running as a service)
# pkill -f "streamlit run app.py"
# nohup streamlit run app.py > streamlit.log 2>&1 &
