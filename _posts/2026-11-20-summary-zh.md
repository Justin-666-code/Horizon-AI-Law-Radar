---
layout: default
title: "Horizon Summary: 2026-11-20 (ZH)"
date: 2026-11-20
lang: zh
---

> 从 9 条内容中筛选出 6 条重要资讯。

---

**AI 与计算机基础**
1. [信息熵与交叉熵损失可视化](#item-ai-foundations-1) ⭐️ 9.0/10
2. [模型压缩三法：剪枝与蒸馏](#item-ai-foundations-2) ⭐️ 8.0/10

**AI 研究前沿**
1. [LLM 辅助审计临床预测研究代码共享现状](#item-ai-research-1) ⭐️ 8.0/10
2. [数据中心电力需求的远距离空气污染影响](#item-ai-research-2) ⭐️ 8.0/10

**AI 产品工程**
1. [PostgreSQL 19 的 WAIT FOR LSN 实现读写一致性](#item-tech-blog-1) ⭐️ 7.0/10

**AI 产品与产业**
1. [Gemini API 推出工具检索功能（预览版）](#item-tech-news-1) ⭐️ 8.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [信息熵与交叉熵损失可视化](https://machinelearningmastery.com/visualizing-information-entropy-in-language-models/) ⭐️ 9.0/10

该教程用掷骰子类比解释信息熵（衡量概率分布的不确定性，单位为比特），并说明其如何通过交叉熵损失函数指导大语言模型（LLM）训练：模型预测下一个词的概率分布 Q 与真实标签的 one-hot 分布 P 之间的交叉熵 H\(P, Q\) = –∑P\(x\) log₂Q\(x\) 越小，模型越准确且越自信。文中用 Python + Plotly 可视化了三种典型预测（正确且自信、错误但自信、完全不确定），直观展示熵值（Q 自身的不确定性）与损失值（Q 相对于 P 的偏差）的关系。

rss · Machine Learning Mastery · 11月19日 11:00

**「学习价值」** 你能掌握信息熵和交叉熵损失的明确定义、计算方法及语义区别（熵描述模型自身不确定性，交叉熵描述预测与真实标签的差距），并能用 NumPy 手动实现二者计算；这直接支撑你理解 PyTorch 中 torch.nn.CrossEntropyLoss 的行为，以及在训练循环中监控 loss 曲线时背后的信息论含义。

**「先修知识」** 需已学过基础概率（如离散随机变量、概率分布、对数运算）和 Python 编程（能读懂 NumPy 数组操作）；无需深度学习框架或微积分推导能力。

**「动手练习」** 运行文中的 Python 代码，手动计算 &\#x27;Confident &amp; Correct&\#x27; 模型的熵（shannon\_entropy）和交叉熵（cross\_entropy）：用纸笔验证公式 –∑qᵢ log₂qᵢ 和 –∑pᵢ log₂qᵢ 在 vocab=\[&\#x27;apple&\#x27;,&\#x27;banana&\#x27;,&\#x27;cat&\#x27;,&\#x27;dog&\#x27;,&\#x27;elephant&\#x27;\]、P=\[0,0,1,0,0\]、Q=\[0.02,0.03,0.90,0.03,0.02\] 下的结果是否分别约为 0.47 和 0.15（保留两位小数）。

**标签**: `#information-theory`, `#cross-entropy-loss`, `#python-visualization`, `#llm-fundamentals`, `#beginner-friendly`

---

<a id="item-ai-foundations-2"></a>
### [模型压缩三法：剪枝与蒸馏](https://machinelearningmastery.com/model-compression-beyond-quantization/) ⭐️ 8.0/10

本文介绍了三种超越量化（quantization）的模型压缩技术：非结构化剪枝（unstructured pruning）、结构化剪枝（structured pruning）和知识蒸馏（knowledge distillation）。它面向实际部署需求，解释了如何通过移除冗余权重（如按幅值设零）或结构单元（如 MLP 中间通道、注意力头），或让小模型（student）模仿大模型（teacher）的软标签输出（使用带温度 T 的 KL 散度损失），来减小模型体积与计算量。文中所有方法均配 PyTorch 可运行代码，并强调关键约束：稀疏矩阵需硬件支持才加速，结构化剪枝需保持张量形状兼容（如 up\_proj 行数与 down\_proj 列数对齐），蒸馏需 teacher 与 student 共享词表且 logits 维度一致。

rss · Machine Learning Mastery · 11月19日 14:06

**「可掌握技能」** 读者能动手实现三种压缩操作：用 torch.quantile 和布尔掩码完成非结构化剪枝并验证稀疏/稠密乘法等价性；编写函数协调剪除 MLP 中 up/down 投影的对应通道，理解结构化剪枝如何生成更小但稠密的子网络；复现带温度缩放的 KL 散度蒸馏损失函数，并在小型 GPT-2 配置上执行单步联合训练（硬标签交叉熵+软标签 KL 损失）。这些实践直接强化 PyTorch 张量操作、线性层参数访问、softmax/log\_softmax 数值稳定性及损失函数组合等本科二年级已具备的能力。

**「必要基础」** 需熟练使用 PyTorch 构建和操作 nn.Linear 层、访问 weight/bias 属性、执行前向传播与梯度更新；理解 softmax、log\_softmax 和 KL 散度的基本定义与 PyTorch 实现（F.kl\_div）；了解 transformer 中 MLP 模块的两层结构（W\_up → 激活 → W\_down）及其张量维度关系（如 up\_proj.out\_features 必须等于 down\_proj.in\_features）。

**「动手练习」** 运行文中的 shrink\_mlp 函数，将 up=nn.Linear\(16,32\)与 down=nn.Linear\(32,16\)剪枝为 keep\_channels=8，打印 smaller\_up.weight.shape 和 smaller\_down.weight.shape；再手动构造一个输入 x=torch.randn\(1,16\)，验证 smaller\_down\(torch.relu\(smaller\_up\(x\)\)\)的输出形状是否为\(1,16\)，确认结构化剪枝后前向传播的维度一致性。

**标签**: `#model pruning`, `#knowledge distillation`, `#PyTorch implementation`, `#sparse computation`, `#transformer architecture`

---

## AI 研究前沿

<a id="item-ai-research-1"></a>
### [LLM 辅助审计临床预测研究代码共享现状](https://news.mit.edu/2026/ai-helps-researchers-investigate-how-medical-studies-share-code-1119) ⭐️ 8.0/10

该研究针对临床预测模型研究中分析代码共享率低、可复用性差的问题，使用大语言模型（LLM）系统筛查近 4000 篇 PubMed Central 开放获取论文，识别代码共享声明并提取链接，再人工验证数百个关联代码仓库；结果显示仅约 1/8 的研究报告共享代码，且多数仓库缺乏必要文档、许可证或运行说明；研究发现直接支撑了 TRIPOD-Code 报告指南的制定，该指南旨在明确临床预测研究中分析代码应包含的核心要素。

rss · MIT News AI · 11月19日 22:15

**「初学者桥梁」** 临床预测研究（如预测患者得病风险）依赖代码实现数据处理、建模和评估，但若作者不公开或未规范整理代码，其他研究者就无法检验或复现结果。你需要理解「可复现性」的基本概念、GitHub 仓库结构（如 README、requirements.txt、license 文件的作用），以及为什么单纯提供代码链接不等于支持复用。一个现实的入门点是：手动检查一篇已公开代码的临床 AI 论文（如在 PubMed Central 中搜索 TRIPOD+AI 引用论文），对照其 GitHub 仓库，判断是否包含可运行所需的全部要素。

**「方法」** 研究采用人机协同流程：先用 LLM 从近 4000 篇论文中识别代码共享语句并提取 URL，再由软件自动抓取对应 GitHub 等仓库，最后由两名独立人工评审员对 500 篇论文及一批仓库进行双盲评估，重点核查文档完整性、许可证存在性、环境依赖说明等可复用性指标；LLM 被明确定义为处理非结构化文本的辅助工具，所有关键判断（如文档是否充分）均经人工校验，作者强调结果反映的是整体趋势而非精确计数。

**「相关性」** AI 本科生应关注此项工作，因为它实证揭示了当前临床 AI 研究中「代码公开≠可复现」这一关键能力边界，并展示了如何用 LLM 规模化审计真实科研实践——这对设计医疗 AI 产品时评估第三方模型可信度、制定内部代码交付标准具有直接参考价值。

**「局限性」** 作者明确指出，LLM 在判断文档“充分性”等主观维度上一致性较低，因此人工验证聚焦于客观指标（如 license 文件是否存在），而对文档质量的评估保留不确定性；研究未覆盖非开放获取论文或未在论文中提及代码但实际托管于其他平台（如 GitLab、私有仓库）的情形。

**标签**: `#reproducibility`, `#clinical-AI`, `#code-sharing`, `#LLM-augmented-research`, `#reporting-guidelines`

---

<a id="item-ai-research-2"></a>
### [数据中心电力需求的远距离空气污染影响](https://news.mit.edu/2026/study-reveals-data-centers-long-distance-damage-air-quality-1119) ⭐️ 8.0/10

该研究针对数据中心快速扩张引发的跨区域空气污染健康影响问题，构建了耦合电力系统调度、大气化学传输与流行病学归因的建模框架。研究人员使用 2023 年美国电网小时级发电调度数据，结合 CMAQ 等化学传输模型，量化了数据中心用电导致的 PM2.5 和臭氧增量，并据此估算出约 650 例过早死亡（其中 513 例源于 PM2.5，137 例源于臭氧），且高发区域集中于中西部农业州（如爱荷华州、南达科他州），而非数据中心密集的弗吉尼亚州和得克萨斯州。

rss · MIT News AI · 11月19日 14:00

**「初学者桥梁」** 这个问题本质是：数据中心虽建在 A 地，但其用电会迫使 B 地（如俄亥俄河谷）的老燃煤/燃气电厂多发电，而 B 地排放的氮氧化物（NOx）和二氧化硫（SO2）在特定气象与氨气（来自农田施肥）条件下，会在 C 地（如下风向的爱荷华州）生成更多致命的 PM2.5。你需要理解电力系统基本概念（如负荷、发电机响应、区域电网互联）、空气污染物二次生成机制（如 NOx→臭氧、SO2+NH3→PM2.5），以及流行病学中浓度-响应函数（C-R function）如何将 PM2.5 浓度变化映射为健康损失。

**「方法」** 研究采用三阶段实证建模：首先用小时级电力系统模型（基于 EIA 和 FERC 数据）识别对数据中心负荷响应的发电机组及其 NOx/SO2 排放；其次将排放输入化学传输模型（CMAQ）模拟 PM2.5 与臭氧的空间分布变化；最后利用已发表的流行病学浓度-响应系数，将污染增量转化为各州过早死亡人数。所有步骤均基于公开数据与标准模型，结果可复现，且明确区分了建模输出（如 650 例死亡）与作者解读（如政策建议）。

**「相关性」** AI 本科生应关注此工作，因为它首次以可验证的时空分辨率揭示了 AI 算力基础设施的隐性外部性边界：即使不训练大模型，仅部署推理服务所引致的电网负荷变动，即可通过跨区域大气传输造成显著公共健康成本，这对评估 AI 系统全生命周期可持续性构成硬性约束。

**「局限性」** 研究未纳入 onsite 发电（如数据中心自建燃气轮机）或需求侧灵活性（如负载迁移、延迟计算）的影响，作者明确指出这是未来工作方向。

**标签**: `#energy-systems-modeling`, `#air-quality-impact`, `#infrastructure-externalities`, `#epidemiological-translation`, `#grid-aware-compute`

---

## AI 产品工程

<a id="item-tech-blog-1"></a>
### [PostgreSQL 19 的 WAIT FOR LSN 实现读写一致性](https://simonwillison.net/2026/Nov/19/postgresql-19/) ⭐️ 7.0/10

rss · Simon Willison · 11月19日 20:43

**「背景」** 在读写分离架构中，应用将写操作发往主库、读操作发往备库，但备库存在复制延迟，导致用户刚写入的数据无法立即从备库读出（read-after-write 不一致）。MediaWiki 等系统曾需自行实现类似逻辑，依赖 MySQL 的 GTID 等机制手工同步位点，既复杂又易出错。

**「方案」** PostgreSQL 19 引入 WAIT FOR LSN 命令，使备库会话可主动等待指定 WAL 日志序列号（LSN）完成重放后再执行查询。应用在主库执行写操作后调用 pg\_current\_wal\_insert\_lsn\(\) 获取当前 LSN，将其通过安全方式（如签名 Cookie）传回客户端；后续请求在备库上先执行 WAIT FOR LSN &\#x27;0/0306EE20&\#x27; WITH \(TIMEOUT &\#x27;0.1s&\#x27;\)，超时则报错，成功后再执行 SELECT。该机制不改变复制协议，仅在会话层提供轻量级同步语义，且兼容现有连接池与负载均衡策略。

**「启示」** WAIT FOR LSN 并非追求强一致性，而是以可控延迟为代价，在最终一致性系统中为关键用户会话注入局部顺序性——它把一致性责任从全局协议下沉到应用可感知、可控制的会话边界内。

**标签**: `#database-consistency`, `#replication`, `#system-design`, `#postgresql`

---

## AI 产品与产业

<a id="item-tech-news-1"></a>
### [Gemini API 推出工具检索功能（预览版）](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-api-tool-retrieval/) ⭐️ 8.0/10

Google 于 2026 年 11 月 19 日在 Gemini Interactions API 预览版中正式推出 Tool Retrieval（工具检索）功能，支持 Gemini 3.6 及更高版本模型（含全部 Gemini 4 系列）。开发者可通过在工具定义中设置 defer\_loading: true 并添加 type: &quot;tool\_search&quot; 工具，实现参数 schema 的按需加载；该机制不改变现有函数调用流程，所有检索、加载与调用均发生在单次 API 请求内。功能已投入生产使用，无额外计费，输入/输出 token 按标准模型费率结算。

rss · Google AI Blog · 11月19日 18:00

**「背景」** 此前 Gemini API 要求将全部工具的完整参数 schema 随每次请求一并提交，导致大型工具库场景下输入 token 急剧膨胀、推理延迟升高、工具选择准确率下降。这一设计已成为构建多工具 LLM 智能体（agent）的关键工程瓶颈。

**「影响」** 开发者可立即将高频使用工具保持常驻加载、对长尾工具启用 defer\_loading，从而在不重构 agent 架构的前提下降低平均输入 token 消耗并提升工具调用准确率；调试时可通过 interaction.steps 清晰追踪模型的工具搜索与加载过程。

**「社区讨论」** 暂无可用社区评论。

**「对产品工程的价值」** 该功能直接优化了 LLM 智能体的产品集成路径：对于正在基于 Gemini 构建多工具 agent 的二年级本科生开发者，属于可立即采用的 actionable 改进——仅需修改工具声明配置，无需新增服务或索引基础设施。

**标签**: `#LLM-agents`, `#API-optimization`, `#tool-integration`, `#context-management`

---