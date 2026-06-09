#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../load-env.sh"
bash "$(dirname "$0")/../nlp2hillm/to-dsl-mouse-port-pl.sh"
bash "$(dirname "$0")/../nlp2hillm/apply-status-mouse-dry-run.sh"
echo "nlp mouse port ok"
