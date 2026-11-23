---
layout: default
title: "Horizon Summary: 2026-11-23 (ZH)"
date: 2026-11-23
lang: zh
---

> 从 2 条内容中筛选出 1 条重要资讯。

---

**AI 与计算机基础**
1. [vLLM 解码策略的运行时代价](#item-ai-foundations-1) ⭐️ 8.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [vLLM 解码策略的运行时代价](https://machinelearningmastery.com/decoding-policies-in-a-serving-engine/) ⭐️ 8.0/10

该教程以 vLLM 为实操平台，讲解不同 LLM 解码策略（贪心解码、采样、束搜索、停止条件、结构化输出）对服务引擎实际运行代价的影响，包括每步 token 生成的计算开销、KV 缓存内存占用、请求生命周期长度以及连续批处理（continuous batching）效率。文中明确区分了模型前向计算（transformer forward pass）与解码后处理（如 logit 重缩放、top-k 筛选、重复惩罚、JSON schema 状态机约束）；KV 缓存指模型在自回归生成中为已生成 token 缓存的 Key-Value 张量，其内存占用随活跃序列数和长度线性增长。

rss · Machine Learning Mastery · 11月22日 19:06

**「学习价值」** 读者可掌握如何用 vLLM 的 SamplingParams 配置真实解码行为，并理解参数（如 temperature、n、min\_tokens、max\_tokens）如何影响 GPU 内存占用与端到端延迟；同时能将本科所学的 Python（含 json 模块）、PyTorch 基础（如 tensor 形状、CUDA 同步）应用于轻量级性能观测（如计时、调用 torch.profiler），建立系统视角下的 AI 模型部署直觉。

**「前置知识」** 需已掌握 Python 基础、PyTorch 张量操作与 CUDA 基本概念（如 torch.cuda.synchronize）；了解 LLM 自回归生成流程及 KV 缓存作用。未学过 vLLM 或系统性能分析不构成障碍，因教程从零配置并解释关键术语。

**「实践练习」** 复现文中的 greedy\_params 与 parallel\_samples（n=4）两个配置，在同一台 GPU 机器上分别运行 show\_output\(\)，记录输出 token 数，并使用 time.perf\_counter\(\)测量两次 generate\(\)的端到端耗时；比较二者输出长度是否接近、耗时比是否接近 4 倍，从而验证‘多输出增加序列数而非仅增加采样开销’这一结论。

**标签**: `#LLM inference`, `#decoding strategies`, `#KV cache`, `#vLLM`, `#system-aware ML`

---