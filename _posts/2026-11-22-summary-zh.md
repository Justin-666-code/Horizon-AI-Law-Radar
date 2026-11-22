---
layout: default
title: "Horizon Summary: 2026-11-22 (ZH)"
date: 2026-11-22
lang: zh
---

> 从 2 条内容中筛选出 1 条重要资讯。

---

**AI 产品与产业**
1. [Hugging Face transformers v5.24.0 发布：新增 Inkling 2 Mini 等 9 个模型，统一缓存参数名为 cache](#item-tech-news-1) ⭐️ 7.0/10

---

## AI 产品与产业

<a id="item-tech-news-1"></a>
### [Hugging Face transformers v5.24.0 发布：新增 Inkling 2 Mini 等 9 个模型，统一缓存参数名为 cache](https://github.com/huggingface/transformers/releases/tag/v5.24.0) ⭐️ 7.0/10

Hugging Face transformers 库于 2026 年 11 月 21 日正式发布 v5.24.0 版本，新增 Inkling 2 Mini（24 层循环解码器 + MoE，每 token 路由至 8/128 专家）、Apertus 1.5（支持文本/图像/音频输入的多模态模型）、WavTokenizer（40 或 75 token/s 音频编码器）、Dory（NVIDIA 的循环语言模型）、HY4-VL（Hunyuan V4 视觉-语言模型）、Omnilingual ASR（覆盖 1600+ 语言的语音识别套件）、Lara Mini（7.2B 参数多语言 MoE 模型）、SarvamMLA（105B 参数 MoE 架构）和 SarvamMoE（30B 参数 MoE 架构），并统一将 \`past\_key\_values\` 和 \`cache\_params\` 参数名重命名为 \`cache\`（旧名仍可用但触发弃用警告）。

github · Cyrilvallez · 11月21日 12:28

**「背景」** Inkling 2 Mini 是 Thinking Machines Lab 推出的轻量级多模态模型，作为 v5.23.0 中已加入的 Inkling 2 Small 的缩小版本；其核心创新在于采用循环解码器（looped decoder）与细粒度混合专家（MoE）结构，在减少层数（24 层 vs. 48 层）的同时通过层复用维持能力。

**「影响」** 所有使用 transformers 的开发者需在升级到 v5.24.0 后更新代码中对 \`past\_key\_values\` 或 \`cache\_params\` 的显式引用为 \`cache\`，否则将收到弃用警告；依赖 PEFT 的项目还需确保 PEFT 版本 ≥ 对应最小兼容版本，否则缓存传递可能失败。

**标签**: `#multimodal-models`, `#model-optimization`, `#huggingface`, `#mixture-of-experts`, `#looped-architectures`

---