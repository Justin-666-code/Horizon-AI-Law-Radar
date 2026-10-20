"""
[INPUT]: 依赖基础 Horizon JSON 配置和 radar-preferences.json 声明式偏好
[OUTPUT]: 生成经过一致性检查的 data/config.json
[POS]: scripts 模块的配置编译器，把用户偏好与底层来源配置解耦
[PROTOCOL]: 变更时更新此头部，然后检查 CLAUDE.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


TIERS = {"primary", "secondary"}
POLICIES = {"primary_only", "mixed"}


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_rss(config: dict[str, Any], name: str) -> dict[str, Any]:
    for source in config["sources"].get("rss", []):
        if source.get("name") == name:
            return source
    raise ValueError(f"Unknown RSS source in preferences: {name}")


def _find_github(config: dict[str, Any], repo: str) -> dict[str, Any]:
    try:
        owner, repository = repo.split("/", 1)
    except ValueError as exc:
        raise ValueError(f"Invalid GitHub repo reference: {repo}") from exc
    for source in config["sources"].get("github", []):
        if source.get("owner") == owner and source.get("repo") == repository:
            return source
    raise ValueError(f"Unknown GitHub source in preferences: {repo}")


def _apply_source_group(
    config: dict[str, Any],
    name: str,
    group: dict[str, Any],
    policy: str,
) -> None:
    tier = group.get("tier")
    enabled = group.get("enabled")
    if tier not in TIERS:
        raise ValueError(f"source group {name}: invalid tier {tier!r}")
    if not isinstance(enabled, bool):
        raise ValueError(f"source group {name}: enabled must be boolean")
    if policy == "primary_only" and tier == "secondary" and enabled:
        raise ValueError(
            f"source group {name}: secondary groups must be disabled "
            "when information_policy is primary_only"
        )

    matched = 0
    for rss_name in group.get("rss", []):
        _find_rss(config, rss_name)["enabled"] = enabled
        matched += 1
    for repo in group.get("github", []):
        _find_github(config, repo)["enabled"] = enabled
        matched += 1
    for provider in group.get("providers", []):
        source = config["sources"].get(provider)
        if not isinstance(source, dict):
            raise ValueError(f"Unknown provider source in preferences: {provider}")
        source["enabled"] = enabled
        matched += 1
    if matched == 0:
        raise ValueError(f"source group {name}: no sources configured")


def apply_preferences(
    input_path: Path,
    preferences_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    config = _load_json(input_path)
    preferences = _load_json(preferences_path)

    policy = preferences.get("information_policy")
    if policy not in POLICIES:
        raise ValueError(f"Unknown information_policy: {policy!r}")

    daily_limit = preferences.get("daily_item_limit")
    if not isinstance(daily_limit, int) or daily_limit <= 0:
        raise ValueError("daily_item_limit must be a positive integer")

    profile_order = preferences.get("profile_order")
    if not isinstance(profile_order, list) or not profile_order:
        raise ValueError("profile_order must be a non-empty list")
    if len(profile_order) != len(set(profile_order)):
        raise ValueError("profile_order must not contain duplicates")
    known_profiles = set(config["processing"]["profile_settings"])
    unknown_profiles = set(profile_order) - known_profiles
    if unknown_profiles:
        raise ValueError(
            "profile_order contains unknown profiles: "
            + ", ".join(sorted(unknown_profiles))
        )
    config["digest"]["profile_order"] = profile_order
    config["digest"]["max_items"] = daily_limit

    thresholds = preferences.get("thresholds")
    if not isinstance(thresholds, dict) or not thresholds:
        raise ValueError("thresholds must be a non-empty object")
    settings = config["processing"]["profile_settings"]
    for profile_id, threshold in thresholds.items():
        if profile_id not in settings:
            raise ValueError(f"Unknown profile threshold: {profile_id}")
        if not isinstance(threshold, (int, float)) or not 0 <= threshold <= 10:
            raise ValueError(f"Invalid threshold for {profile_id}: {threshold}")
        settings[profile_id]["threshold"] = threshold

    category_limits = preferences.get("category_limits")
    if not isinstance(category_limits, dict) or not category_limits:
        raise ValueError("category_limits must be a non-empty object")
    groups = config["digest"]["category_groups"]
    for group_id, limit in category_limits.items():
        if not isinstance(limit, int) or limit < 0:
            raise ValueError(f"Invalid category limit for {group_id}: {limit}")
        if group_id == "other":
            config["digest"]["default_group_limit"] = limit or None
            continue
        if group_id not in groups:
            raise ValueError(f"Unknown category group: {group_id}")
        if limit == 0:
            groups.pop(group_id)
        else:
            groups[group_id]["limit"] = limit

    source_groups = preferences.get("source_groups")
    if not isinstance(source_groups, dict) or not source_groups:
        raise ValueError("source_groups must be a non-empty object")
    for name, group in source_groups.items():
        if not isinstance(group, dict):
            raise ValueError(f"source group {name}: expected object")
        _apply_source_group(config, name, group, policy)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return config


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply personal radar preferences to a Horizon config."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/config.github.json"),
    )
    parser.add_argument(
        "--preferences",
        type=Path,
        default=Path("data/radar-preferences.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/config.json"),
    )
    args = parser.parse_args()

    policy = _load_json(args.preferences).get("information_policy")
    config = apply_preferences(args.input, args.preferences, args.output)
    enabled_rss = sum(
        1 for source in config["sources"].get("rss", []) if source.get("enabled")
    )
    print(
        f"Generated {args.output} with {enabled_rss} RSS sources, "
        f"{config['digest']['max_items']} max items, policy {policy}"
    )


if __name__ == "__main__":
    main()

