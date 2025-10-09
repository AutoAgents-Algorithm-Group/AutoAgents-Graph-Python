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

- [Why AutoAgents Graph?](#why-autoagents-graph)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

## Why AutoAgents Graph?

AutoAgents Graph is a revolutionary AI workflow cross-platform engine that allows you to freely convert workflows between different AI platforms through a unified API. It enables seamless navigation through complex AI ecosystems with intelligent workflow orchestration.

- **Zero Learning Curve**: Unified API design - learn once, use everywhere
- **Type Safety**: Complete type validation based on Pydantic, ensuring secure workflow transmission
- **Platform Compatibility**: Supports mainstream platforms like Dify, Agentify, with continuous expansion
- **Intelligent Conversion**: Automatic node type recognition and conversion, with precise workflow translation

## Quick Start

### Prerequisites
- Python 3.11+

### Installation
```bash
pip install autoagents-graph
```

## Examples

AutoAgents Graph provides three main usage patterns:

#### Agentify
```python
import uuid
from autoagents_graph import NL2Workflow, AgentifyConfig
from autoagents_graph.engine.agentify import START
from autoagents_graph.engine.agentify.models import QuestionInputState, InfoClassState, AiChatState, ConfirmReplyState, KnowledgeSearchState


def main():
    workflow = NL2Workflow(
        platform="agentify",
        config=AgentifyConfig(
            personal_auth_key="your_auth_key",
            personal_auth_secret="your_auth_secret",
            base_url="https://uat.agentspro.cn"
        )
    )

    # 用户输入节点
    workflow.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            initialInput=True
        )
    )

    # 信息分类节点
    ad_label_id = str(uuid.uuid1())
    other_label_id = str(uuid.uuid1())
    
    workflow.add_node(
        id="classifier",
        state=InfoClassState(
            model="doubao-deepseek-v3",
            quotePrompt="""请判断用户输入是否与广告相关。

广告相关包括：
- 广告创意、文案、策划
- 广告投放、渠道、效果
- 营销推广、品牌宣传
- 广告设计、制作
- 广告法规、合规问题
- 其他广告行业相关问题

请严格按照JSON格式返回分类结果。""",
            labels={
                ad_label_id: "广告相关",
                other_label_id: "其他问题"
            }
        )
    )

    # 知识库搜索节点
    workflow.add_node(
        id="kb_search",
        state=KnowledgeSearchState(
            datasets=["ad_knowledge_base"],
            similarity=0.2,
            topK=20,
            enableRerank=False
        )
    )

    # 广告问题AI回答节点
    workflow.add_node(
        id="ad_answer",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是一个专业的广告助手，请根据知识库内容回答用户的广告相关问题。

要求：
1. 基于知识库内容提供准确、专业的回答
2. 如果知识库内容不足，请结合广告行业常识补充
3. 回答要具体、实用，有助于解决用户问题
4. 保持专业、友好的语调""",
            temperature=0.1,
            maxToken=3000,
            isvisible=True,
            historyText=3
        )
    )

    # 非广告问题回复节点
    workflow.add_node(
        id="other_reply",
        state=ConfirmReplyState(
            text="抱歉，我只能处理广告相关的问题。如果您有广告创意、投放策略、文案撰写等方面的需求，我很乐意为您提供帮助！",
            isvisible=True
        )
    )

    # 添加连接边
    # 用户输入到分类器
    workflow.add_edge(START, "classifier", "finish", "switchAny")
    workflow.add_edge(START, "classifier", "userChatInput", "text")

    # 广告相关分支：分类器 -> 知识库搜索 -> AI回答
    workflow.add_edge("classifier", "kb_search", ad_label_id, "switchAny")
    workflow.add_edge(START, "kb_search", "userChatInput", "text")
    
    workflow.add_edge("kb_search", "ad_answer", "finish", "switchAny")
    workflow.add_edge(START, "ad_answer", "userChatInput", "text")
    workflow.add_edge("kb_search", "ad_answer", "quoteQA", "knSearch")

    # 其他问题分支：分类器 -> 确定回复
    workflow.add_edge("classifier", "other_reply", other_label_id, "switchAny")

    # 编译工作流
    workflow.compile(
        name="智能广告处理助手",
        intro="专业的广告助手，能够根据用户输入智能分类处理，为广告相关问题提供专业解答",
        category="营销助手",
        prologue="您好！我是您的专业广告助手，可以帮您解答广告创意、投放策略、文案撰写等各类广告相关问题。请告诉我您想了解什么？"
    )
```

#### Dify
```python
from autoagents_graph import NL2Workflow, DifyConfig
from autoagents_graph.engine.dify import DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState, DifyEndState, START, END


def main():
    # 创建Dify平台工作流
    workflow = NL2Workflow(
        platform="dify",
        config=DifyConfig(
            app_name="Dify测试工作流",
            app_description="基于NL2Workflow构建的Dify工作流",
            app_icon="🤖",
            app_icon_background="#FFEAD5"
        )
    )

    # 添加开始节点
    workflow.add_node(
        id=START,
        position={"x": 50, "y": 200},
        state=DifyStartState(title="开始"),
    )

    # 添加LLM节点
    workflow.add_node(
        id="llm_analysis",
        state=DifyLLMState(
            title="智能分析",
            prompt_template=[{"role": "system", "text": "你是一个专业的AI助手，请分析用户的问题。"}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "doubao-deepseek-v3",
                "provider": ""
            }
        ),
        position={"x": 300, "y": 200}
    )

    # 添加知识检索节点
    workflow.add_node(
        id="knowledge",
        state=DifyKnowledgeRetrievalState(
            dataset_ids=["knowledge_base"],
            multiple_retrieval_config={"top_k": 5, "reranking_enable": True}
        ),
        position={"x": 550, "y": 200}
    )

    # 添加AI回复节点
    workflow.add_node(
        id="ai_reply",
        state=DifyLLMState(
            title="智能回复",
            prompt_template=[{"role": "system", "text": "基于检索结果，为用户提供详细回答。"}],
            model={
                "completion_params": {"temperature": 0.8},
                "mode": "chat",
                "name": "doubao-deepseek-v3",
                "provider": ""
            }
        ),
        position={"x": 800, "y": 200}
    )

    # 添加结束节点
    workflow.add_node(
        id=END,
        state=DifyEndState(title="处理完成"),
        position={"x": 1050, "y": 200}
    )

    # 添加连接边
    workflow.add_edge(START, "llm_analysis")
    workflow.add_edge("llm_analysis", "knowledge")
    workflow.add_edge("knowledge", "ai_reply")
    workflow.add_edge("ai_reply", END)

    # 编译并保存
    yaml_result = workflow.compile()
    workflow.save("playground/dify/outputs/dify_workflow_output.yaml")
    
    print(f"Dify工作流测试完成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()
```

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
- **HttpInvokeState** - HTTP request node
- **OfficeWordExportState** - Word document export node
- **MarkdownToWordState** - Markdown to Word conversion node
- **CodeExtractState** - Code extractor node
- **DatabaseQueryState** - Database query node

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