$ErrorActionPreference = "Stop"

python (Join-Path $PSScriptRoot "plugins\find-work\scripts\update_plugin_version.py")
codex plugin add find-work@find-work-starter

Write-Host "Find Work was refreshed. Start a new task to load the updated plugin."
