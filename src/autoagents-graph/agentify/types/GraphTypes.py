from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime


class AgentGuide(BaseModel):
    indexNum: Optional[int] = None
    guide: Optional[str] = None


class CreateAppParams(BaseModel):
    id: Optional[int] = None
    uuid: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    chatAvatar: Optional[str] = None
    intro: Optional[str] = None
    shareAble: Optional[bool] = None
    guides: Optional[List[AgentGuide]] = None
    appModel: Optional[str] = None
    category: Optional[str] = None
    state: Optional[int] = None
    prologue: Optional[str] = None
    extJsonObj: Optional[Dict[str, Any]] = None
    allowVoiceInput: Optional[bool] = None
    autoSendVoice: Optional[bool] = None
    updateAt: Optional[datetime] = None


# ===== Node States =====

class BaseNodeState(BaseModel):
    """基础节点状态模型"""
    switch: Optional[bool] = False # 联动激活
    switchAny: Optional[bool] = False # 任一激活
    finish: Optional[bool] = False # 运行结束


class HttpInvokeState(BaseNodeState):
    """HTTP调用模块状态"""
    url: Optional[str] = ""
    requestBody: Optional[str] = ""
    success: Optional[bool] = False
    failed: Optional[bool] = False
    response: Optional[str] = ""


class QuestionInputState(BaseNodeState):
    """用户提问模块状态"""
    inputText: Optional[bool] = True
    uploadFile: Optional[bool] = False
    uploadPicture: Optional[bool] = False
    fileUpload: Optional[bool] = False
    fileContrast: Optional[bool] = False
    fileInfo: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    initialInput: Optional[bool] = True
    userChatInput: Optional[str] = ""
    files: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    images: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    unclickedButton: Optional[bool] = False


class AiChatState(BaseNodeState):
    """智能对话模块状态"""
    text: Optional[str] = ""
    images: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    knSearch: Optional[str] = ""
    knConfig: Optional[str] = ""
    historyText: Optional[int] = 3
    model: Optional[str] = "doubao-deepseek-v3"
    quotePrompt: Optional[str] = ""
    stream: Optional[bool] = True
    temperature: Optional[float] = 0.0
    maxToken: Optional[int] = 5000
    isResponseAnswerText: Optional[bool] = False
    answerText: Optional[str] = ""


class ConfirmReplyState(BaseNodeState):
    """确定回复模块状态"""
    stream: Optional[bool] = True
    text: Optional[str] = ""


class KnowledgeSearchState(BaseNodeState):
    """知识库搜索模块状态"""
    text: Optional[str] = ""
    datasets: Optional[List[str]] = Field(default_factory=list)
    similarity: Optional[float] = 0.2
    vectorSimilarWeight: Optional[float] = 1.0
    topK: Optional[int] = 20
    enableRerank: Optional[bool] = False
    rerankModelType: Optional[str] = "oneapi-xinference:bce-rerank"
    rerankTopK: Optional[int] = 10
    isEmpty: Optional[bool] = False
    unEmpty: Optional[bool] = False
    quoteQA: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class Pdf2MdState(BaseNodeState):
    """通用文档解析模块状态"""
    files: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    pdf2mdType: Optional[str] = "general"
    pdf2mdResult: Optional[str] = ""
    success: Optional[bool] = False
    failed: Optional[bool] = False


class AddMemoryVariableState(BaseNodeState):
    """添加记忆变量模块状态"""
    feedback: Optional[str] = ""
    variables: Optional[Dict[str, Any]] = Field(default_factory=dict)


class InfoClassState(BaseNodeState):
    """信息分类模块状态"""
    text: Optional[str] = ""
    knSearch: Optional[str] = ""
    knConfig: Optional[str] = ""
    historyText: Optional[int] = 3
    model: Optional[str] = "doubao-deepseek-v3"
    quotePrompt: Optional[str] = ""
    labels: Optional[Union[Dict[str, str], List[Dict[str, str]]]] = Field(default_factory=dict)
    matchResult: Optional[str] = ""


class CodeFragmentState(BaseNodeState):
    """代码块模块状态"""
    language: Optional[str] = "js"
    description: Optional[str] = ""
    code: Optional[str] = ""
    runSuccess: Optional[bool] = False
    runFailed: Optional[bool] = False
    runResult: Optional[str] = ""
    inputs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    outputs: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ForEachState(BaseNodeState):
    """循环模块状态"""
    items: Optional[List[Any]] = Field(default_factory=list)
    index: Optional[int] = 0
    item: Optional[Any] = None
    length: Optional[int] = 0
    loopEnd: Optional[bool] = False
    loopStart: Optional[bool] = False


# 状态工厂字典，根据module_type获取对应的State类
NODE_STATE_FACTORY = {
    "httpInvoke": HttpInvokeState,
    "questionInput": QuestionInputState,
    "aiChat": AiChatState,
    "confirmreply": ConfirmReplyState,
    "knowledgesSearch": KnowledgeSearchState,
    "pdf2md": Pdf2MdState,
    "addMemoryVariable": AddMemoryVariableState,
    "infoClass": InfoClassState,
    "codeFragment": CodeFragmentState,
    "forEach": ForEachState,
}


def create_node_state(module_type: str, **kwargs) -> BaseNodeState:
    """
    根据module_type创建对应的State实例
    
    Args:
        module_type: 模块类型
        **kwargs: 初始化参数
        
    Returns:
        对应的State实例
        
    Raises:
        ValueError: 当module_type不支持时
    """
    state_class = NODE_STATE_FACTORY.get(module_type)
    if not state_class:
        raise ValueError(f"Unsupported module_type: {module_type}")
    
    return state_class(**kwargs)