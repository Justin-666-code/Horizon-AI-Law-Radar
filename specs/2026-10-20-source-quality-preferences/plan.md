# 实施计划

## 1. 大二基础画像

- 产物：`profiles/ai-foundations/`
- 完成条件：能够区分基础学习价值与前沿新颖度，输出学习重点、先修知识和可执行练习。

## 2. 一手来源配置

- 产物：更新后的 `data/config.github.json`
- 完成条件：默认关闭所有二手发现层；保留并存一手 AI 源；研究论文数量受限。

## 3. 可编辑偏好

- 产物：`data/radar-preferences.json`、`scripts/apply_radar_preferences.py`
- 完成条件：生成器能应用阈值、配额、画像顺序和来源组开关；非法偏好明确失败。

## 4. 自动流水线

- 产物：更新后的 `.github/workflows/daily-summary.yml`
- 完成条件：Actions 在运行 Horizon 前从偏好文件生成配置并通过测试。

## 5. 用户文档与验证

- 产物：`docs/preferences-guide.md`、`docs/information-quality.md`、测试与验证证据
- 完成条件：用户知道日常只改一个文件；能追溯每个来源的一手/二手属性和限制。

