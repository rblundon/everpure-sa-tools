#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q
echo "Virtual environment ready. Activate with: source .venv/bin/activate"
