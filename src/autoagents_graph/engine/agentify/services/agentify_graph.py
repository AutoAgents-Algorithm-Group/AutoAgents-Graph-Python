import json
import uuid
from typing import Optional, List, Dict

from ..utils import (
    NodeValidator, NodeBuilder, EdgeValidator, GraphProcessor
)
from ..api.graph_api import create_app_api
from ..models.graph_types import CreateAppParams


START = "simpleInputId"
# END = None

class AgentifyNode:
    def __init__(self, node_id, module_type, position, inputs=None, outputs=None):
        self.id = node_id
        self.type = "custom"
        self.initialized = False
        self.position = position
        self.data = {
            "inputs": inputs or [],
            "outputs": outputs or [],
            "disabled": False,
            "moduleType": module_type,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "initialized": self.initialized,
            "position": self.position,
            "data": self.data
        }

class AgentifyEdge:
    def __init__(self, source, target, source_handle="", target_handle=""):
        self.id = str(uuid.uuid4())
        self.type = "custom"
        self.source = source
        self.target = target
        self.sourceHandle = source_handle
        self.targetHandle = target_handle
        self.data = {}
        self.label = ""
        self.animated = False
        self.sourceX = 0
        self.sourceY = 0
        self.targetX = 0
        self.targetY = 0

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source,
            "target": self.target,
            "sourceHandle": self.sourceHandle,
            "targetHandle": self.targetHandle,
            "data": self.data,
            "label": self.label,
            "animated": self.animated,
            "sourceX": self.sourceX,
            "sourceY": self.sourceY,
            "targetX": self.targetX,
            "targetY": self.targetY
        }

class AgentifyGraph:
    def __init__(self, 
                 personal_auth_key: Optional[str] = None, 
                 personal_auth_secret: Optional[str] = None, 
                 jwt_token: Optional[str] = None,
                 base_url: str = "https://uat.agentspro.cn"):
        """
        初始化 AgentifyGraph
        
        Args:
            personal_auth_key: 个人认证密钥（如果提供了 jwt_token 则可选）
            personal_auth_secret: 个人认证密码（如果提供了 jwt_token 则可选）
            jwt_token: JWT 认证令牌（可选，如果提供则直接使用，不再调用获取 token 接口）
            base_url: API 基础URL，默认为 "https://uat.agentspro.cn"
        """
        # 结构信息
        self.nodes = []
        self.edges = []
        self.viewport = {"x": 0, "y": 0, "zoom": 1.0}
        
        # 认证信息
        self.personal_auth_key = personal_auth_key
        self.personal_auth_secret = personal_auth_secret
        self.jwt_token = jwt_token
        self.base_url = base_url


    def add_node(self, id: str, *, position=None, state):
        """
        添加节点到工作流图中
        
        Args:
            id: 节点ID
            position: 节点位置，格式为 {"x": 100, "y": 200}，默认自动布局
            state: 节点状态对象（LangGraph风格）
        """
        # 1. 参数验证
        NodeValidator.validate_node_params(id, state)
        
        # 2. 处理位置布局
        position = NodeBuilder.resolve_node_position(position, len(self.nodes))
        
        # 3. 提取state配置
        module_type, inputs, outputs = NodeBuilder.extract_node_config(state, id, position)
        
        # 4. 创建节点
        node = NodeBuilder.create_node(id, position, module_type, inputs, outputs)
        self.nodes.append(node)


    def add_edge(self, source: str, target: str, source_handle: str = "", target_handle: str = ""):
        """
        添加边连接两个节点
        
        Args:
            source: 源节点ID
            target: 目标节点ID
            source_handle: 源节点输出句柄
            target_handle: 目标节点输入句柄
        """
        # 验证参数
        EdgeValidator.validate_edge_params(source, target, source_handle, target_handle)
        EdgeValidator.validate_nodes_exist(source, target, self.nodes)
        
        # 检查并修正句柄类型兼容性
        source_handle, target_handle = GraphProcessor.check_and_fix_handle_type(source, target, source_handle, target_handle, self.nodes)
        
        # 创建并添加边
        edge = AgentifyEdge(source, target, source_handle, target_handle)
        self.edges.append(edge)


    def to_json(self):
        return json.dumps(
            {
                "nodes": [node.to_dict() for node in self.nodes],
                "edges": [edge.to_dict() for edge in self.edges],
                "viewport": self.viewport
            }, 
            indent=2, 
            ensure_ascii=False
        )


    def compile(self,
                name: str = "未命名智能体", # 智能体名称
                avatar: str = "https://uat.agentspro.cn/assets/agent/avatar.png", # 头像URL
                intro: Optional[str] = None, # 智能体介绍
                chatAvatar: Optional[str] = None, # 对话头像URL
                shareAble: Optional[bool] = True, # 是否可分享
                guides: Optional[List] = None, # 引导配置
                category: Optional[str] = None, # 分类
                state: Optional[int] = None, # 状态
                prologue: Optional[str] = None, # 开场白
                extJsonObj: Optional[Dict] = None, # 扩展JSON对象
                allowVoiceInput: Optional[bool] = False, # 是否允许语音输入
                autoSendVoice: Optional[bool] = False, # 是否自动发送语音
                **kwargs) -> None: # 其他参数
        """
        编译并创建智能体应用
        """

        # 更新node里面的targets
        GraphProcessor.update_nodes_targets(self.nodes, self.edges)

        data = CreateAppParams(
            name=name,
            avatar=avatar,
            intro=intro,
            chatAvatar=chatAvatar,
            shareAble=shareAble,
            guides=guides,
            appModel=self.to_json(),  # 自动设置工作流JSON
            category=category,
            state=state,
            prologue=prologue,
            extJsonObj=extJsonObj,
            allowVoiceInput=allowVoiceInput,
            autoSendVoice=autoSendVoice,
            **kwargs
        )
        
        create_app_api(
            data=data, 
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )

