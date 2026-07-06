#!/usr/bin/env bash
# Source from example scripts: source examples/load-env.sh
set -euo pipefail
hillm_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Prefer the project venv so bare python3/hillm/nlp2hillm in example scripts
# resolve to the env where hillm is actually installed.
if [[ -x "$hillm_root/.venv/bin/python3" ]]; then
  export PATH="$hillm_root/.venv/bin:$PATH"
fi
if [[ -f "$hillm_root/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$hillm_root/.env"
  set +a
fi
export HILLM_DRY_RUN="${HILLM_DRY_RUN:-1}"
