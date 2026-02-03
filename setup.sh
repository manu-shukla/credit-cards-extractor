#!/bin/bash
set -e  # Exit on error

echo "Installing Credit Card Extractor..."
echo "======================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Dependencies installed. Installing Playwright..."

# Install Playwright browsers
playwright install chromium

echo "Playwright installed. Setting up environment variables..."

# Copy .env.example if .env doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ".env file created from .env.example"
    else
        touch .env
        echo ".env file created"
    fi
else
    echo ".env file already exists. Updating..."
fi

# Prompt for API keys
echo ""
echo "Enter your Gemini API Key (press Enter to skip): "
read gemini_api_key

echo "Enter your OpenAI API Key (press Enter to skip): "
read openai_api_key

# Update .env file
if [ ! -z "$gemini_api_key" ]; then
    # Remove existing GEMINI_API_KEY line if present
    sed -i.bak '/^GEMINI_API_KEY=/d' .env && rm .env.bak
    echo "GEMINI_API_KEY=$gemini_api_key" >> .env
fi

if [ ! -z "$openai_api_key" ]; then
    # Remove existing OPENAI_API_KEY line if present
    sed -i.bak '/^OPENAI_API_KEY=/d' .env && rm .env.bak
    echo "OPENAI_API_KEY=$openai_api_key" >> .env
fi

echo ""
echo "======================================="
echo "Setup completed successfully!"
echo "======================================="
echo ""
echo "To activate the virtual environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "Then run the scraper with:"
echo "  python main.py"
echo ""