#!/bin/sh
set -eu

exec python3 "$(dirname "$0")/validate_project.py" --format-only "$@"
