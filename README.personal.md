# 从这里开始

这是一套已经按“AI 本科 + 法律硕士规划 + 定向选调规划”预配置好的 Horizon 个人雷达。

你的下一步只有三步：

1. 阅读 [密钥获取入口](KEY-SETUP.md) 和 [个人部署指南](docs/personal-setup.md)。
2. 在阿里云百炼北京地域创建一个 API Key，但不要发到聊天里。
3. 本地运行时把它填进 `.env`；GitHub 部署时把它填进仓库的 `DASHSCOPE_API_KEY` Secret。

先看结论：

- 必需密钥只有一个：`DASHSCOPE_API_KEY`。
- GitHub Actions 会自动提供 `GITHUB_TOKEN`，无需手动新建。
- 默认关闭邮件、微信和 Webhook，不需要提供额外密钥。
- 正式部署优先用 GitHub Actions，因为法律与选调搜索依赖的部分 RSS 在国内本地网络可能不可用。

配置入口：

- [`data/config.github.json`](data/config.github.json)：Actions 使用的来源、阈值和配额。
- [`profiles/`](profiles/)：AI 研究、法律治理、机会公告的判断与写作标准。
- [`.github/workflows/daily-summary.yml`](.github/workflows/daily-summary.yml)：每日采集与 Pages 发布。
- [`specs/2026-10-20-personal-radar/validation.md`](specs/2026-10-20-personal-radar/validation.md)：验收与证据要求。

