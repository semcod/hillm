#!/usr/bin/env bash
# Source from example scripts: source examples/load-env.sh
set -euo pipefail
hillm_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "$hillm_root/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$hillm_root/.env"
  set +a
fi
export HILLM_DRY_RUN="${HILLM_DRY_RUN:-1}"
