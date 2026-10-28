---
layout: default
title: "Horizon Summary: 2026-10-29 (ZH)"
date: 2026-10-29
lang: zh
---

> 从 10 条内容中筛选出 5 条重要资讯。

---

**AI 与计算机基础**
1. [冻结嵌入 vs. QLoRA 微调](#item-ai-foundations-1) ⭐️ 8.0/10

**AI 产品工程**
1. [将‘AI 在此无用’视为有效发现](#item-tech-blog-1) ⭐️ 8.0/10
2. [LLM 辅助游戏原型开发的临界点](#item-tech-blog-2) ⭐️ 6.0/10

**AI 产品与产业**
1. [PyTorch v2.15.0 发布：默认启用重写版 NCCL 后端、单边传输与 FSDP2 增强](#item-tech-news-1) ⭐️ 8.0/10
2. [OpenAI 与 ServiceNow 扩展企业工作流合作](#item-tech-news-2) ⭐️ 6.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [冻结嵌入 vs. QLoRA 微调](https://machinelearningmastery.com/fine-tuning-vs-frozen-embeddings-when-to-adapt-the-llm-vs-the-sklearn-head/) ⭐️ 8.0/10

该教程通过在 AG News 数据集上对比两种 LLM 适配策略，说明了何时选择冻结嵌入+scikit-learn 分类器、何时选择 QLoRA 微调：前者将预训练模型（Qwen2.5-1.5B）作为固定特征提取器，用均值池化（mean pooling）提取文本嵌入，再训练随机森林；后者使用 PEFT 库注入低秩适配器（LoRA），仅训练约 1–2%的参数，并采用 4 位量化（nf4）与 bfloat16 计算以节省显存。结果表明，冻结嵌入方案耗时 96.5 秒、准确率 82.0%，QLoRA 方案耗时 300.3 秒、准确率 87.0%，揭示了计算开销与性能提升之间的明确权衡。

rss · Machine Learning Mastery · 10月28日 11:00

**「学习价值」** 读者可掌握如何用 Hugging Face transformers 和 PEFT 实现两种主流轻量级 LLM 适配范式，并理解其底层机制差异：均值池化如何从隐藏状态生成句向量、LoRA 适配器如何插入注意力层（q\_proj/v\_proj）、4 位量化（BitsAndBytesConfig）如何降低显存占用。这些技能直接衔接大二课程中的 PyTorch 张量操作、线性代数（矩阵低秩近似）、以及 scikit-learn 分类器训练流程。

**「先修知识」** 需已掌握 Python 基础、PyTorch 张量运算（如 torch.mean、attention\_mask 加权求和）、scikit-learn 模型拟合（fit/predict）；了解 Transformer 架构基本概念（如 hidden\_states、attention\_mask）和分类任务设置（num\_labels）。未要求掌握 LoRA 数学推导或全参数微调。

**「实践练习」** 在 Colab 中复现文中代码片段，运行冻结嵌入提取函数 extract\_embeddings\(\)，打印 X\_train.shape 和 X\_train.dtype，验证输出是否为形状为\(800, d\)的 float32 NumPy 数组（d 为 Qwen2.5-1.5B 最后隐藏层维度）；再手动计算一行输入文本经 tokenizer 处理后的 attention\_mask 加权均值池化过程，用纸笔或 Python 逐行验证 sum\_embeds / mask.sum 逻辑。

**标签**: `#LLM adaptation`, `#LoRA`, `#feature extraction`

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [将‘AI 在此无用’视为有效发现](https://simonwillison.net/2026/Oct/28/terk-terkowitz/) ⭐️ 8.0/10

rss · Simon Willison · 10月28日 10:09

**「背景」** 当前 AI 工具泛滥，工程师常被默认要求“必须用 AI”，导致盲目集成、掩盖真实问题。当某项工作未从现有 AI 工具中获益时，常被误判为个人能力不足或执行不力，而非系统性信号。

**「方案」** Terk Terkowitz 提出：若 AI 未带来实际增益，这本身就是一个需主动记录、分析并传播的实证发现——要明确写出具体场景、失败表现（如响应延迟超 200ms、准确率低于人工基线）、根本原因（如领域知识未覆盖、输入格式不兼容），并向团队与管理者同步；该过程直接锻炼产品判断力：定义真实用户问题（“AI 是否真降低了任务完成时间？”）、设定可验证接受标准（“需提升 30%效率且 P95 延迟&lt;150ms”）、设计合理回退路径（“自动降级至结构化表单+人工审核”）。

**「启示」** 产品判断力的核心不是决定“用不用 AI”，而是基于可观测证据持续验证“AI 在何处、以何种方式、为谁真正创造价值”，并将负结果转化为可复用的设计约束。

**「价值路径」** 该观点直接支撑产品工程中的‘要求定义’与‘回退设计’能力；建议你在下一次课程项目需求评审中，为每个 AI 功能点同步列出一条‘失效条件’及对应人工流程。

**标签**: `#product-judgment`, `#acceptance-criteria`, `#fallback-design`

---

<a id="item-tech-blog-2"></a>
### [LLM 辅助游戏原型开发的临界点](https://simonwillison.net/2026/Oct/28/vibe-game-development/) ⭐️ 6.0/10

rss · Simon Willison · 10月28日 13:55

**「背景」** 传统游戏开发需整合编程、美术、音效与系统设计，耗时数月甚至数年；而作者发现，2026 年 10 月 Claude Opus 5.5 在 3D 建模（three.js）、音乐生成及关键的游戏机制设计上取得突破——它能响应模糊指令（如“让它超级有趣”）并产出可玩、有情感张力的浏览器游戏，使个人开发者仅用数小时即可完成原型，但该过程缺乏对‘趣味性’的可测定义、可靠性验证或生产级约束考量。

**「方案」** 作者通过四款 HTML/JS 浏览器游戏实证这一能力：Tree Appreciator 单次提示即生成移动友好的 3D 找不同游戏；Emberwick 经多轮迭代构建出带剧情、地形起伏与地下系统的幻想 RPG；Battle Drones 在‘让它更有趣’指令下从平庸 2D 升级为支持 4 人联机、AI 对战与模型库的完整 RTS；Pumpkin Farmer 则以地域文化为锚点，生成含动物角色、季节机制与彩蛋的温馨模拟游戏。所有项目均依赖静态托管（GitHub Pages 等），运行于现代移动浏览器，但未测试跨设备兼容性、长期运行稳定性或 token 成本，也未建立自动化评估 fun 的指标。

**「启示」** LLM 已跨越‘能生成游戏’到‘能生成有趣游戏’的技术临界点，其核心突破在于将游戏设计中不可言传的‘趣味感’转化为可提示、可迭代的工程信号，而非仅复现已有范式。

**「价值路径」** 该实践主要锻炼产品工程中的集成能力——需协调前端框架、模型输出与浏览器环境；建议第二年学生尝试复现 Tree Appreciator，并手动添加一个可量化的趣味性代理指标（如玩家单局平均交互次数）作为首次评估闭环。

**标签**: `#vibe coding`, `#game prototyping`, `#LLM limitations`, `#browser games`, `#AI-assisted development`

---

## AI 产品与产业

<a id="item-tech-news-1"></a>
### [PyTorch v2.15.0 发布：默认启用重写版 NCCL 后端、单边传输与 FSDP2 增强](https://github.com/pytorch/pytorch/releases/tag/v2.15.0) ⭐️ 8.0/10

PyTorch v2.15.0 于 2026 年 10 月 28 日正式发布，将重写后的 NCCL 后端设为分布式训练默认后端（\`backend=&quot;nccl&quot;\`），提供 hang 诊断飞行记录器，并仅在本版本中保留 \`nccl-legacy\` 和 \`TORCH\_DIST\_USE\_NCCL2=0\` 作为临时回退路径；新增支持 CUDA 图捕获的单边传输（NIXL 后端）；FSDP2 引入 fp32 参数精度控制、CUDA 图捕获的梯度累积及计算/通信重叠；同时支持 Blackwell GPU 上的 NVFP4 4-bit 解码加速、Apple Silicon 的 FP8 和 \`grouped\_mm\` 解码优化，以及 ROCm 10.0、CUDA 13.2/13.4 双轮、Python 3.15 上的 \`torch.compile\`。

github · soulitzer · 10月28日 17:09

**「背景」** PyTorch 自 v2.13 起逐步重构分布式通信栈，v2.14 已实验性引入新 NCCL 实现和 FSDP2 迭代；v2.15 是首次将重写 NCCL 设为默认，且明确宣布 \`nccl-legacy\` 将在下一版本移除，标志着旧通信栈生命周期终结。

**「影响」** 使用 \`torch.distributed.init\_process\_group\(backend=&quot;nccl&quot;\)\` 的用户将默认启用新 NCCL，若未显式指定 \`device\_id\` 或跨 GPU 操作张量，将立即触发设备绑定错误（如 \`Expected tensor on cuda:X but found tensor on cuda:Y\`），需检查并修正设备分配逻辑。

**「社区讨论」** 无可用社区评论。

**「工程路线价值」** 对构建大规模分布式训练 pipeline 的 AI 工程师而言，NCCL 默认切换是必须立即验证和适配的变更；FSDP2 的 CUDA 图集成与内存/通信细粒度控制属于高价值可落地优化项，建议在 Blackwell 或 Apple Silicon 硬件上优先评估。

**标签**: `#distributed-training`, `#pytorch`, `#cuda-graphs`, `#fsdp`, `#nccl`

---

<a id="item-tech-news-2"></a>
### [OpenAI 与 ServiceNow 扩展企业工作流合作](https://openai.com/index/openai-servicenow-partnership-expansion) ⭐️ 6.0/10

OpenAI 与 ServiceNow 宣布扩大合作伙伴关系，实现双方平台的双向集成：OpenAI 的模型和智能体将嵌入 ServiceNow 平台，同时 ServiceNow 的工作流能力也将接入 ChatGPT 和 Codex。该合作目前仅以公告形式发布，未披露任何技术细节，包括所用模型版本、部署方式（如 API 调用或私有化部署）、数据驻留策略、延迟要求、安全控制机制，也未说明上线时间、适用客户范围或已验证的生产环境用例。

rss · OpenAI News · 10月28日 13:15

**「合作背景」** OpenAI 与 ServiceNow 于 2023 年首次宣布建立合作伙伴关系，当时聚焦于将 GPT 模型集成至 ServiceNow 的 IT 服务管理（ITSM）和客户服务平台中，以增强自动化响应与知识检索能力。此次扩展声明未提及此前合作的具体技术实现方式或已上线功能，也未说明是否基于该早期集成进行迭代升级。

**「影响」** 企业 IT、HR 和财务团队将能使用基于 OpenAI 模型的 AI 代理，在 ServiceNow 平台中自动执行事件响应、员工入职和发票处理等多步骤任务；开发者需关注 ServiceNow 与 ChatGPT/Codex 的双向集成是否支持自定义 Agent 工作流部署及企业数据隔离策略。

<details><summary>参考链接</summary>
<ul>
<li><a href="https://www.gend.co/blog/openai-servicenow-integration">OpenAI Enhances ServiceNow with AI-Driven Enterprise Tools</a></li>
<li><a href="https://best-ai.org/ai-news/servicenow-openai-the-definitive-guide-to-enterprise-ai-transformation">ServiceNow &amp; OpenAI : The Definitive Guide to Enterprise AI...</a></li>
<li><a href="https://bakas.media/ai/openai-and-servicenow-partner/">OpenAI and ServiceNow Partner to Bring AI Agents to Enterprise ...</a></li>

</ul>
</details>

**标签**: `#enterprise-ai`, `#platform-integration`, `#workflow-automation`

---