#!/bin/sh
set -eu
LAB_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$LAB_DIR"
if [ -x .venv/bin/python ]; then
    exec .venv/bin/python scripts/check.py "${1:-all}"
fi
exec python3 scripts/check.py "${1:-all}"
