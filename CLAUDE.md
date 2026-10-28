# Horizon Personal Radar
Python + uv + GitHub Actions + RSS/Atom + Qwen API

这是一个基于 `Thysrael/Horizon` 的个人信息雷达配置分支。业务代码来自上游；个人层按“前沿 AI 输入层 -> AI 产品工程输出层 -> AI 安全治理/知识产权约束层 -> 数字政府应用场”筛选信息，并保留一手优先与每日投递能力。

<directory>
src/ - Horizon 采集、分类、评分、增强与简报流水线 (9子目录: ai, processing, scrapers, services, setup, storage, extractors, mcp, tests)
profiles/ - 培养路线感知的内容画像与提示词 (8套: tech-news, tech-blog, finance-news, ai-creator, ai-foundations, ai-research, law-governance, career-opportunity)
data/ - 运行配置、历史简报和本地状态
docs/ - 上游文档、Pages 静态站与个人部署指南
.github/workflows/ - 每日采集与 Pages 发布
specs/2026-10-20-personal-radar/ - 本功能的意图、计划与验证契约
tests/ - 上游回归测试与个人配置契约测试
scripts/ - 上游运维脚本与 Windows 知识库同步任务
</directory>

<config>
.python-version - uv 与开发者统一使用 Python 3.12
data/config.github.json - Actions 使用的可追踪个人配置
data/radar-preferences.json - 日常修改的阶段、来源层级、阈值和配额
data/config.json - 由偏好生成器编译出的运行配置，默认被 Git 忽略
scripts/apply_radar_preferences.py - 校验偏好并生成运行配置
.env.personal.example - 个人密钥变量名样例，不含真实密钥
KEY-SETUP.md - 必需与可选密钥的官方获取入口
.github/workflows/daily-summary.yml - 每日采集和 Pages 发布编排
scripts/Sync-Horizon-Daily.ps1 - 将 gh-pages 日报同步到本机知识库
scripts/Send-Horizon-WeChat.ps1 - 将同步后的日报发送到微信
scripts/skills/horizon-daily-delivery/SKILL.md - 每日知识库与微信双投递的唯一 Skill 真源
</config>

法则: 上游业务代码只读，个人偏好写配置，处理标准写 profile，密钥只进环境变量。
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

