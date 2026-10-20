<#
[INPUT]: 依赖 GitHub CLI 凭据、gh-pages 分支中的每日 Markdown
[OUTPUT]: 将指定日期的中文日报原子写入目标知识库目录
[POS]: scripts 模块的本机同步器，由 Windows 计划任务每日调用
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
#>

param(
    [string]$Destination = "D:\知识库\knowledge1",
    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),
    [int]$WaitMinutes = 90,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$WorkspaceRoot = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot "..\.."))
$WorkRoot = Join-Path $WorkspaceRoot "work"
$GhExe = Join-Path $WorkRoot "gh\bin\gh.exe"
$GhConfigDir = Join-Path $WorkRoot "gh-config"
$LogDir = Join-Path $WorkRoot "logs"
$LogPath = Join-Path $LogDir "horizon-daily-sync.log"
$Repository = "Justin-666-code/Horizon-AI-Law-Radar"
$RemotePath = "_posts/$Date-summary-zh.md"
$TargetPath = Join-Path $Destination "horizon-$Date-zh.md"

function Write-SyncLog {
    param([string]$Message)

    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8
}

if (-not (Test-Path -LiteralPath $GhExe)) {
    throw "GitHub CLI not found: $GhExe"
}
if (-not (Test-Path -LiteralPath $GhConfigDir)) {
    throw "GitHub CLI config not found: $GhConfigDir"
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$env:GH_CONFIG_DIR = $GhConfigDir
$env:GH_PROMPT_DISABLED = "1"
$env:GH_PAGER = "cat"

$deadline = (Get-Date).AddMinutes([Math]::Max(0, $WaitMinutes))
$content = $null

do {
    Write-SyncLog "Fetching $RemotePath from $Repository"
    $encoded = & $GhExe api "repos/$Repository/contents/$RemotePath`?ref=gh-pages" --jq ".content" 2>$null
    if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace(($encoded -join ""))) {
        try {
            $bytes = [Convert]::FromBase64String(($encoded -join ""))
            $candidate = [Text.Encoding]::UTF8.GetString($bytes)
            if ($candidate.Length -gt 500 -and $candidate.Contains("Horizon Summary")) {
                $content = $candidate
                break
            }
        }
        catch {
            Write-SyncLog "Decode failed: $($_.Exception.Message)"
        }
    }

    if ((Get-Date) -ge $deadline) {
        break
    }
    Start-Sleep -Seconds 60
} while ($true)

if ($null -eq $content) {
    throw "No valid Horizon summary for $Date after waiting $WaitMinutes minutes"
}

$unchanged = $false
if ((Test-Path -LiteralPath $TargetPath) -and -not $Force) {
    $existing = [System.IO.File]::ReadAllText($TargetPath, [Text.Encoding]::UTF8)
    $unchanged = ($existing -ceq $content)
}

if (-not $unchanged) {
    $tempPath = "$TargetPath.tmp"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($tempPath, $content, $utf8NoBom)
    Move-Item -LiteralPath $tempPath -Destination $TargetPath -Force
    Write-SyncLog "Saved $TargetPath"
}
else {
    Write-SyncLog "Unchanged $TargetPath"
}

Write-Output $TargetPath

