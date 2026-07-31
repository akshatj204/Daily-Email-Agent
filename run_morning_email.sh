#!/bin/bash
# Morning Email Agent - Scheduled Runner
# This script runs the morning email agent and sends the email

set -euo pipefail

# Change to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Use a virtual environment if present, otherwise fall back to the system Python.
if [ -x "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
else
    echo "No Python interpreter found" >&2
    exit 1
fi

# Run the main script
"$PYTHON_BIN" main.py
