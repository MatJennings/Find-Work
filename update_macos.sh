#!/bin/sh
set -eu

find_work_repository=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$find_work_repository/plugins/find-work/scripts/update_plugin_version.py"
codex plugin add find-work@find-work-starter

echo "Find Work was refreshed. Start a new task to load the updated plugin."
