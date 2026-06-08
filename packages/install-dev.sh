#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [[ -x "$ROOT/.venv/bin/pip" ]]; then
  PIP="$ROOT/.venv/bin/pip"
elif [[ -n "${PIP:-}" ]]; then
  PIP="$PIP"
else
  PIP="python3 -m pip"
fi

cd "$ROOT"
$PIP install -e ".[dev,serial]"
$PIP install -e packages/dsl2hillm
$PIP install -e packages/uri2hillm
$PIP install -e packages/nlp2hillm
$PIP install -e packages/cli2hillm
$PIP install -e packages/mcp2hillm
$PIP install -e packages/rest2hillm
echo "✓ hillm control layers installed"
