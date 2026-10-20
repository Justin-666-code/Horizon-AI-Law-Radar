---
layout: default
title: 个人雷达部署指南
---

# AI × 法律 × 公共服务雷达

这套配置面向“人工智能本科 + 法律硕士规划 + 定向选调规划”的日常信息筛选。它不替你做报考判断，也不提供法律意见；它负责把分散的信息收拢、去重、排序，并把原文链接留在你面前。

## 你会得到什么

- `AI 基础与动手实践`：数学、机器学习、编程、训练、评测和可执行练习。
- `AI 研究前沿`：严格限额的一手研究预印本和机构研究。
- `AI 产品与产业`：官方模型与工具发布、一手项目更新。
- `工程实践`：vLLM、GitHub AI、Simon Willison 等第一手工程文章。

默认每天最多 10 条，只输出中文。法律治理、法硕和选调来源仍保留但默认关闭，因为当前阶段优先建立 AI 基础。所有生成结果在 `data/summaries/`，GitHub Actions 会把 `docs/` 发布到 Pages。

## 覆盖边界

默认策略是一手优先，因此不使用 Google News、Reddit、Telegram 等二手发现层。未来启用法律或选调信息时，省级人事考试网、学校研究生院和微信公众号仍可能不可覆盖，必须保留人工官网复核。

## 第一步：拿到唯一的必需密钥

默认模型是阿里云百炼的 `qwen-plus`，对中文、法律文本和结构化输出都比较合适，国内访问也直接。

