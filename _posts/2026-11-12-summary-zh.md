---
layout: default
title: "Horizon Summary: 2026-11-12 (ZH)"
date: 2026-11-12
lang: zh
---

> 从 14 条内容中筛选出 4 条重要资讯。

---

**AI 与计算机基础**
1. [AI 代理代码沙箱的三层实现](#item-ai-foundations-1) ⭐️ 9.0/10

**AI 研究前沿**
1. [用数学验证网络配置](#item-ai-research-1) ⭐️ 8.0/10

**AI 产品工程**
1. [vLLM 中编码器解耦：通过 EPD 扩展多模态服务](#item-tech-blog-1) ⭐️ 9.0/10

**AI 产品与产业**
1. [Gemini Decisions API 发布：基于 gemini-decision-1 模型的低延迟、校准化多模态决策接口](#item-tech-news-1) ⭐️ 8.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [AI 代理代码沙箱的三层实现](https://machinelearningmastery.com/sandboxing-ai-agent-code-execution-in-python-containers-microvms-and-beyond/) ⭐️ 9.0/10

该教程教读者用 Python 实现三种递进式 AI 代理代码执行沙箱：受限子进程（subprocess）、Docker 容器和 Firecracker 微虚拟机（microVM），每种都针对 CPU、内存、进程、文件和网络攻击设置了具体防护措施，并通过统一的 6 个恶意程序测试其安全性，同时用 bench.py 测量各层的延迟开销。它明确指出子进程共享宿主机内核与文件系统，Docker 容器使用 Linux 命名空间和 cgroups 但仍在宿主内核上运行，而 microVM（如 E2B 或 AWS Lambda MicroVM）则为每次执行提供独立内核，构成硬件级隔离边界。文中所有代码可直接运行，且安全策略（如--network none、--read-only、--cap-drop ALL）均以真实 Docker 命令和 Linux 系统调用呈现。

rss · Machine Learning Mastery · 11月11日 11:00

**「学习价值」** 读者能掌握在 Python 中通过 subprocess 模块设置资源限制（如 resource.setrlimit）、使用 Docker CLI 构建安全容器命令、以及将沙箱抽象为统一接口（run\(code\)）的设计模式；这些技能直接建立在大二已学的 Python 进程控制、Linux 基础命令和系统安全常识之上，并为后续课程中理解可信执行环境（TEE）或云原生安全架构打下实操基础。

**「先修知识」** 需熟悉 Linux/WSL 环境下的 Python subprocess 模块、基本 Docker 命令（如 docker run）及环境变量配置；文中明确要求安装 Docker 和 E2B API 密钥，若缺少这些工具则无法复现后两层沙箱。

**「实践任务」** 在 Linux 或 WSL 中，按教程创建 sandbox.py 和 attacks.py，运行 python attacks.py --backend subprocess，观察输出中&\#x27;Fork flood&\#x27;和&\#x27;Read host secret&\#x27;两项是否显示 ALLOWED，并结合源码第 70–75 行解释为何子进程沙箱无法阻止这两个攻击。

**标签**: `#sandboxing`, `#system security`, `#Python subprocess`, `#Docker`, `#microVM`

---

## AI 研究前沿

<a id="item-ai-research-1"></a>
### [用数学验证网络配置](https://www.amazon.science/blog/using-mathematics-to-validate-network-configurations) ⭐️ 8.0/10

该研究针对云网络中大规模、高复杂度的网络分段（segmentation）策略难以通过动态报文采样进行穷尽验证的问题，提出使用 AWS 自研的自动推理工具 Tiros 进行静态形式化验证。其核心思想是将网络配置（如 Cloud WAN 的路由表、附件和策略文档）翻译为逻辑命题，构建网络行为的逻辑模型，并通过求解器证明特定跨段路径的不存在性。在真实部署场景中，Tiros 每小时可对已建模网络执行一次验证，提供数学上可证明的隔离合规性结论。

rss · Amazon Science · 11月11日 17:02

**「初学者桥梁」** 网络分段就是用规则把不同用途的服务器（比如开发环境和线上生产环境）隔开，防止误连或数据泄露；这个问题本质是判断“从 A 资源是否绝对无法到达 B 资源”。你需要理解基本的网络概念（如 VPC、路由、IP 地址段）和逻辑表达（如“如果某 VPC 打上 prod 标签，则它属于生产段”这类条件语句）。一个现实的入门点是：动手用 Tiros 公开示例（如文中 us-east-1/us-west-2 双区域 VPC 分段）复现其输入逻辑模型（含 tag 谓词、附件连接事实）和查询语句（如?reach\(VPC-prod-use1, VPC-dev-use1\)）。

**「方法」** 该工作将 Cloud WAN 配置（路由表、附件、策略文档）经专用软件转换为带条件谓词（如基于 tag 的段归属规则）和无条件谓词（如附件物理连接事实）的逻辑模型；Tiros 作为后端求解器，对用户查询（如‘是否存在从生产 VPC 到开发 VPC 的可达路径’）进行符号执行并返回所有满足赋值；若求解器返回空集，则数学上证明该违规路径不存在。文中明确说明这是静态分析（不发包），且已集成进 VPC Reachability Analyzer 等客户可见服务，属已部署系统而非纯理论提案。

**「相关性」** AI 本科生应关注此工作，因为它展示了形式化方法如何在真实工业系统中解决“不可穷尽测试”的关键能力边界问题——即当系统状态空间远超测试覆盖能力时，静态逻辑验证可提供比任何采样测试更强的确定性保证。

**「局限性」** 原文未声明 Tiros 的建模范围限制（如是否支持所有 Cloud WAN 特性）或求解可扩展性瓶颈；也未报告在超大规模配置下验证耗时或内存占用的具体数据。

**标签**: `#automated reasoning`, `#network security`, `#static analysis`, `#cloud infrastructure`, `#formal verification`

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [vLLM 中编码器解耦：通过 EPD 扩展多模态服务](https://vllm.ai/blog/2026-11-11-encoder-disaggregation-epd) ⭐️ 9.0/10

rss · vLLM Blog · 11月11日 00:00

**「背景」** 多模态推理需先将图像、视频或音频编码为嵌入向量，再交由语言模型处理；但编码负载（取决于媒体尺寸、模态和请求混合）常与预填充/解码负载异步变化，导致 GPU 资源无法独立伸缩。

**「方案」** vLLM 提出 Encoder/Prefill/Decode（EPD）解耦架构，将三阶段拆分为可独立部署的实例：编码器仅执行媒体预处理，不维护 KV 缓存或生成 token；通过元数据-only 请求（如 image\_grid\_thw、video\_grid\_thw、音频特征长度）替代原始媒体转发，使下游精准重建输入布局；远程嵌入经 NIXL（CPU 共享内存）或 Mooncake（RDMA/TCP）传输，且协议强制校验输出形状（如 Qwen3-Omni 视觉宽 8192、音频宽 2048）；跨编码器复用通过 Mooncake Store 实现，本地未命中时查共享存储，实验中 512 张图重编码从 512 次降至 0 次；在 DeepSeek V4.1 Flash 实测中，12-GPU EPD 相较 8-GPU PD 基线，在并发 64–128 时每 GPU 吞吐提升 6.6–9.5%，P90 首 token 延迟降低 44–47%，而编码器加载耗时从 683 秒压缩至 0.31 秒。

**「启示」** 当多模态预处理负载与语言模型计算负载显著偏离时，解耦编码器并非简单拆分服务，而是必须以严格元数据契约、形状感知传输和显式失败隔离为前提，否则会引入静默错误或资源浪费。

**「工程价值」** 该实践锻炼了系统设计中的可靠性与集成能力；建议在本地双 GPU 环境运行 Mooncake EC 集成脚本，验证元数据-only 路径与基线输出一致性。

**标签**: `#multimodal-serving`, `#system-design`, `#performance-optimization`, `#failure-handling`, `#cost-modeling`

---

## AI 产品与产业

<a id="item-tech-news-1"></a>
### [Gemini Decisions API 发布：基于 gemini-decision-1 模型的低延迟、校准化多模态决策接口](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/) ⭐️ 8.0/10

Google 正式发布 Gemini Decisions API，搭载全新专用模型 gemini-decision-1（v1beta），面向封闭式选项决策任务（如工具选择、策略检查、模型路由、上下文评分），支持单次前向传播对最多 1000 个问题并行打分，端到端延迟 150–250 毫秒，输入 token 计费 $0.10/百万，输出 token 零计费；输入支持文本、图像、音频、视频、PDF（最高 256K tokens），且同一 multimodal 输入可复用于三种决策类型（noul/yes-no、choice/multiple choice、score/rubric）；该 API 已在 Google 内部多个产品（Gemini Notebook、Stitch、CC、Search）中投入生产使用。

rss · Google AI Blog · 11月11日 18:00

**「背景」** 此前 Gemini Interactions API 主要面向生成式响应（token-by-token 输出），适用于开放性问答与内容创作；而 Gemini Decisions API 是首个专为确定性、有限选项决策设计的 Gemini 接口，其底层模型 gemini-decision-1 放弃自回归解码，转而采用单次前向传播直接输出概率分布与置信度，属于决策工程（decision engineering）范式的结构性演进。

**「影响」** 对于需高频、低延迟执行封闭式判断的 AI 系统（如智能体路由、安全过滤、UI 反应触发），开发者可将原依赖 Gemini 3.5 Flash-Lite 的生成式提示方案替换为 Decisions API，在共享 multimodal 输入前提下，实现约 5 倍成本下降与 50–100 ms 模型计算延迟降低，且无需处理输出 token 截断、格式错误或非确定性响应问题。

**「社区讨论」** 无可用社区评论。

**「工程路径价值」** 该 API 直接影响 AI 系统架构中的「决策层」设计：当前阶段，掌握其输入结构（Content blocks）、三类 question schema（noul/choice/score）及零输出计费模型，是构建高吞吐、低延迟生产级 AI 控制平面的关键实操技能；建议第二年本科生在课程项目中用 Doorstep Parcels 或 Find the Zoo Keeper 示例快速验证集成流程。

**标签**: `#API design`, `#multimodal reasoning`, `#decision engineering`, `#LLM optimization`, `#AI deployment`

---