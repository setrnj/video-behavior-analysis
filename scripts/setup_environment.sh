#!/usr/bin/env bash
set -euo pipefail

# Location: scripts/setup_environment.sh
# Purpose: create/use a virtualenv at project root/.venv and install requirements
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
# 修正：指向上级目录的 requirements.txt（根据你的目录结构）
REQ_FILE="$PROJECT_ROOT/../requirements.txt"

echo "Project root: $PROJECT_ROOT"
echo "Virtualenv dir: $VENV_DIR"
echo "Requirements file: $REQ_FILE"

if [ -d "$VENV_DIR" ]; then
  echo "Using existing virtualenv at $VENV_DIR"
else
  echo "Creating virtualenv..."
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install --upgrade pip setuptools wheel

if [ -f "$REQ_FILE" ]; then
  echo "Installing packages from $REQ_FILE"
  pip install -r "$REQ_FILE"
else
  echo "Warning: requirements.txt not found at $REQ_FILE"
  echo "You can still use the virtualenv; install packages manually if needed."
fi

echo "Environment setup complete. To activate:"
echo "  source \"$VENV_DIR/bin/activate\""
