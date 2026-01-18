#!/bin/bash
# CodePulse Quick Launcher for Linux/Mac
# Just run: ./run.sh

# Check Python
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERROR] Python 3 not found!"
    echo "Please run ./setup.sh first"
    echo ""
    exit 1
fi

# Run CodePulse
python3 codepulse.py
