from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


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
    
    @classmethod
    def get_valid_fields(cls) -> set:
        """获取该状态类的所有有效字段名（排除基础字段）"""
        base_fields = {"switch", "switchAny", "finish"}
        all_fields = set(cls.model_fields.keys())
        return all_fields - base_fields


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
    isvisible: Optional[bool] = True
    temperature: Optional[float] = 0.1
    maxToken: Optional[int] = 5000
    isResponseAnswerText: Optional[bool] = False
    answerText: Optional[str] = ""


class ConfirmReplyState(BaseNodeState):
    """确定回复模块状态"""
    text: Optional[str] = ""
    isvisible: Optional[bool] = True


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
    """循环模块状态
    
    注意：index、item、length 字段会自动生成唯一的随机ID格式（如 a545776c.index），
    不接受用户传入的值，每次创建实例都会自动生成新的唯一标识符。
    """
    items: Optional[List[Any]] = Field(default_factory=list)
    index: Optional[str] = ""  # 自动生成，格式：随机ID.index
    item: Optional[str] = ""   # 自动生成，格式：随机ID.item
    length: Optional[str] = "" # 自动生成，格式：随机ID.length
    loopEnd: Optional[bool] = False
    loopStart: Optional[bool] = False
    
    def model_post_init(self, __context):
        """初始化后自动生成循环变量的唯一标识符"""
        random_id = uuid.uuid4().hex[:8]
        self.index = f"{random_id}.index"
        self.item = f"{random_id}.item"
        self.length = f"{random_id}.length"


class DocumentQuestionState(BaseNodeState):
    """文档批量提问模块状态"""
    files: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    batchQuestion: Optional[List[str]] = Field(default_factory=list)
    model: Optional[str] = "glm-4"
    quotePrompt: Optional[str] = ""
    isResponseAnswerText: Optional[bool] = False
    answerText: Optional[str] = ""


class KeywordIdentifyState(BaseNodeState):
    """关键词识别模块状态"""
    files: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    identifyRule: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    identifyResult: Optional[List[Dict[str, Any]]] = Field(default_factory=list)


class OfficeWordExportState(BaseNodeState):
    """文档输出模块状态"""
    text: Optional[str] = ""
    templateFile: Optional[str] = None
    fileInfo: Optional[str] = ""

class MarkdownToWordState(BaseNodeState):
    """Markdown转Word模块状态"""
    markdown: Optional[str] = ""
    word: Optional[str] = ""
    fileInfo: Optional[str] = ""

class CodeExtractState(BaseNodeState):
    """代码提取器模块状态"""
    code: Optional[str] = ""
    fileInfo: Optional[str] = ""

class DatabaseQueryState(BaseNodeState):
    """数据库查询模块状态"""
    sql: Optional[str] = ""
    database: Optional[Union[str, Dict[str, Any]]] = ""  # 支持字符串或字典格式
    showTable: Optional[bool] = True
    queryResult: Optional[str] = ""
    success: Optional[bool] = False
    failed: Optional[bool] = False

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
    "documentQuestion": DocumentQuestionState,
    "keywordIdentify": KeywordIdentifyState,
    "officeWordExport": OfficeWordExportState,
    "markdownToWord": MarkdownToWordState,
    "codeExtract": CodeExtractState,
    "databaseQuery": DatabaseQueryState,
}