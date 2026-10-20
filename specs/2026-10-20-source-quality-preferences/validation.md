# 验证契约

## 自动验证

1. `uv run pytest tests/test_radar_preferences.py tests/test_personal_radar.py -q`
2. 使用偏好生成器生成临时配置，并由 `Config` 模型成功解析。
3. `primary_only` 下启用 `secondary` 来源组必须失败。
4. 未知画像阈值、未知分类组和缺失来源名称必须失败。
5. `actionlint .github/workflows/daily-summary.yml` 通过。

## 配置断言

- `ai-foundations` 存在且处于默认画像顺序首位。
- 默认 `information_policy` 为 `primary_only`。
- Hacker News、Reddit、Telegram、OSS Insight、全部 Google News 和 EFF 默认关闭。
- 默认日报最多 10 条；基础、研究、更新、工程分别有独立配额。
- 法律治理与机会公告画像仍存在，但默认不进入日报。

## 用户流

1. 用户只编辑 `data/radar-preferences.json` 调整阈值或每日条数。
2. 本地运行生成器后启动 Horizon；GitHub Actions 自动使用同一偏好。
3. 若用户将 `information_policy` 改为 `mixed` 并启用法律组，生成器不再拒绝该组合。

