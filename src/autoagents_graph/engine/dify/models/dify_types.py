from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DifyNode(BaseModel):
    """Dify节点模型"""
    id: str
    type: str = "custom"
    position: Dict[str, float]
    positionAbsolute: Optional[Dict[str, float]] = None
    sourcePosition: Optional[str] = None
    targetPosition: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    selected: Optional[bool] = False
    data: Dict[str, Any] = Field(default_factory=dict)


class DifyEdge(BaseModel):
    """Dify边模型"""
    id: str
    type: str = "custom"
    source: str
    target: str
    sourceHandle: Optional[str] = "source"
    targetHandle: Optional[str] = "target"
    data: Dict[str, Any] = Field(default_factory=dict)
    zIndex: Optional[int] = 0


class DifyGraph(BaseModel):
    """Dify图模型"""
    edges: List[DifyEdge] = Field(default_factory=list)
    nodes: List[DifyNode] = Field(default_factory=list)
    viewport: Dict[str, float] = Field(default_factory=lambda: {"x": 0, "y": 0, "zoom": 1.0})


class DifyWorkflow(BaseModel):
    """Dify工作流模型"""
    conversation_variables: List = Field(default_factory=list)
    environment_variables: List = Field(default_factory=list)
    features: Dict[str, Any] = Field(default_factory=dict)
    graph: DifyGraph = Field(default_factory=DifyGraph)


class DifyApp(BaseModel):
    """Dify应用模型"""
    description: str = ""
    icon: str = "🤖"
    icon_background: str = "#FFEAD5"
    mode: str = "workflow"
    name: str = ""
    use_icon_as_answer_icon: bool = False


class DifyWorkflowConfig(BaseModel):
    """完整的Dify YAML配置模型"""
    app: DifyApp = Field(default_factory=DifyApp)
    dependencies: List = Field(default_factory=list)
    kind: str = "app"
    version: str = "0.3.1"
    workflow: DifyWorkflow = Field(default_factory=DifyWorkflow)


# Dify节点状态类型定义
class DifyStartState(BaseModel):
    """Dify开始节点状态"""
    desc: str = ""
    selected: bool = False
    title: str = "开始"
    type: str = "start"
    variables: List = Field(default_factory=lambda: [
        {
            "label": "系统输入",
            "max_length": 48000,
            "options": [],
            "required": True,
            "type": "text-input",
            "variable": "sys_input"
        }
    ])


class DifyLLMState(BaseModel):
    """Dify LLM节点状态"""
    context: Dict[str, Any] = Field(default_factory=lambda: {"enabled": False, "variable_selector": []})
    desc: str = ""
    model: Dict[str, Any] = Field(default_factory=lambda: {
        "completion_params": {"temperature": 0.7},
        "mode": "chat",
        "name": "",
        "provider": ""
    })
    prompt_template: List[Dict[str, str]] = Field(default_factory=lambda: [{"role": "system", "text": ""}])
    selected: bool = False
    structured_output: Optional[Dict[str, Any]] = None
    structured_output_enabled: bool = False
    title: str = "LLM"
    type: str = "llm"
    variables: List = Field(default_factory=list)
    vision: Dict[str, bool] = Field(default_factory=lambda: {"enabled": False})


class DifyKnowledgeRetrievalState(BaseModel):
    """Dify知识检索节点状态"""
    dataset_ids: List[str] = Field(default_factory=list)
    desc: str = ""
    multiple_retrieval_config: Dict[str, Any] = Field(default_factory=lambda: {
        "reranking_enable": False,
        "top_k": 4
    })
    query_variable_selector: List = Field(default_factory=list)
    retrieval_mode: str = "multiple"
    selected: bool = False
    title: str = "知识检索"
    type: str = "knowledge-retrieval"


class DifyEndState(BaseModel):
    """Dify结束节点状态"""
    desc: str = ""
    outputs: List = Field(default_factory=list)
    selected: bool = False
    title: str = "结束"
    type: str = "end"


class DifyAnswerState(BaseModel):
    """Dify直接回复节点状态"""
    desc: str = ""
    selected: bool = False
    title: str = "直接回复"
    type: str = "answer"
    variables: List = Field(default_factory=list)


class DifyCodeState(BaseModel):
    """Dify代码执行节点状态"""
    code: str = ""
    code_language: str = "python3"
    desc: str = ""
    outputs: Dict[str, Any] = Field(default_factory=dict)
    selected: bool = False
    title: str = "代码执行"
    type: str = "code"
    variables: List = Field(default_factory=list)


class DifyToolState(BaseModel):
    """Dify工具调用节点状态"""
    desc: str = ""
    provider_id: str = ""
    provider_name: str = ""
    provider_type: str = "builtin"
    selected: bool = False
    title: str = "工具调用"
    tool_configurations: Dict[str, Any] = Field(default_factory=dict)
    tool_description: str = ""
    tool_label: str = ""
    tool_name: str = ""
    tool_parameters: Dict[str, Any] = Field(default_factory=dict)
    type: str = "tool"


class DifyIfElseState(BaseModel):
    """Dify条件分支节点状态"""
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    desc: str = ""
    logical_operator: str = "and"
    selected: bool = False
    title: str = "条件分支"
    type: str = "if-else"


# 节点状态工厂
DIFY_NODE_STATE_FACTORY = {
    "start": DifyStartState,
    "llm": DifyLLMState,
    "knowledge-retrieval": DifyKnowledgeRetrievalState,
    "end": DifyEndState,
    "answer": DifyAnswerState,
    "code": DifyCodeState,
    "tool": DifyToolState,
    "if-else": DifyIfElseState,
}


def create_dify_node_state(node_type: str, **kwargs) -> BaseModel:
    """
    根据节点类型创建对应的节点状态实例
    
    Args:
        node_type: 节点类型
        **kwargs: 初始化参数
        
    Returns:
        对应的节点状态实例
        
    Raises:
        ValueError: 当node_type不支持时
    """
    state_class = DIFY_NODE_STATE_FACTORY.get(node_type)
    if not state_class:
        raise ValueError(f"Unsupported node_type: {node_type}")
    
    return state_class(**kwargs)
