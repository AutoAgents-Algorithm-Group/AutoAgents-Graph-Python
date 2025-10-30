from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DifyNode(BaseModel):
    """Dify节点模型"""
    data: Dict[str, Any] = Field(default_factory=dict)  
    draggable: Optional[bool] = None  # 是否可拖拽
    height: Optional[int] = None
    id: str
    parentId: Optional[str] = None  # 父节点ID（用于iteration内的节点）
    position: Dict[str, float]
    positionAbsolute: Optional[Dict[str, float]] = None
    selectable: Optional[bool] = None  # 是否可选择
    selected: Optional[bool] = False
    sourcePosition: Optional[str] = None
    targetPosition: Optional[str] = None
    type: str = "custom"
    width: Optional[int] = None
    zIndex: Optional[int] = None  # z轴层级


class DifyEdge(BaseModel):
    """Dify边模型"""
    data: Dict[str, Any] = Field(default_factory=dict)  
    id: str
    selected: Optional[bool] = None  # 添加selected字段
    source: str
    sourceHandle: Optional[str] = "source"
    target: str
    targetHandle: Optional[str] = "target"
    type: str = "custom"
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
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


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
    vision: Dict[str, Any] = Field(default_factory=lambda: {"enabled": False})  # 改为Any以支持configs
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


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
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


class DifyEndState(BaseModel):
    """Dify结束节点状态"""
    desc: str = ""
    outputs: List = Field(default_factory=list)
    selected: bool = False
    title: str = "结束"
    type: str = "end"
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


class DifyAnswerState(BaseModel):
    """Dify直接回复节点状态"""
    answer: str = ""  # 回复内容，支持变量引用如 {{#variable#}}
    desc: str = ""
    selected: bool = False
    title: str = "直接回复"
    type: str = "answer"
    variables: List = Field(default_factory=list)
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


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
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


class DifyToolState(BaseModel):
    """Dify工具调用节点状态"""
    desc: str = ""
    is_team_authorization: Optional[bool] = None
    output_schema: Optional[Any] = None
    paramSchemas: Optional[List[Dict[str, Any]]] = None
    params: Optional[Dict[str, Any]] = None
    provider_id: str = ""
    provider_name: str = ""
    provider_type: str = "builtin"
    selected: bool = False
    title: str = "工具调用"
    tool_configurations: Dict[str, Any] = Field(default_factory=dict)
    tool_description: str = ""
    tool_label: str = ""
    tool_name: str = ""
    tool_node_version: Optional[str] = None
    tool_parameters: Dict[str, Any] = Field(default_factory=dict)
    type: str = "tool"
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


class DifyIfElseState(BaseModel):
    """Dify条件分支节点状态"""
    cases: List[Dict[str, Any]] = Field(default_factory=list)  # cases是必须的，包含条件配置
    desc: str = ""
    logical_operator: str = "and"
    selected: bool = False
    title: str = "条件分支"
    type: str = "if-else"
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


class DifyIterationState(BaseModel):
    """Dify迭代节点状态"""
    desc: str = ""
    error_handle_mode: str = "terminated"  # 错误处理模式
    height: Optional[int] = None
    input_parameters: List[Dict[str, Any]] = Field(default_factory=list)  # 输入参数
    is_array_input: bool = True  # 是否数组输入
    is_parallel: bool = False  # 是否并行执行
    iterator_selector: List[Any] = Field(default_factory=list)  # 迭代器选择器
    output_selector: List[Any] = Field(default_factory=list)  # 输出选择器
    output_type: str = "array[string]"  # 输出类型
    parallel_nums: int = 10  # 并行数量
    selected: bool = False
    start_node_id: str = ""  # 迭代开始节点ID
    title: str = "迭代"
    type: str = "iteration"
    width: Optional[int] = None
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据


class DifyIterationStartState(BaseModel):
    """Dify迭代开始节点状态"""
    desc: str = ""
    isInIteration: bool = True  # 在迭代块内
    selected: bool = False
    title: str = ""
    type: str = "iteration-start"
    
    class Config:
        extra = "allow"  # 允许额外字段，保留原始数据
    
    # 注意：parentId 是节点层级的属性，不应在State中定义
    # iteration_id 对于 iteration-start 节点不需要（它本身就是迭代的起点）


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
