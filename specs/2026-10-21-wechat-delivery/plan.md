# 实施计划

## 1. 消息构造

- 产物：`scripts/send_wechat_summary.py`
- 完成条件：去掉 Front Matter，保留概览和完整日报链接，支持 compact/full。

## 2. 本机投递

- 产物：`scripts/Send-Horizon-WeChat.ps1`
- 完成条件：调用本地 Python 环境和 `WeChatNotifier`，按日期哈希去重。

## 3. 每日串联

- 产物：更新后的 `scripts/Sync-Horizon-Daily.ps1` 与 Codex 自动化
- 完成条件：知识库写入成功后发送微信；知识库内容不因微信失败而删除。

## 4. 扫码登录与验证

- 产物：`scripts/Login-Horizon-WeChat.ps1`、`data/wechat_session.json`
- 完成条件：用户扫码并给机器人发消息后，`WeChatSession.ready` 为真。

