#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./db_downgrade.sh             # downgrade by one migration
#   ./db_downgrade.sh <revision>  # downgrade to a specific revision

cd "$(dirname "$0")"

export FLASK_APP="run.py"

REVISION="${1:--1}"

flask db downgrade "$REVISION"
