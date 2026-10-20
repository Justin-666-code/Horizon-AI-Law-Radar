# data/
> L2 | 父级: ../CLAUDE.md

成员清单
`config.github.json` - GitHub Actions 的可追踪个人配置，定义来源、评分阈值、配额和中文输出
`config.json` - 本地运行配置，内容与 Actions 配置同步，但被 `.gitignore` 忽略
`config.example.json` - 上游完整配置样例
`presets.json` - 上游向导使用的来源预设
`summaries/` - 本地生成的历史 Markdown 简报
`seen.json` - 本地去重历史，运行后生成
`subscribers.json` - 邮件订阅者状态，运行后生成

法则: 配置不是密钥仓库；真实凭据只从环境变量注入。
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

