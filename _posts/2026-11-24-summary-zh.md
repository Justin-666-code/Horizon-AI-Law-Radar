---
layout: default
title: "Horizon Summary: 2026-11-24 (ZH)"
date: 2026-11-24
lang: zh
---

> 从 25 条内容中筛选出 8 条重要资讯。

---

**AI 与计算机基础**
1. [本地 AI 智能体的工具调用实现](#item-ai-foundations-1) ⭐️ 9.0/10
2. [生产级 Docker 用于 MLOps](#item-ai-foundations-2) ⭐️ 8.0/10

**AI 研究前沿**
1. [Speak When You See It：证据驱动的主动任务辅助](#item-ai-research-1) ⭐️ 9.0/10
2. [TrialAgentBench：临床试验 AI 代理评估基准](#item-ai-research-2) ⭐️ 8.0/10

**AI 产品工程**
1. [Ladybird 浏览器首个 alpha 版发布](#item-tech-blog-1) ⭐️ 7.0/10
2. [vLLM 对 ERNIE 5.5 Flash 的零日插件支持](#item-tech-blog-2) ⭐️ 7.0/10

**AI 产品与产业**
1. [OpenAI 与 Cisco 联合发布开源 Linux 运行时防护系统 Shirudo](#item-tech-news-1) ⭐️ 8.0/10
2. [Ollama 发布 v0.40.18-rc0：Metal 推理性能优化与 JetPack 5 支持移除](#item-tech-news-2) ⭐️ 6.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [本地 AI 智能体的工具调用实现](https://machinelearningmastery.com/how-to-build-tool-calling-local-ai-agents-in-python/) ⭐️ 9.0/10

该教程教你在本地用 Python 构建一个能安全调用文件系统工具（如搜索、读取、记忆）的 AI 智能体，使用 Ollama 运行 Qwen3-4B 模型（支持工具调用），所有代码和数据均不联网。它重点解决大语言模型（LLM）与外部环境交互的典型问题：如何将模型生成的结构化工具请求（tool\_calls）解析为 Python 函数调用，再把结果以 tool 角色消息返回给模型；同时通过限制单次工具输出长度（如最多 160 字符/行、最多 MAX\_RESULTS 条匹配）、路径白名单校验（safe\_path）、上下文轮次裁剪（保留最近 6 轮对话）等手段，确保在有限的 32K token 上下文窗口内稳定运行。最终得到一个可调试、可复现、完全离线的项目助理原型。

rss · Machine Learning Mastery · 11月23日 11:00

**「学习价值」** 你能掌握 AI 智能体最基础但关键的工程能力：将 LLM 的结构化输出（tool\_calls）映射到本地 Python 函数，并设计具备输入校验、错误反馈和输出截断的安全工具接口。这直接衔接你已有的 Python 编程能力（如 pathlib、异常处理、函数参数校验）和系统概念（如文件 I/O、路径安全、内存约束），并为你后续理解 LangChain 或 LlamaIndex 等框架中的 ToolExecutor 模块打下实操基础。

**「前提知识」** 需熟练使用 Python 3.10+（含 pathlib、typing、sys 模块）、理解函数定义与异常处理；了解基本的命令行操作（如 pip 安装、虚拟环境激活）；无需深度学习背景，但需知道“上下文窗口”是模型单次能处理的最大 token 数（类似内存容量）。

**「动手练习」** 在本地创建一个测试目录（如 test\_proj），放入一个 README.md（含文字“model is trained on Python code”）和一个空.py 文件；然后手动执行 search\_files 函数（传入 query=&quot;Python&quot;），验证其是否正确返回形如&quot;README.md:1: model is trained on Python code&quot;的字符串，且长度不超过 160 字符；再尝试传入非法路径（如&quot;../etc/passwd&quot;）验证 safe\_path 是否抛出 ValueError。

**标签**: `#tool calling`, `#local LLM`, `#agent implementation`, `#Python systems programming`, `#beginner-friendly AI`

---

<a id="item-ai-foundations-2"></a>
### [生产级 Docker 用于 MLOps](https://pyimagesearch.com/2026/11/23/production-ready-docker-for-mlops-docker-compose-gpus-and-ollama/) ⭐️ 8.0/10

该教程面向实际部署场景，讲解如何用 Docker Compose 编排多容器 ML 服务（含训练器、FastAPI 推理接口、Redis 缓存和 PostgreSQL 日志数据库），并通过 NVIDIA Container Toolkit 为容器启用 GPU 加速；同时演示了用 Ollama 在 Docker 中运行本地大语言模型（LLM）的轻量方法。它解决的是机器学习模型从本地开发到生产环境部署时常见的镜像臃肿、环境不一致、GPU 不可用和缺乏可观测性等实际问题，最终支撑构建可复现、可扩展、安全的 MLOps 流水线。

rss · PyImageSearch · 11月23日 13:45

**「学习价值」** 你能掌握 Docker Compose 多服务编排的实际技能，包括通过 environment 变量和 depends\_on 连接不同容器（如 API 调用 Redis/Postgres），并理解 GPU 容器化中--gpus all 与 deploy.resources.reservations.devices 的配置差异；这些能力直接衔接你已有的 Python（FastAPI）、PyTorch（模型加载/推理）和基础数据库（psycopg2）经验，是将课程项目升级为可部署服务的关键一步。

**「前置知识」** 需已掌握 Docker 基本命令（docker build/run）、编写简单 Dockerfile、使用 Python 包管理（pip）及运行 FastAPI 应用；若要实践 GPU 部分，还需主机安装 NVIDIA 驱动和 NVIDIA Container Toolkit。

**「动手练习」** 克隆教程代码后，在本地运行 docker compose up -d 启动完整栈（trainer、api、redis、db），然后用 curl 向 http://localhost:8000/predict 上传一张 MNIST 风格的手写数字图片，验证 API 返回预测结果且 Redis 缓存键（prediction:\*）和 Postgres 表 predictions 中均有对应记录。

**标签**: `#Docker Compose`, `#MLOps deployment`, `#GPU containerization`

---

## AI 研究前沿

<a id="item-ai-research-1"></a>
### [Speak When You See It：证据驱动的主动任务辅助](https://arxiv.org/abs/2611.30895v1) ⭐️ 9.0/10

该研究揭示了当前主动任务辅助模型在 egocentric（第一人称视角）基准测试中严重依赖时间线索而非视觉证据这一根本问题：一个完全不看视频、仅按固定时间点（如 25 秒报警、30 秒确认）触发的‘视频盲’计时器，在 Ego-MC-Bench 上达到 0.373 的失误 F1，超过所有已发表模型（最高 0.27）。作者将此定义为‘视频盲前沿’，并提出证据对比训练（Evidence-Contrastive Training, ECT），通过在相同录制视频内、相同经过时间下构造正负样本对，迫使模型区分视觉状态而非时间戳。在 QICD 数据集上仅用 209 个视频、约 15 GPU 小时微调后，一个 2B 参数模型在 QICD 和 Ego-MC-Bench 两个基准上均稳定突破该前沿。

rss · arXiv CS.AI + CS.CL · 11月23日 15:57

**「初学者桥梁」** 主动任务助手需要实时判断用户是否完成某一步骤（如‘切完洋葱’）或是否出错，但很多现有模型其实只是‘看表办事’——靠经验统计的时间规律做决策，而不是真正‘看懂画面’。你需要理解分类任务、F1 分数、微调（fine-tuning）和正负样本对的基本概念；一个现实的入门点是复现 ECT 的核心训练策略：在同一个视频里，取同一时刻的两个帧，一帧对应步骤已完成（正样本），另一帧对应未完成（负样本），强制模型从视觉差异而非时间信息中学习。

**「方法」** 作者提出证据对比训练（ECT）：在 QICD 数据集上，对每个正样本（步骤完成时刻），从同一视频的同一经过时间点采样一个负样本（步骤未完成），使模型无法利用时间线索区分二者；训练目标是让模型基于视觉内容判别状态。实证支持包括：在等时间点判别完成/未完成的准确率达 90–92%（远超指令典型持续时间 65%）、时间戳重缩放后性能基本不变、跨视频替换（同任务不同录制）导致完成准确率下降三分之二——三者共同证明模型决策确实依赖视觉证据而非时间模式。

**「相关性」** AI 本科生应关注此项工作，因为它明确揭示了一个可复现的评估陷阱：当基准测试隐含强时间先验时，‘不看视频’的基线可能超越 SOTA 视觉语言模型，这直接挑战了模型能力评估的有效性，并为设计鲁棒的具身 AI 评估协议提供了可操作的检验标准。

**「局限性」** 论文未报告 ECT 在跨任务泛化（如从厨房任务迁移到维修任务）或长时序复杂步骤链上的表现；所有实验均限于 QICD 与 Ego-MC-Bench 两个特定基准，且未验证其在真实部署延迟约束下的实时性。

**标签**: `#temporal\_grounding`, `#evaluation\_pitfall`, `#contrastive\_learning`, `#embodied\_ai`, `#reproducible\_method`

---

<a id="item-ai-research-2"></a>
### [TrialAgentBench：临床试验 AI 代理评估基准](https://arxiv.org/abs/2611.30916v1) ⭐️ 8.0/10

该研究针对临床药物研发中长期、高风险、多阶段决策缺乏可靠 AI 代理评估方法的问题，提出了 TrialAgentBench——一个基于模拟临床试验的公开基准。其核心是通过虚构药企数据生成近 3500 个任务，覆盖单试验分析到受预算与时间约束的多阶段项目管理，并采用反事实感知评分、置信区间校准和价值导向项目评估进行量化评测。在 24 个闭源与开源模型上测试发现，最强模型对原始试验记录的分析误差仅 3.5%（95%置信区间覆盖真值 94–95%），但其在证据驱动的序贯决策（如何时纠错、采购何种证据）上仍严重受限。

rss · arXiv CS.AI + CS.CL · 11月23日 16:08

**「初学者桥梁」** 临床药物研发需在信息不全、成本高昂的条件下连续做多个关键决策（例如：是否修正数据错误？是否追加某项试验？），而现有 AI 模型能否可靠完成这类‘长周期、不确定环境下的决策’尚无标准检验方式。你需要理解假设检验、置信区间、决策树的基本概念，以及 AI 代理（agent）区别于普通语言模型的关键特征——即能规划、调用工具、迭代行动。一个现实的入门点是复现该基准中单试验分析子任务（如从模拟 CSV 中识别偏倚并估计治疗效应），使用 Hugging Face 提供的轻量模型和公开任务脚本。

**「方法」** TrialAgentBench 构建了一个结构化模拟环境，其中每个任务对应虚构药企的真实数据记录（含已知真值），支持从单次统计分析到跨三期项目的资源分配决策；评估采用双重验证：分析类任务通过重运行生成代码验证结果稳健性，项目类任务以最终实现的净现值（NPV）作为价值得分。实证证据来自 24 个模型在统一任务集上的系统评测，报告了精确数值（如 83%不必要的纠错）、95%置信区间覆盖率（94–95%）及与规则基线/Oracle 的价值比（48% vs. 58% vs. 100%），所有结果均基于可复现的模拟轨迹而非主观判断。

**「相关性」** AI 本科生应关注该工作揭示的明确能力边界：当前最强模型可胜任静态数据分析（误差&lt;4%），但在需权衡成本与信息增益的序贯决策中仍系统性失败（如 83%过度纠错），这直接关系到 AI 代理能否被部署于真实药物研发流程中的可行性判断。

**「局限性」** 该基准依赖模拟环境，虽控制了反事实真实性，但未验证模型在真实临床数据分布偏移或非结构化医生笔记等复杂输入下的鲁棒性；作者亦指出，模型在证据获取策略（如选择哪类试验补充数据）上的表现尚未建立可解释的归因机制。

**标签**: `#clinical-ai`, `#agent-benchmarking`, `#decision-under-uncertainty`, `#simulation-based-evaluation`, `#long-horizon-reasoning`

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [Ladybird 浏览器首个 alpha 版发布](https://simonwillison.net/2026/Nov/23/ladybird/) ⭐️ 7.0/10

rss · Simon Willison · 11月23日 21:46

**「背景」** 2026 年，Ladybird 项目启动了一个极具雄心的全新浏览器工程：从 HTML 解析、CSS 引擎、布局、JavaScript 到 WebAssembly，几乎全部自研（仅复用 HarfBuzz、Skia 等少数成熟组件）。其目标是打破 Chromium/Blink 主导的停滞格局，但作为全新实现，它在标准兼容性、安全性和稳定性上面临严峻挑战——尤其在服务工作者、复杂 WebAssembly 应用等前沿场景中暴露明显缺口。

**「方案」** 首个 alpha 版通过进程隔离（如 WebContent 多进程）和轻量 UI 实现了可用性基础；实测中成功运行 ffmpeg 和 Pyodide 编译的 WebAssembly 工具，但 Datasette Lite 因缺失 navigator.serviceWorker.startMessages 而失败，源码中已标记 FIXME。关键突破来自 AI 辅助开发：10 月下旬五天内，AI 编码代理集中修复 CSS 和编辑模块，推动 Web Platform Tests 通过数激增 75,650 项（达约 218 万子测试），WASM 性能提升 7 倍；其 Rust 化 LibJS 引擎也由 Claude Code 和 Codex 在两周内完成迁移。作者强调，该 alpha 定位明确：非日常主浏览器，而是供匿名浏览与安全研究的实验性入口。

**「启示」** Ladybird 的 alpha 不是功能完备的成品，而是以可控范围暴露真实缺陷、用 AI 加速标准对齐、并借透明崩溃反馈闭环驱动演进的技术验证体——它证明，在浏览器这种极端复杂的系统中，‘可用性’可先于‘完备性’被工程化定义和交付。

**「价值路径」** 它锻炼的是产品工程中的‘评估’能力：如何在无成熟基线时定义 alpha 阶段的验收信号（如 WPT 通过率跃升、特定 WASM 场景通过、崩溃可复现可上报）。下一步可尝试复现 Datasette Lite 失败并提交最小化复现用例。

**标签**: `#browser-engine`, `#web-platform-tests`, `#wasm`, `#ai-assisted-development`, `#product-readiness`

---

<a id="item-tech-blog-2"></a>
### [vLLM 对 ERNIE 5.5 Flash 的零日插件支持](https://vllm.ai/blog/2026-11-24-ernie-5-5-flash-preview) ⭐️ 7.0/10

rss · vLLM Blog · 11月24日 00:00

**「背景」** ERNIE 5.5 Flash 是一个 280B 参数的稀疏 MoE 模型，每 token 仅激活 14B 参数，但需支持 100 万 token 上下文——这使传统推理框架在计算、内存带宽和调度开销上迅速成为瓶颈。vLLM 原生不支持其新型注意力结构（如 HCA、MLA-DSA）、Multi-Router Latent MoE 及 VHA 等定制模块，若采用逐算子实现，中间张量频繁往返显存将严重拖慢吞吐。

**「方案」** 作者通过 vLLM 插件架构实现零日支持：不修改 vLLM 主干，仅安装独立插件包即可启用全部优化。核心是四层协同加速——（1）为 VHA、Multi-Router MoE 等新结构设计专用融合内核，将多步计算压缩为单次 GPU kernel 调用，提速 1.55×–6.53×；（2）引入 FlashIndexer 轻量路由器，在索引阶段动态筛选头部，配合阈值预过滤，使 1M 上下文下的 prefill 提速 40%；（3）对路由专家采用 MXFP4（W4A8）量化感知训练（QAT），确保推理无损且免校准；（4）集成 3 层 DSpark 草稿模型，经多阶段蒸馏训练后实测平均接受长度＞4.0，显著提升长程 Agent 任务的解码效率。

**「启示」** 当模型架构创新（如稀疏 MoE+长上下文+多阶段推理）超出通用框架能力边界时，可借助插件化内核融合+轻量可训练组件+量化感知协同设计，在不牺牲数值精度与系统兼容性的前提下，将端到端推理延迟压至工程可行区间。

**「工程价值」** 该工作主要锻炼产品工程中的集成能力：它验证了如何将高度定制的模型组件（如 FlashIndexer、DSpark）以低侵入方式接入标准推理栈。下一步可尝试复现其 vLLM 插件注册机制，用最小代码加载一个自定义 MoE 层。

**标签**: `#inference-optimization`, `#mixture-of-experts`, `#speculative-decoding`, `#quantization`, `#plugin-architecture`

---

## AI 产品与产业

<a id="item-tech-news-1"></a>
### [OpenAI 与 Cisco 联合发布开源 Linux 运行时防护系统 Shirudo](https://openai.com/index/introducing-shirudo) ⭐️ 8.0/10

OpenAI 与 Cisco 于 2026 年 11 月 23 日联合发布开源项目 Shirudo，这是一个基于 eBPF 的 Linux 运行时防护系统，可针对 Java4Shell 等零日漏洞生成并部署 AI 生成的‘防护盾’（shield），在不重启服务、无需等待补丁的情况下实时阻断攻击。Shirudo 已通过受控测试验证：Codex 生成的 eBPF shield 成功拦截对运行中 Elasticsearch 服务的 Java4Shell 利用，同时保持服务可用；其 shield 经加密签名、内核 eBPF 验证器检查，并支持 TPM 硬件级加载记录。项目采用 BSD 2-Clause 主许可证，eBPF 程序额外兼容 GPL。

rss · OpenAI News · 11月23日 21:20

**「背景」** eBPF（extended Berkeley Packet Filter）是 Linux 内核自 3.18 版本起支持的轻量级沙箱化运行时技术，允许在不修改内核源码的前提下，在内核关键路径（如系统调用、网络栈）注入安全监控与干预逻辑；此前已有 Cilium、Tracee 等项目利用 eBPF 实现运行时检测，但 Shirudo 首次将 AI 驱动的 shield 自动生成、策略化验证与硬件可信执行链（TPM attestation）深度集成。

**「影响」** Linux 基础设施工程师现在可在补丁发布前数小时至数天内，使用 Shirudo 快速部署经验证的临时防护 shield，显著缩短 Java4Shell 类高危漏洞的暴露窗口；但需注意其依赖较新内核（≥5.8）及启用 eBPF 支持，且 shield 有效性高度依赖 AI 生成逻辑的精确性，实际生产环境需严格验证输入过滤规则是否误伤合法流量。

**「社区讨论」** 暂无可用社区评论。

**「工程价值路径」** 对正在构建云原生 Linux 服务或负责 SRE/SecOps 的本科生而言，Shirudo 是学习 eBPF 安全编程、AI 辅助防御建模和可信执行链集成的实操范例；当前应立即动手运行 VM 快速启动指南并复现 Java4Shell shield 案例，属于可直接上手的技能强化项。

**标签**: `#runtime security`, `#Linux`, `#zero-day mitigation`, `#AI security`, `#open-source`

---

<a id="item-tech-news-2"></a>
### [Ollama 发布 v0.40.18-rc0：Metal 推理性能优化与 JetPack 5 支持移除](https://github.com/ollama/ollama/releases/tag/v0.40.18-rc0) ⭐️ 6.0/10

Ollama 于 2026 年 11 月 24 日发布 v0.40.18-rc0 发布候选版本，面向 macOS（Apple Silicon）用户显著提升 Metal 后端推理性能：Inkling2 模型的 decode、prefill 和 draft 阶段速度加快，MLX 后端新增残差混合融合（residual mixing fusion），并统一 tensor 辅助函数与模型初始化逻辑；同时将 llama.cpp 升级至 commit b12651，并正式移除对 NVIDIA JetPack 5 的支持。该版本尚未发布正式版，仅作为 RC 提供测试，不兼容已弃用的 JetPack 5 环境。

github · github-actions\[bot\] · 11月24日 04:18

**「背景」** Ollama 是一个用于本地运行大型语言模型（LLM）的开源工具，其 MLX 后端专为 Apple Silicon（Metal）优化，Inkling2 是其内部开发的轻量级推理引擎；JetPack 5 是 NVIDIA 为嵌入式设备（如 Jetson）提供的旧版软件栈，已于 2024 年停止主流支持。

**「影响」** 使用 Apple Silicon Mac 运行 Inkling2 或 MLX 后端模型的开发者将观察到更短的 token 生成延迟（尤其在 draft 模式下），但依赖 JetPack 5 的边缘部署场景将无法升级至该版本，需迁移至 JetPack 6 或改用 llama.cpp 其他后端。

**「社区讨论」** 无可用社区评论。

**「工程路径价值」** 对于聚焦 macOS 本地 LLM 应用开发的本科生，该版本提供了可实测的 Metal 性能改进点（如 prefill 加速），属于当前阶段可动手验证的优化项；JetPack 5 移除则提醒需关注嵌入式 AI 工具链的版本生命周期管理。

**标签**: `#local-inference`, `#apple-silicon`, `#ollama`, `#performance-optimization`, `#llm-deployment`

---