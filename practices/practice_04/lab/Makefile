.PHONY: setup test baseline a b mcp-proof

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

test:
	sh scripts/check.sh all

baseline:
	sh scripts/check.sh baseline

a:
	sh scripts/check.sh a

b:
	sh scripts/check.sh b

mcp-proof:
	.venv/bin/python scripts/prove_mcp.py
