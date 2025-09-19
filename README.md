<div align="center">

<img src="https://img.shields.io/badge/-autoagents_graph-000000?style=for-the-badge&labelColor=faf9f6&color=faf9f6&logoColor=000000" alt="AutoAgents Graph Python SDK" width="380"/>

<h4>The AI Workflow Cross-Platform Engine</h4>

**English** | [简体中文](README-CN.md)

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

## Table of Contents

- [Why Choose AutoAgents Graph?](#why-choose-autoagents-graph)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Why Choose AutoAgents Graph?

AutoAgents Graph is a revolutionary AI workflow cross-platform engine that allows you to freely convert workflows between different AI platforms through a unified API. It enables seamless navigation through complex AI ecosystems with intelligent workflow orchestration.

- **Zero Learning Curve**: Unified API design - learn once, use everywhere
- **Type Safety**: Complete type validation based on Pydantic, ensuring secure workflow transmission
- **Platform Compatibility**: Supports mainstream platforms like Dify, Agentify, with continuous expansion
- **Intelligent Conversion**: Automatic node type recognition and conversion, with precise workflow translation

## Quick Start

### System Requirements
- Python 3.11+
- pip or poetry

### Installation & Setup

```bash
# Install from PyPI
pip install autoagents-graph

# Quick experience
python -c "
from autoagents_graph import Text2Workflow
from autoagents_graph.dify import DifyStartState, DifyLLMState, DifyEndState, START, END

# Create a simple Dify workflow
workflow = Text2Workflow(platform='dify', app_name='Test Workflow')
workflow.add_node(START, state=DifyStartState(title='Start'))
workflow.add_node(END, state=DifyEndState(title='End'))
workflow.add_edge(START, END)
print(workflow.compile())
"
```

### Basic Usage

AutoAgents Graph provides three main usage patterns:

#### Text2Workflow - Cross-Platform Converter
```python
from autoagents_graph import Text2Workflow
from autoagents_graph.dify import DifyStartState, DifyLLMState, DifyEndState, START, END

# Create Dify platform workflow
workflow = Text2Workflow(
    platform="dify",
    app_name="Smart Assistant"
)

# Add nodes
workflow.add_node(id=START, state=DifyStartState(title="Start"))
workflow.add_node(id="ai", state=DifyLLMState(title="AI Response"))
workflow.add_node(id=END, state=DifyEndState(title="End"))

# Compile workflow
workflow.compile()
```

#### FlowGraph - Agentify Native Builder
```python
from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.types import QuestionInputState, AiChatState

# Create Agentify workflow
flow = FlowGraph(
    personal_auth_key="your_key",
    personal_auth_secret="your_secret"
)

# Build intelligent conversation flow
flow.add_node(START, state=QuestionInputState(inputText=True))
flow.add_node("ai", state=AiChatState(model="doubao-deepseek-v3"))
flow.add_edge(START, "ai")

# Publish to platform
flow.compile(name="Smart Chat Assistant")
```


## Architecture

### Core Components

```
autoagents-graph/
├── src/                        # Core source code
│   ├── autoagents-graph/       # Main package
│   │   ├── agentify/          # Agentify platform engine
│   │   │   ├── FlowGraph.py   # Workflow graph builder
│   │   │   ├── NodeRegistry.py# Node registry
│   │   │   └── types/         # Node type definitions
│   │   ├── dify/              # Dify platform adapter
│   │   │   ├── DifyGraph.py   # Dify workflow builder
│   │   │   └── DifyTypes.py   # Dify node types
│   │   └── Text2Workflow.py   # Cross-platform converter
└── playground/                 # Examples and tests
    ├── agentify/              # Agentify platform examples
    ├── dify/                  # Dify platform examples
    └── text2workflow/         # Cross-platform examples
```

### Design Philosophy

- **Unified Abstraction**: Workflows from different platforms unified as node-edge graph models
- **Intelligent Adaptation**: Automatic node type recognition and cross-platform conversion
- **Modular Design**: Each platform independently implemented for easy extension and maintenance
- **Type Safety**: Complete type system ensuring compile-time error detection

### Supported Node Types

#### Agentify Platform Nodes
- **QuestionInputState** - User input node
- **AiChatState** - AI conversation node
- **ConfirmReplyState** - Confirmation reply node
- **KnowledgeSearchState** - Knowledge base search node
- **Pdf2MdState** - Document parsing node
- **AddMemoryVariableState** - Memory variable node
- **InfoClassState** - Information classification node
- **CodeFragmentState** - Code execution node
- **ForEachState** - Loop iteration node

#### Dify Platform Nodes
- **DifyStartState** - Start node
- **DifyLLMState** - LLM node
- **DifyKnowledgeRetrievalState** - Knowledge retrieval node
- **DifyEndState** - End node

## Contributing

We welcome community contributions! Please check the contribution guidelines for detailed processes.

### Development Workflow
1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Contribution Types
- Bug fixes
- New feature development
- Documentation improvements
- Test cases
- Platform adapters

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

If you have any questions or suggestions, please contact us through [Issues](https://github.com/forhheart/autoagents-graph/issues).