---
layout: default
title: "Horizon Summary: 2026-11-23 (ZH)"
date: 2026-11-23
lang: zh
---

> 从 1 条内容中筛选出 1 条重要资讯。

---

**AI 与计算机基础**
1. [解码策略对推理开销的影响](#item-ai-foundations-1) ⭐️ 8.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [解码策略对推理开销的影响](https://machinelearningmastery.com/decoding-policies-in-a-serving-engine/) ⭐️ 8.0/10

该教程讲解了大语言模型（LLM）在服务引擎（以 vLLM 为例）中不同解码策略（如贪心解码、采样、束搜索、停止条件、结构化输出）如何具体影响运行时开销，包括每步 token 的计算量、KV 缓存（Key-Value cache，即模型在自回归生成时缓存的历史注意力键值对，用于避免重复计算）占用、序列状态数量以及批处理效率。它不介绍算法原理，而是聚焦于系统层面的因果关系：例如设置 n=4 会创建 4 个独立输出序列，导致约 4 倍的私有 KV 缓存和 4 倍的解码步数；结构化输出需在每步对 logits 进行动态掩码，增加后处理开销。

rss · Machine Learning Mastery · 11月22日 19:06

**「学习价值」** 读者能掌握将抽象解码参数（如 SamplingParams 中的 temperature、n、top\_p）映射到具体系统资源消耗（GPU 显存、延迟、批处理吞吐）的分析能力，并学会使用 vLLM 的 profiling 功能（如 torch\_profiler）采集真实运行时的算子耗时与内存分配事件。这直接衔接本科生已有的 Python 编程、PyTorch 基础及对 Transformer 和 KV 缓存概念的初步理解。

**「前置知识」** 需理解 Transformer 模型的自回归生成机制、KV 缓存的作用（即为何缓存历史 key/value 可加速后续 token 生成），并能运行基础 PyTorch 代码。若尚未接触过 vLLM 或 GPU 性能分析工具（如 nvidia-smi、PyTorch Profiler），需先完成其官方 Quick Start 教程。

**「实践练习」** 复现文中的 greedy\_params 和 parallel\_samples（n=4）两个配置，在同一台机器上分别运行 show\_output\(\) 并记录输出长度；然后用提供的 benchmark 代码片段测量二者 wall time 和 output tokens per second，对比说明为何 n=4 的请求更慢且单位时间产出 token 更少。

**标签**: `#LLM inference`, `#decoding strategies`, `#KV cache`, `#system performance`, `#practical ML systems`

---