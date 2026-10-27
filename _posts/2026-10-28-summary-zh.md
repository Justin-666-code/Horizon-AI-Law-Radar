---
layout: default
title: "Horizon Summary: 2026-10-28 (ZH)"
date: 2026-10-28
lang: zh
---

> 从 7 条内容中筛选出 3 条重要资讯。

---

**AI 与计算机基础**
1. [Python 上下文管理器进阶应用](#item-ai-foundations-1) ⭐️ 9.0/10

**科技新闻**
1. [Ollama v0.40.12 发布：支持 Liquid AI LFM3 多模态模型家族及 d1-2B 决策模型](#item-tech-news-1) ⭐️ 7.0/10
2. [OpenAI 与 Oracle 扩大合作，将 Oracle 应用集成至 ChatGPT](#item-tech-news-2) ⭐️ 6.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [Python 上下文管理器进阶应用](https://machinelearningmastery.com/context-managers-beyond-opening-files/) ⭐️ 9.0/10

该教程深入讲解 Python 上下文管理器（context manager）的底层协议（\_\_enter\_\_和\_\_exit\_\_方法），并展示其在 AI/ML 工程中的实际用途：如自动计时（Timer）、临时日志级别控制（quiet）、自动清理临时目录（tempfile.TemporaryDirectory）、安全覆盖环境变量（unittest.mock.patch.dict）以及动态管理多个资源（contextlib.ExitStack）。它解决的是机器学习脚本中常见的资源泄漏与错误恢复问题——例如评估脚本因异常中途退出导致临时目录未删除、日志静默、环境变量残留等。关键教训是：with 语句本质是定义一个‘有保障退出边界’，而非仅用于文件操作；\_\_exit\_\_方法返回 False（或 None）才能确保异常正常传播，避免静默失败。

rss · Machine Learning Mastery · 10月27日 11:00

**「可掌握技能」** 你能学会将任意临时状态变更（如修改 os.environ、调整 logging 级别、创建临时路径）封装为可复用、异常安全的上下文管理器，并能根据场景选择最合适的实现方式（类、@contextmanager 装饰器、标准库内置类或 ExitStack）。这直接提升你在 PyTorch/TensorFlow 项目中编写鲁棒数据预处理、模型评估或实验脚本的能力，尤其强化对 Python 异常处理机制和资源生命周期的理解。

**「前置知识」** 需掌握 Python 基础语法（函数、类、异常 try/except）、os 和 logging 标准库的简单使用，以及基本的文件 I/O 操作。无需高级系统编程或并发知识。

**「动手练习」** 仿照文中 Timer 类，编写一个名为 QuietLogger 的上下文管理器类（非@contextmanager），用于临时降低指定 logger 的级别至 WARNING，并在退出时恢复原级别；然后用 with QuietLogger\(&\#x27;transformers&\#x27;\)作为测试，验证其在 evaluate\(\)抛出异常时仍能正确恢复日志级别。

**标签**: `#context managers`, `#resource management`, `#error resilience`, `#Python fundamentals`, `#practical systems programming`

---

## 科技新闻

<a id="item-tech-news-1"></a>
### [Ollama v0.40.12 发布：支持 Liquid AI LFM3 多模态模型家族及 d1-2B 决策模型](https://github.com/ollama/ollama/releases/tag/v0.40.12) ⭐️ 7.0/10

Ollama v0.40.12 正式发布，首次集成 Liquid AI 的 LFM3 模型家族（含文本、视觉、音频模态）和更新的 2B 参数 d1 决策模型，全部专为本地设备代理任务优化。当前仅支持 Apple 硬件（如 M 系列芯片），Linux 和 Windows 平台支持尚未提供。LFM3 系列包括 lfm3（1.7B 参数、256K 上下文）、lfm3-vl（图像理解）、lfm3-audio（18 种语言语音识别/翻译/合成）和 lfm3-omni（统一多模态）；d1:2b 和 d1-omni:2b 支持基于文本、图像及音频的决策任务。该版本还包含对 Gemma 4、Flint、Laguna 在 Apple 硅上的提示处理加速、MLX 上 DFlash2 草稿模型的推测解码支持等改进。

github · github-actions\[bot\] · 10月27日 00:07

**「Liquid AI 的 LFM3 和 d1 模型基础」** Liquid AI 于 2026 年 10 月发布 LFM3 模型家族，作为其 tri-hybrid 架构下的新一代轻量级本地多模态模型，支持文本、视觉和音频处理，并强调结构化输出与设备端智能体任务适配；d1 系列是其配套的决策模型，此前已存在较小参数规模版本，本次更新为基于 LFM3 架构的 2B 参数版本。

**「影响」** Apple 设备用户可立即通过 ollama run 命令本地运行 LFM3 和 d1-2B 模型，但 Linux 和 Windows 用户暂无法使用这些新模型，需等待后续平台支持；开发者若依赖跨平台一致性部署，将面临兼容性限制。

**标签**: `#local-ai`, `#multimodal-models`, `#ollama`, `#agent-systems`, `#open-source-ai`

---

<a id="item-tech-news-2"></a>
### [OpenAI 与 Oracle 扩大合作，将 Oracle 应用集成至 ChatGPT](https://openai.com/index/oracle-apps-in-chatgpt) ⭐️ 6.0/10

OpenAI 与 Oracle 宣布扩大合作伙伴关系，计划将 Oracle 的企业级业务应用（如 ERP、HCM 等）及 Oracle 自研 AI 代理（AI agents）集成至 ChatGPT 用户界面；该集成面向 ChatGPT 企业版（ChatGPT Enterprise）用户，但官方未公布具体上线时间、支持的 Oracle 应用版本、API 接入方式、数据权限模型或实际可用功能范围；当前仅确认为一项合作意向声明，尚无已发布、可验证的集成能力或公开技术文档。

rss · OpenAI News · 10月27日 07:00

**「背景」** OpenAI 与 Oracle 自 2023 年起建立合作关系，最初聚焦于将 Oracle Cloud Infrastructure（OCI）作为 OpenAI 模型训练和推理的云基础设施提供商；此次扩展标志着合作从底层算力支持转向应用层集成。

**标签**: `#AI-integration`, `#enterprise-software`, `#ChatGPT`

---