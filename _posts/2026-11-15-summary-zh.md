---
layout: default
title: "Horizon Summary: 2026-11-15 (ZH)"
date: 2026-11-15
lang: zh
---

> 从 3 条内容中筛选出 1 条重要资讯。

---

**AI 与计算机基础**
1. [权重仅量化入门](#item-ai-foundations-1) ⭐️ 8.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [权重仅量化入门](https://machinelearningmastery.com/weight-only-quantization/) ⭐️ 8.0/10

本文介绍了权重仅量化（weight-only quantization）这一模型压缩技术，用于减少大语言模型（LLM）推理时的显存占用和加速计算：它将线性层权重从 FP16/BF16 浮点数转换为 INT8 或 INT4 整数，而保持激活值（activations）仍为高精度浮点；核心方法是不对称仿射量化（asymmetric affine quantization），即用缩放因子（scale）和零点（zero point）将浮点范围线性映射到整数区间（如 uint8 的 0–255），再反向近似重建；文中给出了可运行的 PyTorch 代码实现该映射，并演示了如何用 TorchAO、GPTQ、AWQ 和 GGUF 等工具链完成端到端量化与部署。

rss · Machine Learning Mastery · 11月14日 16:04

**「可掌握技能」** 你能动手实现一个完整的不对称仿射量化-反量化函数，并理解 scale 与 zero point 的数学含义及其对零值表示的影响；你还能复现 TorchAO 对简单 MLP 模型的 INT8 权重量化流程，从而将本科所学的线性代数（矩阵乘法）、Python 编程和 PyTorch 基础（张量操作、nn.Module）直接应用于真实 LLM 优化任务。

**「前置知识」** 需已掌握 Python 基础、PyTorch 张量运算（如 torch.mean、torch.clamp）、线性层前向传播（y = x @ W.T）；了解 FP16/BF16 与 INT8 的基本位宽差异；无需深度学习训练经验，但需知道‘权重’和‘激活值’在神经网络中的角色。

**「动手练习」** 运行文中的 quantize\_asymmetric\(\)和 dequantize\(\)函数，输入 x = torch.tensor\(\[-2.3, -0.2, 0.0, 0.7, 3.1\]\)，记录输出的 scale、zero\_point、量化结果 q 及最大重构误差；再手动验证一个值（如 x\[0\] = -2.3）是否满足公式：round\(-2.3 / scale\) + zero\_point == q\[0\]（注意 clamp 边界）。

**标签**: `#quantization`, `#PyTorch`, `#LLM optimization`, `#post-training compression`, `#undergraduate-applicable`

---