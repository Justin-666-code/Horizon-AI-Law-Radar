---
layout: default
title: "Horizon Summary: 2026-11-09 (ZH)"
date: 2026-11-09
lang: zh
---

> 从 2 条内容中筛选出 2 条重要资讯。

---

**AI 产品工程**
1. [SQLite parse\_number\(\) 扩展：C 与 Rust 实现对比](#item-tech-blog-1) ⭐️ 7.0/10
2. [Datasette \#3046：避免向 Firefox 发送 link: rel=next 响应头](#item-tech-blog-2) ⭐️ 7.0/10

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [SQLite parse\_number\(\) 扩展：C 与 Rust 实现对比](https://simonwillison.net/2026/Nov/8/sqlite-parse-number-c-vs-rust/) ⭐️ 7.0/10

rss · Simon Willison · 11月8日 22:26

**「背景」** 作者想为 SQLite 添加一个 parse\_number\(\) 自定义函数，用于从含符号（如 &\#x27;$&\#x27;、&\#x27;%&\#x27;、&\#x27;,&\#x27;）和负号的混乱字符串（如 &\#x27;-$1,234.56&\#x27;）中提取数值，以便后续聚合或排序；现有 SQLite 内置函数无法直接处理此类格式。

**「方案」** 作者用 LLM 生成了 C 和 Rust 两种实现：C 版本仅 14 KB，Rust 版本（基于 rusqlite 或 sqlite-loadable-rs）达 298–321 KB；但初始 Rust 实现更快，主因是其浮点解析（如 from\_str）比 C 的 strtod 快约两倍；随后作者让 LLM 重写 C 版本，自定义高效字符串扫描逻辑，最终在混合数据上将单行解析延迟从 67 ns 降至 19 ns，优于 Rust 各版本（41–46 ns）；测试覆盖整数、小数和混合类型，共 200 万行，单位为纳秒。

**「启示」** 对于轻量级、低延迟的 SQLite 扩展，高度定制的 C 实现可在极小二进制体积下实现最优运行时性能，而 Rust 的优势（如内存安全）在此场景中被启动开销和依赖膨胀部分抵消。

**「产品价值路径」** 该工作主要锻炼「性能评估」能力；下一步可对 parse\_number\(\) 添加鲁棒性测试（如空输入、嵌套符号、科学计数法），验证 LLM 生成代码在边界条件下的行为。

**标签**: `#sqlite`, `#performance`, `#systems-programming`, `#rust`, `#c`

---

<a id="item-tech-blog-2"></a>
### [Datasette \#3046：避免向 Firefox 发送 link: rel=next 响应头](https://simonwillison.net/2026/Nov/7/link-rel-next/) ⭐️ 7.0/10

rss · Simon Willison · 11月7日 23:57

**「背景」** Datasette 在 HTML 页面响应中默认添加 HTTP Link: rel=&quot;next&quot; 头，用于指示下一页数据的 URL；但 Firefox 自 2002 年起会自动预取该链接对应资源，而用户极少实际点击“下一页”，导致服务器无谓渲染完整页面、客户端浪费带宽。

**「方案」** 作者发现该行为源于 Firefox 长期未修复的预取机制（可追溯至 24 年前的 Bug），并确认其在当前版本中仍复现于网络面板；他提出在 Datasette 中增加 User-Agent 检测逻辑，对 Firefox 请求主动省略 rel=&quot;next&quot; 头，其他浏览器（如 Chrome、Safari）则保持原策略不变——此举无需修改客户端，不破坏标准语义，且仅影响明确已知存在副作用的场景。

**「启示」** 一个符合规范的 HTTP 特性（Link 头）在特定浏览器实现中可能引发显著资源浪费，此时产品级工程决策不是弃用标准，而是通过轻量、精准的 UA 条件逻辑隔离异常行为。

**「价值路径」** 该修改属于交付（delivery）能力中的兼容性治理；下一步可为 Datasette 的响应头注入逻辑补充自动化测试，验证不同 User-Agent 下 Link 头的存在性与内容。

**标签**: `#HTTP`, `#performance-optimization`, `#browser-compatibility`, `#web-infrastructure`, `#product-tradeoffs`

---