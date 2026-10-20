<#
[INPUT]: 依赖本地 Python 环境、data/wechat_session.json 和知识库日报
[OUTPUT]: 将当日日报发送到微信，并用状态文件防止重复发送
[POS]: scripts 模块的微信投递入口，由每日知识库同步任务调用
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
#>

param(
    [string]$Date = (Get-Date -Format "yyyy-MM-dd"),
    [string]$SummaryPath = "",
    [ValidateSet("compact", "full")]
    [string]$Mode = "compact",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$WorkspaceRoot = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot "..\.."))
$Python = Join-Path $WorkspaceRoot "work\Horizon-main\.venv\Scripts\python.exe"
$Sender = Join-Path $PSScriptRoot "send_wechat_summary.py"
$StateFile = Join-Path $WorkspaceRoot "work\state\wechat-delivered.json"
$LogDir = Join-Path $WorkspaceRoot "work\logs"
$LogPath = Join-Path $LogDir "horizon-wechat.log"

if ([string]::IsNullOrWhiteSpace($SummaryPath)) {
    $SummaryPath = Join-Path "D:\知识库\knowledge1" "horizon-$Date-zh.md"
}

function Write-WeChatLog {
    param([string]$Message)
    New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
    $line = "{0} {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -LiteralPath $LogPath -Value $line -Encoding UTF8
}

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python environment not found: $Python"
}
if (-not (Test-Path -LiteralPath $SummaryPath)) {
    throw "Summary not found: $SummaryPath"
}

$arguments = @(
    $Sender,
    "--summary", $SummaryPath,
    "--date", $Date,
    "--mode", $Mode,
    "--state-file", $StateFile
)
if ($Force) {
    $arguments += "--force"
}

Write-WeChatLog "Sending $SummaryPath to WeChat ($Mode)"
try {
    & $Python @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "WeChat sender exited with code $LASTEXITCODE"
    }
    Write-WeChatLog "WeChat delivery succeeded for $Date"
}
catch {
    Write-WeChatLog "WeChat delivery failed: $($_.Exception.Message)"
    throw
}

