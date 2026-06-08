#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PIP="${PIP:-python3 -m pip}"

cd "$ROOT"
$PIP install -e .
$PIP install -e packages/dsl2hillm
$PIP install -e packages/uri2hillm
$PIP install -e packages/nlp2hillm
$PIP install -e packages/cli2hillm
$PIP install -e packages/mcp2hillm
$PIP install -e packages/rest2hillm
echo "✓ hillm control layers installed"
