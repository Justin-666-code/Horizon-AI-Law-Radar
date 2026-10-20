# Horizon Personal Radar
Python + uv + GitHub Actions + RSS/Atom + Qwen API

这是一个基于 `Thysrael/Horizon` 的个人信息雷达配置分支。业务代码来自上游，个人层只包含数据配置、处理画像、部署工作流和验证文档。

<directory>
src/ - Horizon 采集、分类、评分、增强与简报流水线 (9子目录: ai, processing, scrapers, services, setup, storage, extractors, mcp, tests)
profiles/ - 内容域画像与提示词 (8套: tech-news, tech-blog, finance-news, ai-creator, ai-foundations, ai-research, law-governance, career-opportunity)
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
</config>

法则: 上游业务代码只读，个人偏好写配置，处理标准写 profile，密钥只进环境变量。
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md

