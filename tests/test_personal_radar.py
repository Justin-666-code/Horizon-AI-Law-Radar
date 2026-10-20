"""
[INPUT]: 依赖项目 Config 模型、ProfileRegistry 及个人追踪配置
[OUTPUT]: 验证个人情报源配置、处理画像与来源引用的一致性
[POS]: tests 模块的个人部署契约测试，保护配置漂移
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from pathlib import Path

from src.models import Config
from src.processing.profiles import ProfileRegistry


ROOT = Path(__file__).resolve().parents[1]


def _collect_categories(value):
    if isinstance(value, dict):
        if isinstance(value.get("category"), str):
            yield value["category"]
        for child in value.values():
            yield from _collect_categories(child)
    elif isinstance(value, list):
        for child in value:
            yield from _collect_categories(child)


def test_personal_radar_config_and_profiles_are_consistent():
    config = Config.model_validate_json(
        (ROOT / "data" / "config.github.json").read_text(encoding="utf-8")
    )
    registry = ProfileRegistry.load(
        ROOT / "profiles", config.processing.default_profile
    )

    registry.validate_source_references(config.sources.model_dump(mode="json"))

    assert {
        "ai-foundations",
        "ai-research",
        "law-governance",
        "career-opportunity",
    } <= registry.ids
    assert set(config.processing.profile_settings) <= registry.ids
    assert config.ai.languages == ["zh"]
    assert config.digest.max_items == 10
    assert config.digest.profile_order == [
        "ai-foundations",
        "ai-research",
        "tech-news",
        "tech-blog",
    ]
    assert config.sources.google_news is None
    assert config.email is None
    assert config.webhook is None
    assert config.wechat is None

    source_categories = set(
        _collect_categories(config.sources.model_dump(mode="json"))
    )
    grouped_categories = [
        category
        for group in config.digest.category_groups.values()
        for category in group.categories
    ]
    assert len(grouped_categories) == len(set(grouped_categories))
    assert set(grouped_categories) <= source_categories

