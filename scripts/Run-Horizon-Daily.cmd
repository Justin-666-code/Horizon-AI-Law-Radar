@echo off
chcp 65001 >nul
rem [INPUT]: 依赖同目录 Sync-Horizon-Daily.ps1、正常用户网络和微信本地会话
rem [OUTPUT]: 双击后同步当天日报到新闻雷达目录并发送一条紧凑微信
rem [POS]: scripts 模块的 Windows 一键入口，用于脱离受限 Codex 沙箱执行
rem [PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

set "SCRIPT=%~dp0Sync-Horizon-Daily.ps1"
set "INSTALL_SKILL=%~dp0Install-HorizonDailySkill.ps1"
set "DESTINATION=D:\TuringEcho\drafts\horizon-daily"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%INSTALL_SKILL%" -IfMissing

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT%" ^
  -Destination "%DESTINATION%" ^
  -WaitMinutes 90 ^
  -SendWeChat ^
  -WeChatMode compact

echo.
echo Exit code: %ERRORLEVEL%
pause
