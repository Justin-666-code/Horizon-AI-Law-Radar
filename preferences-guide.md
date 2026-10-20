---
layout: default
title: 检索偏好修改指南
---

# 检索偏好修改指南

日常修改只需要编辑：

```text
data/radar-preferences.json
```

不要同时手改 `data/config.json`。后者是生成产物，下一次运行会被覆盖。

## 最常改的四组参数

### 每日条数

```json
"daily_item_limit": 10
```

这是全天文报的最终上限，不保证每个栏目都能填满。

### 各栏目数量

```json
"category_limits": {
  "foundations": 4,
  "research": 3,
  "ai-updates": 2,
  "engineering": 3,
  "other": 1
}
```

设为 `0` 会移除该栏目。`other` 是未归入其他栏目的兜底配额。

### 评分门槛

```json
"thresholds": {
  "ai-foundations": 6.8,
  "ai-research": 8.3,
  "tech-news": 7.5,
  "tech-blog": 7.0
}
```

数值越高越严格。不要把所有栏目一起降到很低；先看连续几天的入选结果，再只调整一个栏目。

### 来源组开关

```json
"source_groups": {
  "primary_ai": {
    "tier": "primary",
    "enabled": true
  },
  "community_discovery": {
    "tier": "secondary",
    "enabled": false
  }
}
```

默认 `information_policy` 是 `primary_only`，因此 `tier: secondary` 的组必须关闭。若确实需要聚合器或社区，先把策略改为：

```json
"information_policy": "mixed"
```

再显式启用对应组。系统不会静默把二手来源混进来。

## 三个修改层级

### 1. 日常检索标准

编辑 `data/radar-preferences.json`：

- 每日总条数。
- 各栏目条数。
- 各画像阈值。
- 一手/全部来源策略。
- 来源组启停。
- 栏目顺序。

### 2. 内容判断标准

编辑对应画像目录：

```text
profiles/ai-foundations/analysis.md
profiles/ai-research/analysis.md
profiles/tech-blog/analysis.md
```

`match.md` 决定什么内容属于该画像，`analysis.md` 决定评分标准，`enrichment.md` 决定日报写什么。

### 3. 来源本身

只有在新增、删除或替换具体 RSS、GitHub 仓库时才编辑：

```text
data/config.github.json
```

新增来源后，还要在 `data/radar-preferences.json` 的某个来源组里登记它的名称，生成器才会控制其启停。

## 应用修改

本地：

```powershell
uv run python scripts/apply_radar_preferences.py
uv run horizon --hours 24
```

GitHub Actions 会在每次日报运行前自动执行同一个生成器。推送到 `main` 后，下一天按新偏好运行。

## 当前默认画像顺序

1. `ai-foundations`：大二基础、数学、编程、训练与评测。
2. `ai-research`：少量高价值研究，明确预印本边界。
3. `tech-news`：官方模型、工具和项目发布。
4. `tech-blog`：第一手工程实践。

`law-governance` 和 `career-opportunity` 仍保留，但默认不进入日报。

