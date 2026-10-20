# 验证契约

## 自动验证

- `preferences.profile_order` 只包含 `law-governance`，不包含 `career-opportunity`。
- `category_limits.law == 2`，不再存在 opportunity 配额。
- 法律/公共治理 Google News 源启用且 `max_items <= 10`。
- 失效的 USPTO 与 Copyright Office RSS 不存在于默认配置。
- WIPO 和 EU Digital Strategy 保留为官方来源。
- `test_radar_preferences`、`test_personal_radar`、`test_profiles`、`test_rss` 通过。

## 用户流

1. 运行一天日报。
2. 确认融合栏目最多 2 条。
3. 确认内容至少连接 AI/计算机与知识产权、数字政府、政务 AI、司法科技或公共治理中的一个。
4. 确认没有法硕培训广告、选调报名广告或普通犯罪新闻。

