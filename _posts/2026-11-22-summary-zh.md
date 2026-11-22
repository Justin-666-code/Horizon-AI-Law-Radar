---
layout: default
title: "Horizon Summary: 2026-11-22 (ZH)"
date: 2026-11-22
lang: zh
---

> 从 1 条内容中筛选出 1 条重要资讯。

---

**AI 产品与产业**
1. [Hugging Face Transformers v5.24.0 发布：新增 Inkling 2 Mini 等 9 个模型，统一缓存参数名为 cache](#item-tech-news-1) ⭐️ 7.0/10

---

## AI 产品与产业

<a id="item-tech-news-1"></a>
### [Hugging Face Transformers v5.24.0 发布：新增 Inkling 2 Mini 等 9 个模型，统一缓存参数名为 cache](https://github.com/huggingface/transformers/releases/tag/v5.24.0) ⭐️ 7.0/10

Hugging Face Transformers 库于 2026 年 11 月 21 日正式发布 v5.24.0 版本，新增 Inkling 2 Mini（24 层循环解码器 + MoE，每 token 路由至 8/128 专家）、Apertus 1.5（支持文本/图像/音频输入）、WavTokenizer（40 或 75 token/s 音频编码器）、Dory（NVIDIA 循环语言模型）、HY4-VL（Hunyuan V4 视觉-语言模型）、Omnilingual ASR（覆盖 1600+ 语言的语音识别套件）、Lara Mini（7.2B 参数多语言 MoE 模型）、SarvamMLA（105B 参数 MoE 架构）和 SarvamMoE（30B 参数 MoE 架构）共 9 个新模型；同时将所有模型的缓存参数名统一为 \`cache\`，弃用 \`past\_key\_values\` 和 \`cache\_params\`（保留向后兼容但触发弃用警告）。

github · Cyrilvallez · 11月21日 12:28

**「背景」** Inkling 2 Mini 是 Thinking Machines Lab 推出的轻量级多模态模型，作为 Inkling 2 Small（已在 v5.23.0 中加入）的缩小版本，其核心创新在于采用循环解码器（looped decoder）与细粒度混合专家（MoE）结构，在减少参数量的同时维持性能；该架构通过让第 6–17 层重复执行三次，并在每次循环中注入前次残差信息，实现计算效率与能力的再平衡。

**「影响」** 所有使用 \`past\_key\_values\` 或 \`cache\_params\` 参数名的推理或训练代码在升级到 v5.24.0 后将收到弃用警告，需在后续版本中迁移到 \`cache\`；依赖旧参数名且未处理警告的自动化流水线可能在未来版本中断。

**标签**: `#multimodal-models`, `#model-optimization`, `#huggingface`, `#mixture-of-experts`, `#looped-architectures`

---