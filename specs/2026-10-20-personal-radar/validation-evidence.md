# 验证证据

验证日期：2026-10-20

环境：

- Windows / PowerShell 5.1
- Python 3.12.15
- uv 0.13.3
- actionlint 1.7.12

## 配置与画像

命令：

```powershell
python -c "from pathlib import Path; from src.models import Config; from src.processing.profiles import ProfileRegistry; c=Config.model_validate_json(Path('data/config.github.json').read_text(encoding='utf-8')); r=ProfileRegistry.load(Path('profiles'), c.processing.default_profile); r.validate_source_references(c.sources.model_dump(mode='json')); print('PROFILES=' + ','.join(sorted(r.ids)))"
```

结果：

```text
PROFILES=ai-creator,ai-research,career-opportunity,finance-news,law-governance,tech-blog,tech-news
CONFIG_OK profiles=7 rss=10 profiles_order=career-opportunity,law-governance,ai-research,tech-news,tech-blog
```

`data/config.json` 与 `data/config.github.json` 的 SHA-256 一致，且都通过 `python -m json.tool`。

## 自动化测试

聚焦测试：

```text
43 passed in 1.94s
```

覆盖文件：`test_personal_radar.py`、`test_profiles.py`、`test_balanced_digest.py`、`test_cli.py`。

除 Windows 路径断言外全量回归：

```text
540 passed in 5.01s
```

完整 Windows 回归：

```text
2 failed, 547 passed in 4.90s
```

两处失败均为上游 `tests/test_setup_wizard.py` 在 Windows 上把 `data/presets.json` 与 `data\\presets.json` 直接比较，和本个人配置无关。GitHub Actions 使用 Linux runner，不触发该路径差异。

## 工作流

命令：

```powershell
actionlint .github/workflows/daily-summary.yml
```

结果：

```text
ACTIONLINT_OK
```

额外使用 PyYAML 解析通过，识别到 job：`daily-summary`。

## 真实来源抓取

使用 `httpx + feedparser` 对配置中的非 Google News RSS 做实时探测：

| 来源 | 结果 | HTTP | 条目 |
| --- | --- | --- | --- |
| arXiv CS.AI + CS.CL | 通过 | 200 | 25 |
| OpenAI News | 通过 | 200 | 1300 |
| MIT News AI | 通过 | 200 | 50 |
| Simon Willison | 通过 | 200 | 30 |
| vLLM Blog | 通过 | 200 | 50 |
| EFF Digital Rights | 通过 | 200 | 50 |

四个 Google News 查询在当前本地网络被跳过，设计上由 GitHub Actions 执行。Horizon 对单个源失败采用跳过并记录日志的语义。

## 尚未执行

- 没有真实 `DASHSCOPE_API_KEY`，因此没有执行真实的模型评分、增强和最终日报生成。
- 没有用户 GitHub 仓库与 Actions Secret，因此没有执行线上定时工作流和 Pages 发布。

这两项必须由用户在本机或 GitHub 上注入密钥后完成；不能用配置解析通过代替模型与端到端验证。

