---
layout: default
title: "Horizon Summary: 2026-10-26 (ZH)"
date: 2026-10-26
lang: zh
---

> 从 3 条内容中筛选出 1 条重要资讯。

---

**AI 与计算机基础**
1. [JSON 自定义类型序列化](#item-ai-foundations-1) ⭐️ 9.0/10

---

## AI 与计算机基础

<a id="item-ai-foundations-1"></a>
### [JSON 自定义类型序列化](https://machinelearningmastery.com/robust-serialization-with-json-and-custom-types/) ⭐️ 9.0/10

该教程教如何用 Python 标准库 json 模块扩展序列化/反序列化能力，解决 datetime、set、pathlib.Path、Enum 等非原生类型无法直接 JSON 化的实际问题；通过继承 json.JSONEncoder 并重写 default\(\)方法实现自定义编码，通过 json.loads\(\)的 object\_hook 参数实现带类型标记（如\_\_type\_\_）的解码，并加入异常捕获以处理损坏数据；最终构建出支持默认值填充和字段迁移的鲁棒配置加载函数 load\_experiment\_config，适用于 ML 实验元数据管理。

rss · Machine Learning Mastery · 10月26日 11:00

**「可掌握技能」** 你能学会编写可复用的 JSON 编解码器，将 Python 对象与 JSON 字符串双向转换，同时保留原始类型语义；该实践直接强化你对 Python 面向对象（继承、isinstance）、字典操作、异常处理和函数式编程（高阶函数 object\_hook）的理解，并可立即用于课程设计中的模型配置文件读写或实验日志持久化任务。

**「前置知识」** 需熟练使用 Python 基础语法（类定义、字典、异常 try-except）、熟悉 datetime、Enum、pathlib.Path 等标准库类型；了解 JSON 基本格式（键值对、数组、字符串/数字/布尔/空值）即可，无需深度学习或 PyTorch 知识。

**「动手练习」** 复制文中的 RobustEncoder 和 robust\_decoder 代码，在本地 Python 环境运行：先用 json.dumps\(\)序列化一个含 datetime.now\(\)和\{&\#x27;a&\#x27;,&\#x27;b&\#x27;\}的字典，再用 json.loads\(..., object\_hook=robust\_decoder\)反序列化，验证输出中 timestamp 是否为 datetime 类型、features 是否为 set 类型。

**标签**: `#JSON serialization`, `#custom encoding`, `#Python data pipelines`

---