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
- 每日日报会自动同步到 `D:\知识库\knowledge1\horizon-YYYY-MM-DD-zh.md`。

日常修改只需先看：

- [`data/radar-preferences.json`](data/radar-preferences.json)：每日条数、阈值、分类配额和一手/二手策略。
- [`docs/preferences-guide.md`](docs/preferences-guide.md)：如何修改检索标准。
- [`docs/information-quality.md`](docs/information-quality.md)：当前来源的一手性与局限。
- [`profiles/`](profiles/)：AI/计算机基础、研究、工程、知识产权治理、法硕与公共服务的判断标准。
- [`.github/workflows/daily-summary.yml`](.github/workflows/daily-summary.yml)：每日采集与 Pages 发布。
- [`specs/2026-10-20-personal-radar/validation.md`](specs/2026-10-20-personal-radar/validation.md)：验收与证据要求。

