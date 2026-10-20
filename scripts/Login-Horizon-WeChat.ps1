<#
[INPUT]: 依赖本地 Python 环境、Horizon 微信 CLI 与 data/config.json
[OUTPUT]: 完成微信扫码登录并将 iLink 会话保存到 data/wechat_session.json
[POS]: scripts 模块的微信会话安装器，只在首次登录或会话失效时运行
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
#>

param([switch]$Force)

$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$WorkspaceRoot = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot "..\.."))
$Python = Join-Path $WorkspaceRoot "work\Horizon-main\.venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python environment not found: $Python"
}

$arguments = @("-m", "src.services.wechat_cli", "login")
if ($Force) {
    $arguments += "--force"
}

Push-Location $RepoRoot
try {
    & $Python @arguments
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}

