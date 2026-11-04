#!/bin/bash
# Dual-Engine RAG Backend — start FastAPI server (port 8080)
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/backend"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/venv/Scripts/activate" ]; then
    source "$SCRIPT_DIR/venv/Scripts/activate"
elif [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "ERROR: venv not found. Create it first:"
    echo "  cd $SCRIPT_DIR && ./setup.sh"
    exit 1
fi

echo "Starting Dual-Engine RAG backend on port 8080..."
uvicorn app.main:app --reload --port 8080
