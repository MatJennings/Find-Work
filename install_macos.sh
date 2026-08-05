#!/bin/sh
set -eu

find_work_repository=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if ! command -v codex >/dev/null 2>&1; then
  echo "The codex command is unavailable. Open this folder in the ChatGPT desktop app and use its integrated terminal, then retry." >&2
  exit 1
fi

codex plugin marketplace add "$find_work_repository"
codex plugin add find-work@find-work-starter

echo
echo "Find Work is installed. Confirm that find-work appears below:"
codex plugin list
echo
echo "Create a private job-search folder, open it in the desktop app, and ask:"
echo 'Use $setup-job-search to set up this folder.'
