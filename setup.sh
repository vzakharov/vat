#!/bin/bash

# Setup script for VSCode Agent Toolbox

# Create required directories
mkdir -p output

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install required packages
echo "Installing required Python packages..."
pip install requests python-dotenv beautifulsoup4 inflect

# # Make sure scripts are executable
chmod +x tools/*.py 2> /dev/null
chmod +x tools/*.sh 2> /dev/null

# Check for .env file and create if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file and add your API keys."
fi

echo "Setup complete! You can now use the VSCode Agent Toolbox."
