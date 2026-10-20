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

### 抓取时间窗口

```json
"collection_time_window_hours": 24
```

调大可以覆盖低频作者，但 Horizon 当前不会跨运行持久去重，因此不建议为了“多抓一点”盲目调到 168 小时。需要更长窗口时，先确认重复内容是否可接受。

### 各栏目数量

```json
"category_limits": {
  "foundations": 3,
  "research": 2,
  "ai-updates": 1,
  "engineering": 2,
  "law": 1,
  "opportunity": 1,
  "other": 0
}
```

设为 `0` 会移除该栏目。`other` 是未归入其他栏目的兜底配额。

### 评分门槛

```json
"thresholds": {
  "ai-foundations": 6.8,
  "ai-research": 8.3,
  "tech-news": 7.5,
  "tech-blog": 7.5,
  "law-governance": 7.5,
  "career-opportunity": 8.0
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

默认 `information_policy` 是 `mixed`。AI 与计算机默认只启用 `primary` 来源；只有法律、知识产权、法硕和公共服务使用小比例 `secondary` 发现。

若要求绝对一手，把策略改为：

```json
"information_policy": "primary_only"
```

此时所有 `tier: secondary` 来源组必须关闭。系统不会静默把二手来源混进来。

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

RSS 来源可在 `data/config.github.json` 中设置 `max_items`，限制单次运行最多取多少条。宽泛搜索源应设置此上限；法律查询默认最多 10 条，法硕 3 条，选调 5 条。

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
5. `law-governance`：知识产权、AI 治理与法律，最多 1 条。
6. `career-opportunity`：法硕与公共服务路径，最多 1 条。

法硕与公共服务合计约占日报的 20%，并且必须能说明与 AI、计算机或数字治理的关系。

