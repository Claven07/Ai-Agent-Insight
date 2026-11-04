# Installs AI Agent Insights into the shared workspace skill path
# used by OpenAI Codex and Google Antigravity.
# Run from any PowerShell working directory:
#   .\scripts\install-workspace-skill.ps1

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceSkill = Join-Path $repoRoot "SKILL.md"
$sourceReferences = Join-Path $repoRoot "references"
$targetRoot = Join-Path $repoRoot ".agents\skills\ai-agent-insights"
$targetReferences = Join-Path $targetRoot "references"

if (-not (Test-Path -LiteralPath $sourceSkill -PathType Leaf)) {
    throw "Root SKILL.md not found: $sourceSkill"
}
if (-not (Test-Path -LiteralPath $sourceReferences -PathType Container)) {
    throw "references directory not found: $sourceReferences"
}

New-Item -ItemType Directory -Path $targetRoot -Force | Out-Null
New-Item -ItemType Directory -Path $targetReferences -Force | Out-Null

Copy-Item -LiteralPath $sourceSkill -Destination (Join-Path $targetRoot "SKILL.md") -Force
Get-ChildItem -LiteralPath $targetReferences -Force | Remove-Item -Recurse -Force
Copy-Item -Path (Join-Path $sourceReferences "*") -Destination $targetReferences -Recurse -Force

$installedSkill = Join-Path $targetRoot "SKILL.md"
$installedReferenceCount = @(Get-ChildItem -LiteralPath $targetReferences -File -Recurse).Count
if (-not (Test-Path -LiteralPath $installedSkill -PathType Leaf)) {
    throw "Installation failed: target SKILL.md is missing."
}
if ($installedReferenceCount -lt 1) {
    throw "Installation failed: no reference files were copied."
}

Write-Host ""
Write-Host "AI Agent Insights installed for this workspace." -ForegroundColor Green
Write-Host "Location: $targetRoot"
Write-Host "Reference files: $installedReferenceCount"
Write-Host ""
Write-Host "Open this repository folder in Codex and/or Antigravity."
Write-Host "Start a NEW chat, then invoke the skill:"
Write-Host '  Codex:       $ai-agent-insights'
Write-Host "  Antigravity: /ai-agent-insights"
