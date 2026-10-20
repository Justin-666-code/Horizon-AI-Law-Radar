# scripts/
> L2 | 父级: ../CLAUDE.md

成员清单
`check_mcp.py` - 上游 MCP 环境检查脚本
`daily-run.sh` - 上游 POSIX 每日运行脚本
`Sync-Horizon-Daily.ps1` - 从 `gh-pages` 拉取当日 Markdown 并原子写入本机知识库
`Register-Horizon-DailySync.ps1` - 为当前 Windows 用户注册每日 08:00 同步任务
`apply_radar_preferences.py` - 将可编辑偏好编译为 Horizon 最终配置并执行一致性检查
`Send-Horizon-WeChat.ps1` - 将当日知识库日报发送到微信并防止重复投递
`send_wechat_summary.py` - 构造紧凑或完整微信消息并调用 WeChatNotifier
`Login-Horizon-WeChat.ps1` - 首次扫码登录或强制刷新微信 iLink 会话

法则: 同步脚本不包含密钥，只通过隔离的 GitHub CLI 配置目录读取已有授权。
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

