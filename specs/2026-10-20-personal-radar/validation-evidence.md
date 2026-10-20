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

## GitHub Actions 线上运行

仓库：`https://github.com/Justin-666-code/Horizon-AI-Law-Radar`

首次真实运行：

```text
Run: 39390055800
Conclusion: success
Duration: 9m 12s
Fetched: 174
Analyzed: 174
Passed profile filters: 23
Removed topic duplicates: 1
Balanced digest: 8/22
Enriched: 8/8
Token usage: 192214 (input: 159316, output: 32898)
```

生成并发布：

```text
data/summaries/horizon-2026-10-20-zh.md
docs/_posts/2026-10-20-summary-zh.md
gh-pages commit: 14992e8cb1d99188844a5d959743f38a1debc40b
Pages build: built
```

线上验证：

```text
Home: 200, contains 2026-10-20
Article: 200
Pages: https://justin-666-code.github.io/Horizon-AI-Law-Radar/
```

当日机会公告和法律治理来源有抓取结果，但没有条目达到 7.5 分，因此简报没有为了填满栏目而加入低质量内容。后续应基于多个自然日的分布再调整阈值，不用单日结果直接放宽。

## 本机知识库同步

已实测：

```text
Target: D:\知识库\knowledge1\horizon-2026-10-20-zh.md
Length: 16672 bytes
SHA256: DBC43E659781522B79B8074C94591F92DDE5D16FB7D0A349531DFFCA583DA78F
First run: saved
Second run: unchanged
Hash stable: true
Mtime stable: true
```

Codex 每日 08:00 自动化已创建并持久化到 `C:\Users\16339\.codex\automations\horizon\automation.toml`。Windows 系统计划任务在当前受限沙箱身份下因 `New-ScheduledTaskAction` 权限被拒绝，脚本保留给普通桌面环境作为可选备选；每日同步由已验证的 Codex 自动化承担。

