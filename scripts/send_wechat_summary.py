"""
[INPUT]: 依赖本地 WeChat 会话、日报 Markdown、StorageManager 与 WeChatNotifier
[OUTPUT]: 将完整或紧凑日报发送到微信，并记录当日已发送哈希
[POS]: scripts 模块的微信投递器，由本机每日同步任务在知识库写入后调用
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

from src.models import WeChatConfig
from src.services.wechat import SESSION_FILE, WeChatNotifier
from src.storage.manager import StorageManager


def strip_front_matter(markdown: str) -> str:
    if not markdown.startswith("---\n"):
        return markdown.strip()
    parts = markdown.split("\n---\n", 1)
    if len(parts) != 2:
        return markdown.strip()
    return parts[1].strip()


def build_message(markdown: str, date: str, url: str, mode: str) -> str:
    body = strip_front_matter(markdown)
    if mode == "full":
        return body

    sections = body.split("\n---\n", 2)
    overview = "\n---\n".join(sections[:2]).strip()
    message = (
        f"# Horizon 日报 {date}\n\n"
        f"{overview}\n\n"
        f"[查看完整日报]({url})"
    )
    if len(message) <= 3800:
        return message
    paragraphs = overview.split("\n\n")
    kept: list[str] = []
    for paragraph in paragraphs:
        candidate = "\n\n".join([*kept, paragraph])
        if len(candidate) > 3000:
            break
        kept.append(paragraph)
    kept_text = "\n\n".join(kept).strip()
    return (
        f"# Horizon 日报 {date}\n\n"
        f"{kept_text}\n\n"
        f"[查看完整日报]({url})"
    )


def report_url(date: str, base_url: str) -> str:
    parsed = datetime.strptime(date, "%Y-%m-%d")
    return (
        f"{base_url.rstrip('/')}/{parsed.year}/"
        f"{parsed.month:02d}/{parsed.day:02d}/summary-zh.html"
    )


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a Horizon summary to WeChat")
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--mode", choices=("compact", "full"), default="compact")
    parser.add_argument(
        "--base-url",
        default="https://justin-666-code.github.io/Horizon-AI-Law-Radar",
    )
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    config_path = data_dir / "config.json"
    session_path = data_dir / SESSION_FILE
    if not args.summary.exists():
        raise FileNotFoundError(f"Summary not found: {args.summary}")
    if not session_path.exists():
        raise FileNotFoundError(
            f"WeChat session not found: {session_path}. Run Login-Horizon-WeChat.ps1."
        )

    markdown = args.summary.read_text(encoding="utf-8")
    url = report_url(args.date, args.base_url)
    message = build_message(markdown, args.date, url, args.mode)
    digest = hashlib.sha256(
        f"{args.mode}\0{message}".encode("utf-8")
    ).hexdigest()

    state = _load_state(args.state_file)
    previous = state.get(args.date)
    if not args.force and isinstance(previous, dict) and previous.get("hash") == digest:
        print(f"Already sent {args.date} ({args.mode}); skipping.")
        return

    storage = StorageManager(data_dir=data_dir, config_path=config_path)
    notifier = WeChatNotifier(
        WeChatConfig(enabled=True, languages=["zh"], chunk_size=4000),
        storage,
    )
    import asyncio

    result = asyncio.run(notifier.send_daily_summary(message, "zh"))
    if not result.sent:
        raise RuntimeError(result.detail or result.status.value)

    state[args.date] = {
        "hash": digest,
        "mode": args.mode,
        "chunks": result.chunks_sent,
        "sent_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "summary": str(args.summary),
    }
    _write_state(args.state_file, state)
    print(f"Sent {args.date} to WeChat in {result.chunks_sent} message(s).")


if __name__ == "__main__":
    main()

