---
layout: default
title: "Horizon Summary: 2026-10-25 (ZH)"
date: 2026-10-25
lang: zh
---

> 从 3 条内容中筛选出 2 条重要资讯。

---

**AI 与计算机基础**
1. [从零实现推理模型](#item-ai-foundations-1) ⭐️ 9.0/10

**科技新闻**
1. [Ollama v0.40.11 发布：新增 macOS 语音合成与 d3 决策模型](#item-tech-news-1) ⭐️ 7.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [从零实现推理模型](https://magazine.sebastianraschka.com/p/building-reasoning-models) ⭐️ 9.0/10

该课程是一套共 8 讲、总计 11 小时的 PyTorch 实践视频，指导初学者在小型预训练模型 Qwen3-0.6B（通义千问 3 的 0.6B 参数版本）基础上，逐步实现四大核心推理增强技术：答案验证器（verifier）、推理时扩展（inference-time scaling，含采样与自一致性）、基于可验证奖励的强化学习（RLVR，使用简化版 GRPO 算法）以及模型蒸馏（distillation）；所有实现均在 MATH-500 数学评测集上进行量化验证，结果可复现、可对比。其中‘可验证奖励’指利用符号/数值等效性自动判定答案正误（如‘2+2=4’与‘4’视为等价），避免人工标注；‘GRPO’是 Group Relative Policy Optimization 的缩写，一种无需价值网络、仅依赖组内相对排序构造优势函数的策略优化方法。

rss · Sebastian Raschka · 10月24日 11:14

**「可掌握的核心能力」** 学习者能亲手构建端到端的 LLM 推理能力增强流水线：从加载 Qwen3 模型、实现 KV 缓存加速生成，到编写数学答案归一化与等价性校验逻辑；并能用 PyTorch 实现采样多样性控制、自一致性投票、log 概率计算、GRPO 损失函数及蒸馏数据准备与监督训练。这些技能直接衔接大二已学的 Python 编程、PyTorch 张量操作、基础概率（如采样与似然）、以及模型评估（如准确率计算）能力。

**「必要前置知识」** 需熟练使用 Python 和 PyTorch（如定义 Module、调用 forward、管理 device 与 autograd）；了解基本概率概念（如采样、log 概率）和神经网络训练流程（loss、optimizer、checkpoint）。课程不依赖《从零构建大语言模型》前作，但若未接触过 Transformer 架构或 tokenization，建议先补足基础。

**「动手练习」** 在 Video 2 代码基础上，修改 greedy decoding 为 temperature=0.7 的 multinomial sampling，对同一 MATH-500 测试题生成 5 个答案，并用 Video 3 中提供的 verifier 提取并比对最终答案字符串（如‘\\boxed\{5\}’→‘5’），统计 5 次中答案一致的比例（self-consistency rate）及整体正确率。

**标签**: `#reasoning models`, `#PyTorch implementation`, `#LLM evaluation`, `#reinforcement learning`, `#model distillation`

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [Ollama v0.40.11 发布：新增 macOS 语音合成与 d3 决策模型](https://github.com/ollama/ollama/releases/tag/v0.40.11) ⭐️ 7.0/10

Ollama v0.40.11 正式发布，为 macOS 平台新增原生语音合成能力，支持通过 \`ollama run\` 实时播放文本或模型回复的音频，并提供 OpenAI 兼容的流式音频 API（\`/v1/audio/speech\`）；同时集成 d3 决策模型家族（含 2B、4B、9B、27B 四种参数规模），支持对文本、结构化状态或图像输入进行分类、二元判断（yes/no）及带概率评分的多选项路由。该版本已于 2026 年 10 月 24 日发布，仅限 macOS 系统启用语音功能，d3 模型需显式调用 \`ollama run d3\` 并传入 \`--ask\` 参数。

github · github-actions\[bot\] · 10月24日 00:30

**「背景」** Ollama 是一个开源的本地大模型运行时工具，此前版本已支持模型拉取、运行和 API 服务；d3 模型源自 vLLM Semantic Router 项目，专为语义路由与结构化决策设计，此前未集成进 Ollama 核心运行时。

**「影响」** macOS 开发者可直接利用 \`ollama run\` 或 \`/v1/audio/speech\` 实现低延迟语音输出，无需额外 TTS 服务；但该语音功能暂不支持 Linux 或 Windows，跨平台应用需做条件适配。

**「社区讨论」** 无可用社区评论。

**标签**: `#artificial-intelligence`, `#machine-learning`, `#open-source`, `#developer-tools`, `#speech-synthesis`

---