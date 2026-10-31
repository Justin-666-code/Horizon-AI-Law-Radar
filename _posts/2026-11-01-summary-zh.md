---
layout: default
title: "Horizon Summary: 2026-11-01 (ZH)"
date: 2026-11-01
lang: zh
---

> 从 1 条内容中筛选出 1 条重要资讯。

---

**AI 产品工程**
1. [ChatGPT HTML 预览沙箱绕过漏洞分析](#item-tech-blog-1) ⭐️ 9.0/10

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [ChatGPT HTML 预览沙箱绕过漏洞分析](https://simonwillison.net/2026/Oct/31/how-we-took-over-chatgpt-accounts/) ⭐️ 9.0/10

rss · Simon Willison · 10月31日 23:15

**「背景」** ChatGPT 允许用户生成并分享可交互的 HTML 预览（原称 Canvas），为保障安全，这些内容被加载在 sandboxed iframe 中，并受严格 CSP 策略限制。但该设计隐含一个关键矛盾：为支持数学公式输入等功能，主页面需接收来自沙箱 iframe 的 postMessage 消息，而消息处理逻辑直接使用 innerHTML 插入内容，形成未受控的 DOM 注入入口。

**「方案」** 攻击者利用 MathLive 库的虚拟键盘触发机制，向父页面发送恶意 postMessage；其 handler 不校验来源且直接用 innerHTML 渲染消息内容，从而注入无 sandbox 属性的新 iframe；再借助 YouTube oEmbed 接口（CSP 白名单内）反射执行 JavaScript，绕过 CSP 对 inline script 的拦截；最终在 ChatGPT 主域上下文中窃取登录用户的 API 凭据与私有数据。该链式漏洞使任意分享链接可劫持其他已登录用户的会话，OpenAI 后来修复并支付 5000 美元赏金。

**「启示」** 即使采用沙箱 iframe 和 CSP，跨帧通信（如 postMessage）仍构成实质性的特权边界——任何未验证来源、未净化内容的 innerHTML 使用，都可能将隔离失效转化为完整上下文劫持。该案例揭示了富交互产品中安全边界的脆弱性本质：隔离机制的有效性取决于最弱的通信接口，而非最强的容器约束。

**「工程价值」** 该案例锻炼产品工程中的可靠性能力：需系统性识别和审计所有跨帧通信路径及其 DOM 操作副作用。建议在当前阶段对所有 postMessage handler 执行 source.origin 校验与 HTML 内容白名单过滤。

**标签**: `#security`, `#sandboxing`, `#CSP`, `#postMessage`, `#product-tradeoffs`

---