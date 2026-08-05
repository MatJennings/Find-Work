$ErrorActionPreference = "Stop"

$findWorkRepository = $PSScriptRoot
if (-not (Get-Command codex -ErrorAction SilentlyContinue)) {
    throw "The codex command is unavailable. Open this folder in the ChatGPT desktop app and use its integrated terminal, then retry."
}

codex plugin marketplace add $findWorkRepository
codex plugin add find-work@find-work-starter

Write-Host ""
Write-Host "Find Work is installed. Confirm that find-work appears below:"
codex plugin list
Write-Host ""
Write-Host "Create a private job-search folder, open it in the desktop app, and ask:"
Write-Host "Use `$setup-job-search to set up this folder."
