---
name: horizon-daily-delivery
description: Deliver or diagnose the daily Horizon Chinese briefing from GitHub Actions to the local news-radar knowledge base and WeChat. Use for daily sync, missed delivery recovery, or WeChat resend; do not use it to redesign Horizon sources or profiles.
---

# Horizon Daily Delivery

Run this skill for the recurring daily delivery of Horizon's `zh` briefing:

- Source of truth: `C:\Users\16339\Documents\Codex\2026-10-20\ai-https-github-com-thysrael-horizon\outputs\horizon-student-radar`
- Knowledge destination: `D:\知识库\knowledge1\00_资源库\03_新闻雷达`
- Date basis: `Asia/Shanghai`
- Delivery: one compact WeChat message plus the full Markdown file

## Do not repeat setup work

Do not re-audit sources, profiles, thresholds, or the previous day's implementation. This skill assumes the radar is already configured and validated. Only diagnose those layers when the user explicitly asks for a content-quality change.

Do not regenerate the briefing merely because the local file is absent. First determine whether GitHub Actions is pending, successful with a date mismatch, or failed.

## Standard run

Run the deterministic helper:

```powershell
$projectRoot = "C:\Users\16339\Documents\Codex\2026-10-20\ai-https-github-com-thysrael-horizon"
& "$projectRoot\work\Horizon-main\.venv\Scripts\python.exe" `
  "$projectRoot\outputs\horizon-student-radar\scripts\skills\horizon-daily-delivery\scripts\run_daily_delivery.py" `
  --wait-minutes 90 `
  --mode compact
```

It performs all of the following:

1. Computes today's date in `Asia/Shanghai`.
2. Invokes `scripts/Sync-Horizon-Daily.ps1` with the canonical destination, compact WeChat delivery, and the configured wait window.
3. Verifies the Markdown file exists and is larger than 500 bytes.
4. Verifies `work/state/wechat-delivered.json` records today's date with at least one delivered chunk.

Use `--check-only` for a no-side-effect state check. Use `--date YYYY-MM-DD` only when recovering a specific past briefing.

## Failure handling

### No local file after the wait

Inspect Actions without rerunning the radar:

```powershell
gh run list --repo Justin-666-code/Horizon-AI-Law-Radar --workflow daily-summary.yml --limit 3
gh run view <run-id> --repo Justin-666-code/Horizon-AI-Law-Radar --log
```

If Actions wrote the prior UTC date, verify that `HORIZON_TIMEZONE=Asia/Shanghai` is present and that `_summary_date` uses `HORIZON_TIMEZONE`, not UTC.

### WeChat reply budget exhausted

Treat `-2` or `0/10` as an iLink budget exhaustion, not a content failure. Ask the user to send any message to the bot. Poll:

```powershell
python -m src.services.wechat_cli status --refresh
```

After the context refreshes, rerun only the WeChat sender; do not regenerate the briefing.

### Sandbox denies network

If GitHub or WeChat sockets are denied, stop and report the exact blocked operation. Do not create duplicate files, fabricate delivery state, or repeatedly retry the same restricted process. Run the project-level `Run-Horizon-Daily.cmd` outside the Codex sandbox, or start a Codex session with network permission.

## Safety invariants

- Never print or commit `data/wechat_session.json`, bot tokens, user IDs, API keys, or QR contents.
- Keep the full Markdown in the knowledge base; WeChat compact mode sends one overview message with the Pages link.
- Preserve idempotence by date and content hash.
- Do not modify `data/radar-preferences.json` during a delivery task.

