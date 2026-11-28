---
layout: default
title: "Horizon Summary: 2026-11-28 (ZH)"
date: 2026-11-28
lang: zh
---

> 从 2 条内容中筛选出 1 条重要资讯。

---

**AI 与计算机基础**
1. [构建 Proposer-Critic-Judge 验证环](#item-ai-foundations-1) ⭐️ 8.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [构建 Proposer-Critic-Judge 验证环](https://machinelearningmastery.com/building-a-multi-agent-verification-loop-in-python-with-small-open-models/) ⭐️ 8.0/10

该教程教学生如何用单个 4 位量化的开源大语言模型（Qwen2.5-7B-Instruct）在 Python 中实现 Proposer-Critic-Judge 三角色验证环，解决小模型在算术推理任务中易出错的问题。它通过‘角色复用’（persona multiplexing）技术，仅加载一次模型，再动态切换系统提示词（system prompt）来模拟三个不同角色：Proposer 生成初解、Critic 独立推演并比对纠错、Judge 综合输出终解。最终通过测量每步的延迟（latency）和输入/输出 token 数，量化验证环带来的准确率提升与计算开销之间的权衡。

rss · Machine Learning Mastery · 11月27日 11:00

**「可掌握的能力」** 你能学会如何用 Hugging Face Transformers 库对模型进行 4-bit 量化加载，并编写带计时与 token 统计的 prompt 调用函数；还能理解并实践‘角色提示工程’——即通过精心设计的 system prompt 控制同一模型在不同步骤中扮演专业角色，这是 AI 编程与模型评估课程中关键的实操技能。

**「前置知识」** 需已掌握 Python 基础、Hugging Face Transformers 基本用法（如 AutoTokenizer/AutoModelForCausalLM 加载模型），并能在 Google Colab 中启用 GPU 运行时；未接触过 multi-agent 框架（如 LangGraph）亦可直接上手。

**「动手练习」** 在 Colab 中复现文中的完整代码，运行 target\_task（Bob 和 Alice 年龄问题），记录并对比 baseline 单次调用与 verification\_loop 三次调用的 latency 和 total\_tokens 数值；然后修改 CRITIC\_SYS，删去&\#x27;First, independently calculate...&\#x27;等 chain-of-thought 指令，观察 critique 输出是否退化为简单判断，验证提示词对推理行为的直接影响。

**标签**: `#multi-agent patterns`, `#LLM prompting`, `#performance measurement`

---