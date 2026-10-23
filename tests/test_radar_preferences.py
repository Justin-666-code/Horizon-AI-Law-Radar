"""
[INPUT]: 依赖偏好生成器、基础配置、偏好文件和 Horizon Config 模型
[OUTPUT]: 验证一手优先策略、阈值、配额和来源启停的生成契约
[POS]: tests 模块的配置编译器测试，保护用户可编辑偏好
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from src.models import Config


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "apply_radar_preferences.py"
SPEC = importlib.util.spec_from_file_location("apply_radar_preferences", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def _preferences() -> dict:
    return json.loads(
        (ROOT / "data" / "radar-preferences.json").read_text(encoding="utf-8")
    )


def test_generates_primary_ai_foundations_config(tmp_path) -> None:
    output = tmp_path / "config.json"
    MODULE.apply_preferences(
        ROOT / "data" / "config.github.json",
        ROOT / "data" / "radar-preferences.json",
        output,
    )

    config = Config.model_validate_json(output.read_text(encoding="utf-8"))

    assert config.digest.max_items == 10
    assert config.collection.time_window_hours == 24
    assert config.digest.profile_order == [
        "ai-foundations",
        "ai-research",
        "tech-news",
        "tech-blog",
        "law-governance",
    ]
    assert config.processing.profile_settings["ai-foundations"].threshold == 5.0
    assert config.processing.profile_settings["law-governance"].threshold == 4.5
    assert config.sources.hackernews.enabled is False
    assert config.sources.reddit.enabled is False
    assert config.sources.telegram.enabled is False
    assert config.sources.ossinsight.enabled is False
    google_sources = {
        source.name: source.enabled
        for source in config.sources.rss
        if source.name.startswith("Google News")
    }
    assert google_sources["Google News - 中文 AI 前沿"] is False
    assert google_sources["Google News - AI法律治理与数字政府"] is True
    assert "Google News - 法律硕士招生" not in google_sources
    assert "Google News - 选调与公务员" not in google_sources
    assert any(
        source.name == "WIPO Press Releases" and source.enabled
        for source in config.sources.rss
    )
    assert config.digest.category_groups["foundations"].limit == 3
    assert config.digest.category_groups["research"].limit == 2
    assert config.digest.category_groups["law"].limit == 2
    assert "opportunity" not in config.digest.category_groups


def test_primary_only_rejects_enabled_secondary_group(tmp_path) -> None:
    preferences = _preferences()
    preferences["information_policy"] = "primary_only"
    preferences["source_groups"]["community_discovery"]["enabled"] = True
    preferences_path = tmp_path / "preferences.json"
    preferences_path.write_text(
        json.dumps(preferences, ensure_ascii=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="secondary groups must be disabled"):
        MODULE.apply_preferences(
            ROOT / "data" / "config.github.json",
            preferences_path,
            tmp_path / "config.json",
        )


def test_rejects_unknown_source(tmp_path) -> None:
    preferences = _preferences()
    preferences["source_groups"]["primary_ai"]["rss"].append("Missing Feed")
    preferences_path = tmp_path / "preferences.json"
    preferences_path.write_text(
        json.dumps(preferences, ensure_ascii=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unknown RSS source"):
        MODULE.apply_preferences(
            ROOT / "data" / "config.github.json",
            preferences_path,
            tmp_path / "config.json",
        )


def test_rejects_unknown_profile_in_order(tmp_path) -> None:
    preferences = _preferences()
    preferences["profile_order"].append("missing-profile")
    preferences_path = tmp_path / "preferences.json"
    preferences_path.write_text(
        json.dumps(preferences, ensure_ascii=False),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="profile_order contains unknown profiles"):
        MODULE.apply_preferences(
            ROOT / "data" / "config.github.json",
            preferences_path,
            tmp_path / "config.json",
        )

