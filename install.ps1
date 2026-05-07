param(
    [ValidateSet("codex", "claude", "agents", "both", "all")]
    [string]$Target = "both",
    [string]$CodexHome = $env:CODEX_HOME,
    [string]$ClaudeHome = $env:CLAUDE_HOME,
    [string]$AgentsHome = $env:AGENTS_HOME
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsRoot = Join-Path $Root "skills"
$Skills = @("agent-routing-orchestrator")
$LegacySkills = @("cost-aware-delegation", "cross-agent-project-lead")

function Install-Skills($DestRoot) {
    New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null
    foreach ($skill in $LegacySkills) {
        $dest = Join-Path $DestRoot $skill
        if (Test-Path -LiteralPath $dest) {
            Remove-Item -Recurse -Force -LiteralPath $dest
            Write-Host "Removed legacy $skill -> $DestRoot"
        }
    }
    foreach ($skill in $Skills) {
        $src = Join-Path $SkillsRoot $skill
        $dest = Join-Path $DestRoot $skill
        if (Test-Path -LiteralPath $dest) {
            Remove-Item -Recurse -Force -LiteralPath $dest
        }
        Copy-Item -Recurse -Force -LiteralPath $src -Destination $DestRoot
        Write-Host "Installed $skill -> $DestRoot"
    }
}

if (-not $CodexHome) {
    $CodexHome = Join-Path $env:USERPROFILE ".codex"
}
if (-not $ClaudeHome) {
    $ClaudeHome = Join-Path $env:USERPROFILE ".claude"
}
if (-not $AgentsHome) {
    $AgentsHome = Join-Path $env:USERPROFILE ".agents"
}

if ($Target -in @("codex", "both", "all")) {
    Install-Skills (Join-Path $CodexHome "skills")
}

if ($Target -in @("claude", "both", "all")) {
    Install-Skills (Join-Path $ClaudeHome "skills")
}

if ($Target -in @("agents", "all")) {
    Install-Skills (Join-Path $AgentsHome "skills")
}
