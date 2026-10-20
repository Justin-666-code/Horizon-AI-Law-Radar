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
PROFILES=ai-creator,ai-foundations,ai-research,career-opportunity,finance-news,law-governance,tech-blog,tech-news
CONFIG_OK profiles=8 generated_config=true
```

`data/config.json` 由 `data/radar-preferences.json` 生成，不再手工复制或维护。

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
Length: 7951 bytes
SHA256: A754C416327ED54B9CBE51656C5D2BAB9374AA443471863E8B86DA07783DD748
First run: saved
Second run: unchanged
Hash stable: true
Mtime stable: true
```

Codex 每日 08:00 自动化已创建并持久化到 `C:\Users\16339\.codex\automations\horizon\automation.toml`。Windows 系统计划任务在当前受限沙箱身份下因 `New-ScheduledTaskAction` 权限被拒绝，脚本保留给普通桌面环境作为可选备选；每日同步由已验证的 Codex 自动化承担。

## 一手信息与大二适配整改

验证命令：

```powershell
python scripts/apply_radar_preferences.py --input data/config.github.json --preferences data/radar-preferences.json --output data/config.json
pytest tests/test_radar_preferences.py tests/test_personal_radar.py tests/test_profiles.py -q
actionlint .github/workflows/daily-summary.yml
```

结果：

```text
Generated data/config.json with 27 RSS sources, 10 max items, policy mixed
53 focused tests passed
545 full regression tests passed excluding the two known Windows-only upstream path assertions
ACTIONLINT_OK
```

生成配置的默认来源：

```text
arXiv CS.AI + CS.CL
OpenAI News
MIT News AI
Microsoft Research
Google AI Blog
Lilian Weng
Sebastian Raschka
Andrej Karpathy
fast.ai
GitHub AI and ML
Simon Willison
vLLM Blog
```

默认关闭：

```text
Hacker News
Reddit
Telegram
OSS Insight
Google News - 中文 AI 前沿
EFF Digital Rights
```

日报画像顺序：

```text
ai-foundations, ai-research, tech-news, tech-blog, law-governance, career-opportunity
```

内容域配额：

```text
foundations=3
research=2
ai-updates=1
engineering=2
law=1
opportunity=1
other=0
max_items=10
```

一手源实时探测：

```text
OpenAI News              200  1300 entries
MIT News AI              200    50 entries
Microsoft Research       200    10 entries
Google AI Blog           200    20 entries
Lilian Weng              200    53 entries
Sebastian Raschka        200    20 entries
Andrej Karpathy          200    10 entries
fast.ai                  200    20 entries
GitHub AI and ML         200    10 entries
PyTorch Blog             200    10 entries
TensorFlow Blog          200    25 entries
Apple ML Research        200    10 entries
Berkeley BAIR Blog       200    10 entries
CMU ML Blog              200     1 entry
Amazon Science           200    25 entries
Machine Learning Mastery 200    10 entries
PyImageSearch            200     9 entries
EU Digital Strategy      200     1 entry
WIPO Press Releases      reachable, no recent item in the final run
USPTO News               404, disabled by failure isolation
U.S. Copyright Office    404, disabled by failure isolation
Simon Willison           200    30 entries
vLLM Blog                200    50 entries
arXiv API                此前成功，本次连续探测触发 429 限流
```

arXiv 在 Horizon 中属于单源失败可降级路径；本次不会因限流删除该研究入口，但 Microsoft Research、MIT News AI 等一手研究源仍可在 arXiv 限流时提供内容。

最终线上验证：

```text
Run: 39403257390
Conclusion: success
Duration: 2m 31s
Fetched: 22
Analyzed: 22
Selected: 3
AI foundations: 1/3
Research: 1/2
AI updates: 0/1
Engineering: 0/2
Law: 1/1
Opportunity: 0/1
Token usage: 35973
Final article: 4009 characters / 7951 bytes
```

入选内容：

```text
Python 描述符与受控属性
检索工具输出导致 LLM 代理准确率下降
欧盟委员会委托开展《数字服务法》下网络金融诈骗研究
```

法律查询增加 `max_items=10` 后，从上一轮的 34 条候选降到 2 条；选调最多 5 条、法硕最多 3 条。官方知识产权源中 EU Digital Strategy 贡献 1 条法律治理内容，USPTO 与 Copyright Office RSS 返回 404，Horizon 按单源失败隔离。法硕/选调候选低于 3.5 分，仍未进入日报。

