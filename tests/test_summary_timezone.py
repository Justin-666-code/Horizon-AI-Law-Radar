"""
[INPUT]: 依赖 orchestrator 的 _summary_date 与标准库 ZoneInfo
[OUTPUT]: 验证 HORIZON_TIMEZONE 下的日报日期边界
[POS]: tests 模块的日报日期契约测试，防止 UTC 跨日覆盖前一天文件
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from datetime import datetime, timezone

from src.orchestrator import _summary_date


def test_shanghai_summary_date_advances_after_utc_midnight_boundary() -> None:
    utc_time = datetime(2026, 10, 21, 23, 30, tzinfo=timezone.utc)

    assert _summary_date(utc_time, "Asia/Shanghai") == "2026-10-22"


def test_utc_summary_date_is_preserved() -> None:
    utc_time = datetime(2026, 10, 21, 23, 30, tzinfo=timezone.utc)

    assert _summary_date(utc_time, "UTC") == "2026-10-21"
