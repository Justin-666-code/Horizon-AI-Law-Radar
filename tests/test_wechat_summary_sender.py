"""
[INPUT]: 依赖微信日报发送脚本的 Front Matter 与紧凑消息构造函数
[OUTPUT]: 验证微信消息不包含 YAML 头、保留栏目概览和完整日报链接
[POS]: tests 模块的微信投递契约测试，保护每日消息长度与内容边界
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "send_wechat_summary.py"
SPEC = importlib.util.spec_from_file_location("send_wechat_summary", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_compact_message_keeps_overview_and_link() -> None:
    markdown = """---
title: Test
---

> 从 10 条内容中筛选出 3 条。

---

**AI 与计算机基础**
1. [示例文章](#item-1)

---

## 详情
这里不应出现在紧凑消息中。
"""
    message = MODULE.build_message(
        markdown,
        "2026-10-21",
        "https://example.com/report",
        "compact",
    )

    assert "title: Test" not in message
    assert "示例文章" in message
    assert "这里不应出现在紧凑消息中" not in message
    assert "https://example.com/report" in message
    assert len(message) < 4000


def test_full_message_strips_only_front_matter() -> None:
    markdown = """---
title: Test
---

# Body

Full content.
"""
    message = MODULE.build_message(
        markdown,
        "2026-10-21",
        "https://example.com/report",
        "full",
    )

    assert "title: Test" not in message
    assert "Full content." in message

