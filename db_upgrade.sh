#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./db_upgrade.sh            # upgrade to head
#   ./db_upgrade.sh <revision> # upgrade to a specific revision

cd "$(dirname "$0")"

export FLASK_APP="run.py"

REVISION="${1:-head}"

flask db upgrade "$REVISION"
