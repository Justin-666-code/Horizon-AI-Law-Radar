# 密钥获取入口

这套配置只需要一个真实密钥：`DASHSCOPE_API_KEY`。

## 必需：阿里云百炼 API Key

直接创建地址：

https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key

官方说明：

https://help.aliyun.com/zh/model-studio/get-api-key

操作要点：

1. 登录阿里云并完成实名认证。
2. 打开百炼 API Key 页面。
3. 右上角地域选择 `华北 2（北京）`；当前配置使用北京地域的兼容接口。
4. 点击 `创建 API Key`，归属账号和业务空间使用默认值即可。
5. 创建后复制密钥，填入本地 `.env` 或 GitHub 仓库 Secret。

变量名固定为：

```text
DASHSCOPE_API_KEY
```

不要发到聊天、Issue、README、截图或 Git 提交中。

## 可选：GitHub Token

GitHub Actions 会自动提供 `GITHUB_TOKEN`，因此线上运行不需要手动创建。

只有在本机直接运行并频繁抓取 GitHub Releases 时，才建议建一个只读 Token：

https://github.com/settings/personal-access-tokens/new

本轮配置不创建任何 GitHub Token 也能通过 GitHub Actions 运行。

## 当前不需要的其他密钥

- `HORIZON_WEBHOOK_URL`：只有启用飞书、钉钉、Slack 或 Discord 推送时才需要。
- `EMAIL_PASSWORD`：只有启用邮件投递时才需要。
- `APIFY_TOKEN`：只有启用 X/Twitter 采集时才需要。
- `LWN_KEY`：只有订阅 LWN 全文时才需要。
- `OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`GOOGLE_API_KEY`：当前 `qwen-plus` 配置不需要。

