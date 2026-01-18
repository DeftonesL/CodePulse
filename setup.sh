#!/bin/bash

# CodePulse Setup Script for Linux/Mac
# Auto-installs dependencies and sets up the environment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "========================================"
echo "  CodePulse Setup - Linux/Mac"
echo "========================================"
echo ""

# Check Python
echo -e "${BLUE}[1/4] Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 not found!${NC}"
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi

PYVER=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[OK] Python $PYVER detected${NC}"
echo ""

# Check pip
echo -e "${BLUE}[2/4] Checking pip...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}[WARNING] pip not found, installing...${NC}"
    python3 -m ensurepip --default-pip
fi
echo -e "${GREEN}[OK] pip is ready${NC}"
echo ""

# Upgrade pip
echo -e "${BLUE}[3/4] Upgrading pip...${NC}"
python3 -m pip install --upgrade pip --quiet
echo -e "${GREEN}[OK] pip upgraded${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}[4/4] Installing CodePulse dependencies...${NC}"
echo "This may take a minute..."
echo ""

python3 -m pip install --quiet \
    click>=8.0.0 \
    rich>=13.0.0 \
    networkx>=3.0 \
    jinja2>=3.1.0 \
    pytest>=8.0.0

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK] All dependencies installed!${NC}"
else
    echo -e "${RED}[ERROR] Failed to install dependencies!${NC}"
    exit 1
fi
echo ""

# Create reports directory
mkdir -p reports

# Make codepulse.py executable
chmod +x codepulse.py 2>/dev/null || true

# Optional AI setup
echo ""
echo "========================================"
echo "  Optional: AI Features"
echo "========================================"
echo ""
echo "Would you like to install AI features?"
echo "(Requires Anthropic API key)"
echo ""
read -p "Install AI dependencies? (y/n): " INSTALL_AI

if [ "$INSTALL_AI" = "y" ] || [ "$INSTALL_AI" = "Y" ]; then
    echo ""
    echo "Installing AI dependencies..."
    python3 -m pip install --quiet anthropic>=0.40.0
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[OK] AI dependencies installed!${NC}"
        echo ""
        echo "To use AI features, set your API key:"
        echo "  export ANTHROPIC_API_KEY=your-key-here"
        echo ""
        echo "Or create a .env file with:"
        echo "  ANTHROPIC_API_KEY=your-key-here"
    else
        echo -e "${YELLOW}[WARNING] Failed to install AI dependencies${NC}"
    fi
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo -e "${GREEN}CodePulse is ready to use!${NC}"
echo ""
echo "Quick Start:"
echo "  ./codepulse.py       - Interactive mode"
echo "  python3 codepulse.py - Alternative way"
echo ""
echo "Example scans:"
echo "  ./codepulse.py       - Start interactive CLI"
echo ""
