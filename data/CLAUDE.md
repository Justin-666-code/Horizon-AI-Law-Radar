# data/
> L2 | 父级: ../CLAUDE.md

成员清单
`config.github.json` - GitHub Actions 的可追踪个人配置，定义来源、评分阈值、配额和中文输出
`radar-preferences.json` - 用户日常编辑的偏好真源，控制阶段、层级、阈值、配额和来源组
`config.json` - 由偏好生成器编译出的本地运行配置，被 `.gitignore` 忽略
`config.example.json` - 上游完整配置样例
`presets.json` - 上游向导使用的来源预设
`summaries/` - 本地生成的历史 Markdown 简报
`seen.json` - 本地去重历史，运行后生成
`subscribers.json` - 邮件订阅者状态，运行后生成

法则: 日常改偏好，来源底层改基础配置，生成配置不手改；真实凭据只从环境变量注入。
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

