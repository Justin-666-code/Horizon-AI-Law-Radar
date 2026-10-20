# 实施计划

## 1. 个人处理画像

- 产物：`profiles/ai-research/`、`profiles/law-governance/`、`profiles/career-opportunity/`
- 完成条件：每个 profile 均包含 `profile.json`、`match.md`、`analysis.md`、`enrichment.md`，可被 `ProfileRegistry` 加载。

## 2. 来源与运行参数

- 产物：`data/config.github.json`、`data/config.json`
- 完成条件：配置通过 Pydantic 校验；所有显式 profile 引用存在；来源类别进入配额组；中文单语；默认关闭外部投递。

## 3. 每日自动化

- 产物：`.github/workflows/daily-summary.yml`
- 完成条件：每日定时运行；只要求 `DASHSCOPE_API_KEY`；使用仓库自带 `GITHUB_TOKEN` 提高 GitHub API 限额；发布 `docs/` 到 `gh-pages`。

## 4. 可执行部署说明

- 产物：`docs/personal-setup.md`、`.env.personal.example`
- 完成条件：明确本地运行、GitHub 部署、密钥获取、Pages 开启、成本控制和常见故障排查步骤。

## 5. 自动验证

- 产物：`tests/test_personal_radar.py`
- 完成条件：验证追踪配置、个人 profile 和来源 profile 引用；运行项目既有 profile、配置和工作流相关测试。

## 6. 本机知识库同步

- 产物：`scripts/Sync-Horizon-Daily.ps1`、`scripts/Register-Horizon-DailySync.ps1`
- 完成条件：能从 `gh-pages` 获取当天中文 Markdown，写入 `D:\知识库\knowledge1`；重复运行不改变相同内容；每日 08:00 有自动触发。

