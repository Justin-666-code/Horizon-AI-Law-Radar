---
layout: default
title: "Horizon Summary: 2026-11-02 (ZH)"
date: 2026-11-02
lang: zh
---

> 从 2 条内容中筛选出 1 条重要资讯。

---

**AI 产品工程**
1. [遇到依赖问题时先删除 uv.lock 文件](#item-tech-blog-1) ⭐️ 7.0/10

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [遇到依赖问题时先删除 uv.lock 文件](https://simonwillison.net/2026/Nov/1/delete-uv-lock-first/) ⭐️ 7.0/10

rss · Simon Willison · 11月1日 23:24

**「背景」** 作者在升级到 Python 3.15 后频繁遇到依赖构建失败，典型表现为 PyO3 不支持该新版本（最高仅支持至 3.14），导致 watchfiles==1.1.1 等 Rust 编写的 Python 包无法构建 wheel。

**「方案」** 根本原因在于临时生成的 uv.lock 文件锁定了不兼容 Python 3.15 的旧版依赖（如过时的 PyO3 绑定）；而库项目本不应提交 uv.lock（已加入 .gitignore），故该文件纯属本地缓存。删除 uv.lock 后重新运行 uv run pytest，uv 会基于当前 Python 解释器版本重新解析依赖图并拉取适配 3.15 的最新兼容版本（例如更新后的 PyO3 或其 wheel），从而绕过硬编码的不兼容约束。

**「启示」** uv.lock 的语义是「可重现的本地执行环境」而非「跨版本兼容保证」；当 Python 运行时版本变更时，依赖锁文件可能成为过时的兼容性障碍，而非保障。

**「工程价值」** 这体现了产品工程中「可靠性」能力：识别工具输出（lock 文件）与真实运行约束（Python 版本演进）之间的隐含冲突。建议在 CI 中为新 Python 版本添加「清除 uv.lock 后重解析」的验证步骤。

**标签**: `#dependency-management`, `#python-tooling`, `#debugging-practice`, `#version-compatibility`

---