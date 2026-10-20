# 验证契约

## 自动验证

1. `uv run pytest tests/test_personal_radar.py tests/test_profiles.py tests/test_cli.py -q`
2. `uv run python -m json.tool data/config.github.json`
3. `uv run python -m json.tool data/config.json`
4. 使用项目 `Config` 与 `ProfileRegistry` 加载配置，确认所有来源 profile 引用有效。

## 用户流验证

1. 在 `data/config.json` 所在的本地仓库创建 `.env` 并设置 `DASHSCOPE_API_KEY`。
2. 运行 `uv run horizon --hours 24`。
3. 确认 `data/summaries/` 生成当日中文 Markdown。
4. 确认简报按“机会公告、法律治理、AI 研究、AI 产品与产业、工程实践”顺序分段，且不超过 18 条。
5. 随机选择三条信息，确认每条都有原始链接，公告日期和资格信息与原文一致。
6. 运行 `scripts/Sync-Horizon-Daily.ps1`，确认 `D:\知识库\knowledge1\horizon-YYYY-MM-DD-zh.md` 存在且可读。
7. 连续运行同步脚本两次，确认第二次内容哈希和文件修改时间不变。

## GitHub 用户流

1. 推送仓库，添加 `DASHSCOPE_API_KEY` Secret。
2. 手动触发 `Daily Horizon Summary`。
3. 确认工作流成功并创建 `gh-pages` 分支。
4. 在 GitHub Pages 选择 `gh-pages` 根目录。
5. 打开页面，确认当日中文简报可读。

## 失败语义

- 缺少 `DASHSCOPE_API_KEY`：工作流在明确报错后停止，不生成空简报冒充成功。
- Google News 在本地网络失败：其他 RSS 源继续运行；日志给出单个源失败，不中断整条流水线。
- AI 无法判断资格或法律状态：输出省略结论，并保留原文链接。
- 来源失效：跳过该来源并保留日志；连续失败时在个人配置中禁用或替换。
- 当日 `gh-pages` 文件尚未出现：在设定等待时间内轮询，超时后明确失败，不写入空文件。