1. 打开 [百炼北京地域 API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。
2. 完成实名认证并开通百炼模型服务。
3. 确认右上角地域为 `华北 2（北京）`，然后创建一个 API Key。官方步骤见 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
4. 只把密钥填进 `.env` 或 GitHub Secrets。

请不要把密钥粘贴到聊天、Issue、README、截图或提交记录里。Horizon 的 `data/config.github.json` 只保存环境变量名 `DASHSCOPE_API_KEY`，不会保存密钥值。

如果你更想用 DeepSeek，把 `data/config.github.json` 和 `data/config.json` 的 `ai` 段改为：

```json
{
  "ai": {
    "provider": "deepseek",
    "model": "deepseek-chat",
    "api_key_env": "DEEPSEEK_API_KEY",
    "temperature": 0.2,
    "max_tokens": 8192,
    "throttle_sec": 0.5,
    "analysis_concurrency": 2,
    "enrichment_concurrency": 1,
    "languages": ["zh"]
  }
}
```

然后把密钥变量改成 `DEEPSEEK_API_KEY`。不要把两套密钥同时写进公开仓库。

## 第二步：本地运行

Windows 上推荐用项目自带的 `uv` 工作流。若本机尚未安装 `uv`，按 [官方安装说明](https://docs.astral.sh/uv/getting-started/installation/) 安装即可。

```powershell
Copy-Item .env.personal.example .env
# 用编辑器打开 .env，把 replace-me 换成真实密钥
uv sync
uv run horizon --hours 24
```

运行后检查：

```powershell
Get-ChildItem data\summaries
Get-Content (Get-ChildItem data\summaries\*.md | Sort-Object LastWriteTime | Select-Object -Last 1)
```

如果你在中国大陆直接运行，Google News 和部分境外源可能连接失败。失败的单个源会写日志并跳过，不会把整条流水线伪装成成功；正式使用请以 GitHub Actions 为主。

## 第三步：部署到 GitHub Actions

### 3.1 推送到 GitHub

把这个目录作为仓库根目录推送到你自己的 GitHub 仓库。不要只上传 `data/config.json`，因为它被 `.gitignore` 忽略；Actions 使用 `data/config.github.json` 和 `data/radar-preferences.json` 生成运行配置。

如果本机没有 Git，推荐安装 [GitHub Desktop](https://desktop.github.com/)，选择 `File` → `Add local repository`，选中这个目录；仓库尚不存在时按提示创建，再点击 `Publish repository`。发布后回到浏览器继续添加 Secret。

### 3.2 添加密钥

打开仓库：

`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

添加：

| 名称 | 是否必需 | 用途 |
| --- | --- | --- |
| `DASHSCOPE_API_KEY` | 是 | 百炼模型调用 |
| `GITHUB_TOKEN` | 否 | Actions 自动提供，工作流已直接使用；无需手动创建 |
| `HORIZON_WEBHOOK_URL` | 否 | 飞书、钉钉、Slack、Discord 或自定义 Webhook |
| `EMAIL_PASSWORD` | 否 | 邮件投递，默认关闭 |
| `APIFY_TOKEN` | 否 | X/Twitter，默认关闭 |

### 3.3 运行工作流

打开 `Actions` → `Daily Horizon Summary` → `Run workflow`。

工作流会：

1. 安装 Python 与 uv。
2. 安装 Horizon 依赖。
3. 把 `data/radar-preferences.json` 编译成运行配置。
4. 抓取、评分、去重、补充背景并生成中文简报。
5. 把 `docs/` 发布到 `gh-pages` 分支。

仓库没有密钥时，工作流会在预检步骤明确失败，不会生成空日报。

### 3.4 打开 Pages

第一次成功运行并创建 `gh-pages` 分支后，进入：

`Settings` → `Pages` → `Build and deployment` → `Deploy from a branch`

选择：

- Branch: `gh-pages`
- Folder: `/ (root)`

保存后等待 GitHub 构建，页面地址通常是：

```text
https://<你的 GitHub 用户名>.github.io/<仓库名>/
```

如果仓库是私有的，GitHub Pages 的可访问性取决于你的 GitHub 套餐；个人长期使用可以把仓库设为公开，但不要把密钥放在仓库中。

## 每天怎么读

优先看“AI 基础与动手实践”，把能在一个月至三个月内完成的练习挑出来。接着看少量研究论文，明确它们是预印本还是正式发表。最后看官方产品更新和工程实践。

## 同步到本机知识库

每天生成的 Markdown 会由本机定时自动化同步到：

```text
D:\知识库\knowledge1\horizon-YYYY-MM-DD-zh.md
```

同步器位于 `scripts/Sync-Horizon-Daily.ps1`。它从仓库的 `gh-pages` 分支读取日报，先写临时文件再原子替换，内容没有变化时不会重写。日志位于工作区的 `work/logs/horizon-daily-sync.log`。

Codex 定时自动化已配置为每天北京时间 08:00 执行，成功时静默，下载失败或目标目录不可写时才提醒。`scripts/Register-Horizon-DailySync.ps1` 也可在普通桌面 PowerShell 中注册 Windows 计划任务，作为 Codex 应用未运行时的备选；在受限沙箱内注册系统任务会被 Windows 拒绝，这不影响 Codex 自动化。

## 如何按你的方向微调

### 可选：缩小选调地域

这属于未来阶段。先把 `information_policy` 改为 `mixed`，再启用 `secondary_law_and_career` 来源组。

编辑 `data/config.github.json` 中 `Google News - 选调与公务员` 的 URL，在查询词中加入你的目标省份，例如：

```text
广东 选调生
```

同时保留全国查询，避免漏掉中央或其他机会。

### 关注特定法硕院校

同上，需要先启用二手来源组；不要把院校条件写进通用 profile。

在 `data/config.github.json` 中新增一条 RSS，并在 `data/radar-preferences.json` 的来源组中登记名称，再运行偏好生成器：

```text
site:edu.cn 法律硕士 招生 <学校名>
```

不要把院校名写进 profile；profile 管判断标准，config 管个人来源。

### 控制模型花费

优先调低这四项：

- `source_groups` 中启用的来源组数量。
- `collection.time_window_hours`，默认 24 小时。
- `daily_item_limit`，默认 10 条。
- `ai.analysis_concurrency` 和 `ai.enrichment_concurrency`，默认 2 和 1。

不要为了省成本把 `ai.max_tokens` 降到 2000 以下；公告细节和结构化输出容易截断。

### 启用飞书或钉钉

在 `data/config.github.json` 的运行配置中加入 `webhook` 段，并只在 Actions Secret 中保存 URL。推荐先用 `uv run horizon-webhook --dry-run` 检查模板，再启用真实发送。默认配置没有开启投递，因此第一次部署不会因为 Webhook 配错而失败。

## 常见故障

### `DASHSCOPE_API_KEY is missing`

本地检查 `.env` 是否在仓库根目录；Actions 检查 Secret 名称是否完全一致，然后重新运行工作流。

### `Google News` 抓取失败

这通常是本地网络问题。先运行 `uv run horizon --hours 24` 查看其他源是否正常；正式使用请依赖 GitHub Actions。若 Actions 也连续失败，检查 Google News RSS 是否变更，或暂时把该来源设为 `enabled: false`。

### 简报条目太少

不要立刻把阈值全部降到 0。先看日志是哪个来源失败，再按域把 `career-opportunity` 或 `law-governance` 的阈值降到 7.0，观察一周后调整。

### GitHub Pages 404

先确认工作流成功且 `gh-pages` 分支已创建，再确认 Pages 的发布分支选择了 `gh-pages` 根目录。Pages 构建有短暂延迟，不要连续重复触发工作流。

## 安全边界

- `.env` 已被 `.gitignore` 忽略；不要把真实密钥写进 `.env.personal.example`。
- `data/config.json` 也是本地运行文件，密钥值不应出现在任何 JSON。
- Actions Secret 只在工作流运行时注入，不会变成仓库文件。
- GitHub 仓库和 Pages 的公开范围由你决定；公告和摘要可能有个人信息或未公开招聘内容，默认不要把敏感内容公开发布。

