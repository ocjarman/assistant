#!/bin/bash

# Exit on error
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if not already installed
if [ ! -f "venv/.requirements_installed" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
    touch venv/.requirements_installed
fi

# Function to handle script termination
cleanup() {
    echo "Stopping sleep monitor..."
    exit 0
}

# Set up trap for clean exit
trap cleanup SIGINT SIGTERM

# Main loop
while true; do
    echo "Starting sleep monitor..."
    python3 sleep.py || {
        echo "Sleep monitor crashed. Restarting in 5 seconds..."
        sleep 5
    }
done 