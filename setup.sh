#!/bin/bash
# Setup script for Recipe Search Application

echo "🍳 Recipe Search Application Setup"
echo "=================================="

# Check Python version
echo "Checking Python version..."
if ! python3 --version >/dev/null 2>&1; then
    echo "❌ Python 3 not found. Please install Python 3.7+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION found"

# Check tkinter
echo "Checking tkinter support..."
if ! python3 -c "import tkinter" >/dev/null 2>&1; then
    echo "❌ tkinter not found."
    echo "Please install tkinter support:"
    echo "  - macOS: brew install python-tk"
    echo "  - Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  - Windows: Reinstall Python with tcl/tk support"
    exit 1
fi
echo "✅ tkinter available"

# Install dependencies
echo "Installing dependencies..."
if pip3 install -r requirements.txt >/dev/null 2>&1; then
    echo "✅ Dependencies installed successfully"
elif pip3 install --break-system-packages -r requirements.txt >/dev/null 2>&1; then
    echo "✅ Dependencies installed with --break-system-packages"
else
    echo "❌ Failed to install dependencies"
    echo "Try: pip3 install --break-system-packages -r requirements.txt"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get a Spoonacular API key from: https://rapidapi.com/spoonacular/api/recipe-food-nutrition"
echo "2. Run the application: python3 src/main.py"
echo "3. Enter your API key in the application"
echo ""
echo "Happy cooking! 👨‍🍳"