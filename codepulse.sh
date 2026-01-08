#!/bin/bash
# ============================================
# CodePulse - Professional Code Scanner
# ============================================
#
# Quick Usage:
#   ./codepulse.sh <path>              - Quick HTML scan
#   ./codepulse.sh <path> json         - JSON output
#   ./codepulse.sh <path> html         - HTML output
#   ./codepulse.sh <path> fast         - Fast (8 workers)
#   ./codepulse.sh <path> full         - Full scan (no cache)
#

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================"
echo "  CodePulse Fast Scanner v0.10.0"
echo "========================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 not found!"
    echo
    echo "Please install Python 3.9+ from your package manager"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}[ERROR]${NC} Python $REQUIRED_VERSION or higher required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check if project path provided
if [ $# -eq 0 ]; then
    echo -e "${RED}[ERROR]${NC} No project path specified!"
    echo
    echo "Usage:"
    echo "  ./codepulse.sh <project_path> [mode]"
    echo
    echo "Examples:"
    echo "  ./codepulse.sh /home/user/project"
    echo "  ./codepulse.sh ./src html"
    echo "  ./codepulse.sh /var/www fast"
    echo "  ./codepulse.sh ./project full"
    echo
    echo "Modes:"
    echo "  html  - HTML report (default)"
    echo "  json  - JSON report"
    echo "  fast  - Fast scan (8 workers)"
    echo "  full  - Full scan (no cache/incremental)"
    echo
    exit 1
fi

# Set project path
PROJECT_PATH="$1"

# Check if project exists
if [ ! -e "$PROJECT_PATH" ]; then
    echo -e "${RED}[ERROR]${NC} Project path not found: $PROJECT_PATH"
    echo
    exit 1
fi

echo -e "${BLUE}[*]${NC} Project: $PROJECT_PATH"

# Parse mode (2nd argument)
MODE="${2:-html}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build command
CMD="python3 \"$SCRIPT_DIR/fast_scan.py\" \"$PROJECT_PATH\""

# Apply mode
case "$MODE" in
    html)
        CMD="$CMD --format html"
        echo -e "${BLUE}[*]${NC} Format:  HTML Report"
        ;;
    json)
        CMD="$CMD --format json"
        echo -e "${BLUE}[*]${NC} Format:  JSON Report"
        ;;
    fast)
        CMD="$CMD --format html --workers 8"
        echo -e "${BLUE}[*]${NC} Format:  HTML Report"
        echo -e "${BLUE}[*]${NC} Mode:    Fast (8 workers)"
        ;;
    full)
        CMD="$CMD --format html --no-cache --no-incremental"
        echo -e "${BLUE}[*]${NC} Format:  HTML Report"
        echo -e "${BLUE}[*]${NC} Mode:    Full Scan"
        ;;
    *)
        # Treat as custom argument
        CMD="$CMD $MODE"
        echo -e "${BLUE}[*]${NC} Custom:  $MODE"
        ;;
esac

# Add additional arguments
shift 2
while [ $# -gt 0 ]; do
    CMD="$CMD \"$1\""
    shift
done

echo -e "${BLUE}[*]${NC} Cache:   Enabled"
echo
echo "========================================"
echo "  Starting Scan..."
echo "========================================"
echo

# Run scan
eval $CMD
EXIT_CODE=$?

# Check result
if [ $EXIT_CODE -ne 0 ]; then
    echo
    echo "========================================"
    echo -e "  ${RED}Scan Failed!${NC}"
    echo "========================================"
    echo
    echo "Check errors above and try again."
    echo
    exit $EXIT_CODE
fi

echo
echo "========================================"
echo -e "  ${GREEN}Scan Complete!${NC}"
echo "========================================"
echo

# Auto-open HTML if generated
if [[ "$MODE" == "html" ]] || [[ "$MODE" == "fast" ]] || [[ "$MODE" == "full" ]]; then
    echo -e "${BLUE}[*]${NC} Opening HTML report..."
    echo
    
    # Find most recent HTML file
    LATEST_HTML=$(ls -t "$SCRIPT_DIR/reports/"*.html 2>/dev/null | head -n1)
    
    if [ -n "$LATEST_HTML" ]; then
        # Detect OS and open
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            open "$LATEST_HTML"
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v xdg-open &> /dev/null; then
                xdg-open "$LATEST_HTML"
            elif command -v gnome-open &> /dev/null; then
                gnome-open "$LATEST_HTML"
            else
                echo -e "${YELLOW}[!]${NC} Please open manually: $LATEST_HTML"
            fi
        fi
    fi
fi

exit 0
