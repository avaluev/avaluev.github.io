#!/bin/bash

# Quick setup script for Autonomous AI Team

set -e  # Exit on error

echo "🤖 Autonomous AI Team - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found Python $python_version"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your ANTHROPIC_API_KEY!"
    echo "   Run: nano .env"
    echo ""
else
    echo "✓ .env file exists"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Check API key
echo ""
echo "🔑 Checking API configuration..."
if grep -q "your_claude_api_key_here" .env 2>/dev/null; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY not configured in .env"
    echo "   You need to add your Claude API key to run the system."
    echo ""
    echo "   Get your API key from: https://console.anthropic.com/"
    echo "   Then edit .env and replace 'your_claude_api_key_here'"
else
    echo "✓ API key appears to be configured"
fi

echo ""
echo "======================================"
echo "✨ Setup complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your API key (if not already done):"
echo "   nano .env"
echo ""
echo "2. Run the example script:"
echo "   source venv/bin/activate"
echo "   python scripts/example_usage.py"
echo ""
echo "3. Or start the API server:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo "   # Then visit http://localhost:8000/docs"
echo ""
echo "4. Or use Docker:"
echo "   cd docker"
echo "   docker-compose up"
echo ""
echo "📖 See README.md for full documentation"
echo ""
