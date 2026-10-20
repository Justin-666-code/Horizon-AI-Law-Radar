<#
[INPUT]: 依赖 Sync-Horizon-Daily.ps1、Windows 计划任务与当前用户登录令牌
[OUTPUT]: 注册或更新每日 08:00 运行的 Horizon 知识库同步任务
[POS]: scripts 模块的安装器，将同步脚本接入 Windows 调度器
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
#>

param(
    [string]$TaskName = "Horizon Daily Knowledge Sync",
    [string]$Destination = "D:\知识库\knowledge1",
    [string]$DailyAt = "08:00"
)

$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$SyncScript = Join-Path $PSScriptRoot "Sync-Horizon-Daily.ps1"
$Powershell = Join-Path $env:SystemRoot "System32\WindowsPowerShell\v1.0\powershell.exe"
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

if (-not (Test-Path -LiteralPath $SyncScript)) {
    throw "Sync script not found: $SyncScript"
}

$escapedScript = $SyncScript.Replace('"', '""')
$escapedDestination = $Destination.Replace('"', '""')
$arguments = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$escapedScript`" -Destination `"$escapedDestination`" -WaitMinutes 90"

$action = New-ScheduledTaskAction `
    -Execute $Powershell `
    -Argument $arguments `
    -WorkingDirectory $RepoRoot
$trigger = New-ScheduledTaskTrigger -Daily -At $DailyAt
$principal = New-ScheduledTaskPrincipal `
    -UserId $CurrentUser `
    -LogonType Interactive `
    -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Copy the daily Horizon Markdown report to $Destination" `
    -Force | Out-Null

Get-ScheduledTask -TaskName $TaskName | Select-Object TaskName, State

