"""
[INPUT]: 依赖项目内 Horizon 同步脚本、微信会话、知识库目标目录和 Asia/Shanghai 时区
[OUTPUT]: 完成或检查当天日报的知识库同步、微信投递及状态验证
[POS]: horizon-daily-delivery Skill 的确定性执行器，消除每日重复手工流程
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROJECT_ROOT = Path(
    r"C:\Users\16339\Documents\Codex\2026-10-20"
    r"\ai-https-github-com-thysrael-horizon"
)
DEFAULT_REPO_ROOT = DEFAULT_PROJECT_ROOT / "outputs" / "horizon-student-radar"
DEFAULT_DESTINATION = Path(r"D:\TuringEcho\drafts\horizon-daily")
POWERSHELL = Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")


def _today() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d")


def _load_state(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _check(date: str, destination: Path, repo_root: Path) -> list[str]:
    problems: list[str] = []
    summary = destination / f"horizon-{date}-zh.md"
    if not summary.exists():
        problems.append(f"missing summary: {summary}")
    elif summary.stat().st_size <= 500:
        problems.append(f"summary too small: {summary} ({summary.stat().st_size} bytes)")

    workspace_root = repo_root.parents[1]
    state_path = workspace_root / "work" / "state" / "wechat-delivered.json"
    record = _load_state(state_path).get(date)
    if not isinstance(record, dict):
        problems.append(f"missing WeChat delivery record for {date}")
    elif int(record.get("chunks") or 0) < 1:
        problems.append(f"invalid WeChat chunk count for {date}")

    if not (repo_root / "data" / "wechat_session.json").exists():
        problems.append("missing local WeChat session")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description="Run or check Horizon daily delivery")
    parser.add_argument("--date", default=_today())
    parser.add_argument("--wait-minutes", type=int, default=90)
    parser.add_argument("--mode", choices=("compact", "full"), default="compact")
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(os.environ.get("HORIZON_RADAR_ROOT", DEFAULT_REPO_ROOT)),
    )
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    sync_script = repo_root / "scripts" / "Sync-Horizon-Daily.ps1"
    if not sync_script.exists():
        raise SystemExit(f"Sync script not found: {sync_script}")
    if not POWERSHELL.exists():
        raise SystemExit(f"PowerShell not found: {POWERSHELL}")

    if args.check_only:
        problems = _check(args.date, args.destination, repo_root)
        if problems:
            print("\n".join(problems))
            raise SystemExit(2)
        print(f"READY date={args.date} destination={args.destination}")
        return

    command = [
        str(POWERSHELL),
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(sync_script),
        "-Destination",
        str(args.destination),
        "-Date",
        args.date,
        "-WaitMinutes",
        str(max(0, args.wait_minutes)),
        "-SendWeChat",
        "-WeChatMode",
        args.mode,
    ]
    result = subprocess.run(command, cwd=repo_root, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    problems = _check(args.date, args.destination, repo_root)
    if problems:
        raise SystemExit("\n".join(problems))
    print(f"DELIVERED date={args.date} destination={args.destination}")


if __name__ == "__main__":
    main()

