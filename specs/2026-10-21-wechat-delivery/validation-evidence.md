# 微信投递验证证据

验证日期：2026-10-21

## 扫码会话

- 使用 Horizon 官方 iLink Bot 登录流程生成二维码。
- 用户扫码并在微信中给机器人发送消息。
- 本地会话保存到 `data/wechat_session.json`。
- `horizon-wechat status`：

```text
Context: present
Replies left: 9/10 (estimated)
Ready to deliver.
```

会话 token 和用户标识未写入本文档。

## 真实发送

命令：

```powershell
.\scripts\Send-Horizon-WeChat.ps1 -Date 2026-10-20 -SummaryPath "D:\知识库\knowledge1\horizon-2026-10-20-zh.md" -Mode compact -Force
```

结果：

```text
WeChat notification sent (1 messages).
Sent 2026-10-20 to WeChat in 1 message(s).
```

## 幂等验证

相同日期、相同摘要再次执行：

```text
Already sent 2026-10-20 (compact); skipping.
```

没有重复发送。

## 自动化

Codex 每日 08:00 自动化已更新为：

```text
Sync-Horizon-Daily.ps1 -Destination D:\知识库\knowledge1 -SendWeChat -WeChatMode compact
```

成功时静默；失败时才通知。自动化会验证知识库文件存在且微信投递状态中记录了当天消息。

