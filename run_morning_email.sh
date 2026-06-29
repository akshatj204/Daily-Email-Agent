#!/bin/bash
# Morning Email Agent - Scheduled Runner
# This script runs the morning email agent and sends the email

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the main script
python main.py

# Deactivate virtual environment
deactivate
