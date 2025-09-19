<div align="center">

<img src="https://img.shields.io/badge/-autoagents_graph-000000?style=for-the-badge&labelColor=faf9f6&color=faf9f6&logoColor=000000" alt="AutoAgents Graph Python SDK" width="380"/>

<h4>AI工作流跨平台转换引擎</h4>

[English](README.md) | **简体中文**

<a href="https://pypi.org/project/autoagents-graph">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://img.shields.io/pypi/v/autoagents-graph.svg?style=for-the-badge" />
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/autoagents-graph.svg?style=for-the-badge" />
  </picture>
</a>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="media/dark_license.svg" />
  <img alt="License MIT" src="media/light_license.svg" />
</picture>

</div>

## 目录

- [为什么选择AutoAgents Graph？](#为什么选择autoagents-graph)
- [快速开始](#快速开始)
- [示例](#示例)
- [支持的节点类型](#支持的节点类型)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 为什么选择AutoAgents Graph？

AutoAgents Graph 是一个革命性的AI工作流跨平台转换引擎，让你可以通过统一的API在不同AI平台间自由转换工作流。它通过智能的工作流编排，帮助你在复杂的AI生态系统中无缝穿梭。

- **零学习成本**：统一的API设计，一次学习，处处使用
- **类型安全**：基于Pydantic的完整类型验证，确保工作流安全传递
- **平台兼容**：支持Dify、Agentify等主流平台，持续扩展中
- **智能转换**：节点类型自动识别和转换，实现精准的工作流翻译

## 快速开始

### 系统要求
- Python 3.11+

### 安装
```bash
pip install autoagents-graph
```

## 示例

AutoAgents Graph 提供三种主要使用方式：

#### Text2Workflow - 跨平台转换器
```python
from autoagents_graph import Text2Workflow
from autoagents_graph.dify import DifyStartState, DifyLLMState, DifyEndState, START, END

# 创建Dify平台工作流
workflow = Text2Workflow(
    platform="dify",
    app_name="智能助手"
)

# 添加节点
workflow.add_node(id=START, state=DifyStartState(title="开始"))
workflow.add_node(id="ai", state=DifyLLMState(title="AI回答"))
workflow.add_node(id=END, state=DifyEndState(title="结束"))

# 编译工作流
workflow.compile()
```

#### FlowGraph - Agentify原生构建器
```python
from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.types import QuestionInputState, AiChatState

# 创建Agentify工作流
flow = FlowGraph(
    personal_auth_key="your_key",
    personal_auth_secret="your_secret"
)

# 构建智能对话流程
flow.add_node(START, state=QuestionInputState(inputText=True))
flow.add_node("ai", state=AiChatState(model="doubao-deepseek-v3"))
flow.add_edge(START, "ai")

# 发布到平台
flow.compile(name="智能对话助手")
```

### 支持的节点类型

#### Agentify平台节点
- **QuestionInputState** - 用户输入节点
- **AiChatState** - AI对话节点
- **ConfirmReplyState** - 确认回复节点
- **KnowledgeSearchState** - 知识库搜索节点
- **Pdf2MdState** - 文档解析节点
- **AddMemoryVariableState** - 记忆变量节点
- **InfoClassState** - 信息分类节点
- **CodeFragmentState** - 代码执行节点
- **ForEachState** - 循环迭代节点

#### Dify平台节点
- **DifyStartState** - 开始节点
- **DifyLLMState** - LLM节点
- **DifyKnowledgeRetrievalState** - 知识检索节点
- **DifyEndState** - 结束节点

## 贡献指南

我们欢迎社区贡献！请查看贡献指南了解详细流程。

### 开发流程
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 贡献类型
- Bug修复
- 新功能开发
- 文档改进
- 测试用例
- 平台适配器

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。