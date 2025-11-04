import json
import uuid
from typing import Optional, List, Dict, Any

from ..utils import (
    NodeValidator, NodeBuilder, EdgeValidator, GraphProcessor
)
from ..api.graph_api import create_app_api, update_app_api, get_app_detail_api
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
        
        response = create_app_api(
            data=data, 
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )

        workflow_id = response.get("data").get("id")
        
        print("workflow_id:", workflow_id)

        return workflow_id

    def update(self,
               agent_id: int, # 要更新的智能体ID
               name: Optional[str] = None, # 智能体名称
               avatar: Optional[str] = None, # 头像URL
               intro: Optional[str] = None, # 智能体介绍
               chatAvatar: Optional[str] = None, # 对话头像URL
               shareAble: Optional[bool] = None, # 是否可分享
               guides: Optional[List] = None, # 引导配置
               category: Optional[str] = None, # 分类
               state: Optional[int] = None, # 状态
               prologue: Optional[str] = None, # 开场白
               extJsonObj: Optional[Dict] = None, # 扩展JSON对象
               allowVoiceInput: Optional[bool] = None, # 是否允许语音输入
               autoSendVoice: Optional[bool] = None, # 是否自动发送语音
               load_existing_workflow: bool = True, # 是否加载现有工作流结构
               merge_workflow: bool = True, # 是否合并工作流（True=合并，False=完全替换）
               **kwargs) -> None: # 其他参数
        """
        更新智能体应用（支持获取现有配置并修改工作流结构）
        
        Args:
            agent_id: 要更新的智能体ID
            name: 智能体名称（可选，不提供则保持原值）
            avatar: 头像URL（可选，不提供则保持原值）
            intro: 智能体介绍（可选，不提供则保持原值）
            chatAvatar: 对话头像URL（可选，不提供则保持原值）
            shareAble: 是否可分享（可选，不提供则保持原值）
            guides: 引导配置（可选，不提供则保持原值）
            category: 分类（可选，不提供则保持原值）
            state: 状态（可选，不提供则保持原值）
            prologue: 开场白（可选，不提供则保持原值）
            extJsonObj: 扩展JSON对象（可选，不提供则保持原值）
            allowVoiceInput: 是否允许语音输入（可选，不提供则保持原值）
            autoSendVoice: 是否自动发送语音（可选，不提供则保持原值）
            load_existing_workflow: 是否加载现有工作流结构到当前实例
            merge_workflow: 是否合并工作流（True=在现有基础上添加当前节点，False=完全使用当前工作流）
            **kwargs: 其他参数
        """
        
        print("=== 开始更新智能体 ===")
        
        # 获取现有配置
        print("📖 获取现有智能体配置...")
        response = get_app_detail_api(
            agent_id=agent_id,
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )
        current_config = response.get("data", {})
        print("✅ 成功获取配置")
        
        # 处理工作流结构
        final_workflow_json = ""
        
        if load_existing_workflow:
            print("🔄 处理工作流结构...")
            # 获取现有工作流
            existing_app_model = current_config.get('appModel', '{}')
            if isinstance(existing_app_model, str):
                import json
                try:
                    existing_workflow = json.loads(existing_app_model)
                except json.JSONDecodeError:
                    print("⚠️ 现有工作流JSON解析失败，将使用空工作流")
                    existing_workflow = {"nodes": [], "edges": [], "viewport": {"x": 0, "y": 0, "zoom": 1.0}}
            else:
                existing_workflow = existing_workflow or {"nodes": [], "edges": [], "viewport": {"x": 0, "y": 0, "zoom": 1.0}}
            
            if merge_workflow and (self.nodes or self.edges):
                print("🔀 合并现有工作流和新增内容...")
                # 合并模式：保留现有节点和边，添加当前构建的节点和边
                
                # 更新当前构建的nodes的targets
                GraphProcessor.update_nodes_targets(self.nodes, self.edges)
                
                # 合并节点 - 避免重复ID
                existing_nodes = existing_workflow.get('nodes', [])
                existing_node_ids = {node.get('id') for node in existing_nodes}
                
                merged_nodes = existing_nodes.copy()
                new_nodes_count = 0
                
                for node in self.nodes:
                    node_dict = node.to_dict()
                    node_id = node_dict.get('id')
                    
                    if node_id in existing_node_ids:
                        # 如果节点ID已存在，更新现有节点
                        for i, existing_node in enumerate(merged_nodes):
                            if existing_node.get('id') == node_id:
                                merged_nodes[i] = node_dict
                                print(f"  🔄 更新节点: {node_id}")
                                break
                    else:
                        # 添加新节点
                        merged_nodes.append(node_dict)
                        new_nodes_count += 1
                        print(f"  ➕ 添加新节点: {node_id}")
                
                # 合并边 - 避免重复连接
                existing_edges = existing_workflow.get('edges', [])
                existing_edge_keys = {
                    f"{edge.get('source')}→{edge.get('target')}:{edge.get('sourceHandle')}→{edge.get('targetHandle')}"
                    for edge in existing_edges
                }
                
                merged_edges = existing_edges.copy()
                new_edges_count = 0
                
                for edge in self.edges:
                    edge_dict = edge.to_dict()
                    edge_key = f"{edge_dict.get('source')}→{edge_dict.get('target')}:{edge_dict.get('sourceHandle')}→{edge_dict.get('targetHandle')}"
                    
                    if edge_key not in existing_edge_keys:
                        merged_edges.append(edge_dict)
                        new_edges_count += 1
                        print(f"  ➕ 添加新连接: {edge_dict.get('source')} → {edge_dict.get('target')}")
                
                # 保持现有视口设置
                final_workflow = {
                    "nodes": merged_nodes,
                    "edges": merged_edges,
                    "viewport": existing_workflow.get('viewport', {"x": 0, "y": 0, "zoom": 1.0})
                }
                
                print(f"✅ 合并完成: 现有{len(existing_nodes)}节点+新增{new_nodes_count}节点, 现有{len(existing_edges)}连接+新增{new_edges_count}连接")
                
            elif self.nodes or self.edges:
                print("🔄 使用当前构建的工作流完全替换...")
                # 完全替换模式：使用当前构建的工作流
                GraphProcessor.update_nodes_targets(self.nodes, self.edges)
                
                final_workflow = {
                    "nodes": [node.to_dict() for node in self.nodes],
                    "edges": [edge.to_dict() for edge in self.edges],
                    "viewport": self.viewport
                }
                print(f"✅ 完全替换: {len(self.nodes)}个节点, {len(self.edges)}个连接")
            else:
                print("📋 保持现有工作流结构不变...")
                # 没有新的工作流内容，保持现有结构
                final_workflow = existing_workflow
                
            final_workflow_json = json.dumps(final_workflow, ensure_ascii=False)
            
        else:
            print("🆕 使用当前构建的工作流...")
            # 不加载现有工作流，直接使用当前构建的工作流
            GraphProcessor.update_nodes_targets(self.nodes, self.edges)
            final_workflow_json = self.to_json()
        
        # 构建更新参数 - 使用现有值作为默认值
        update_params = {
            'name': name if name is not None else current_config.get('name', '未命名智能体'),
            'avatar': avatar if avatar is not None else current_config.get('avatar', 'https://uat.agentspro.cn/assets/agent/avatar.png'),
            'intro': intro if intro is not None else current_config.get('intro', ''),
            'chatAvatar': chatAvatar if chatAvatar is not None else current_config.get('chatAvatar', ''),
            'shareAble': shareAble if shareAble is not None else current_config.get('shareAble', True),
            'guides': guides if guides is not None else current_config.get('guides', []),
            'category': category if category is not None else current_config.get('category', ''),
            'state': state if state is not None else current_config.get('state', 1),
            'prologue': prologue if prologue is not None else current_config.get('prologue', ''),
            'extJsonObj': extJsonObj if extJsonObj is not None else current_config.get('extJsonObj', {}),
            'allowVoiceInput': allowVoiceInput if allowVoiceInput is not None else current_config.get('allowVoiceInput', False),
            'autoSendVoice': autoSendVoice if autoSendVoice is not None else current_config.get('autoSendVoice', False),
            'appModel': final_workflow_json
        }
        
        # 添加其他kwargs参数
        update_params.update(kwargs)
        
        data = CreateAppParams(**update_params)
        
        print("📤 执行更新请求...")
        response = update_app_api(
            agent_id=agent_id,
            data=data,
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )

        updated_workflow_id = response.get("data").get("id")
        
        print(f"✅ 智能体更新成功! ID: {updated_workflow_id}")

        return updated_workflow_id

    def get_json(self, agent_id: int) -> Dict[str, Any]:
        """
        获取指定智能体的 appModel JSON 内容
        
        Args:
            agent_id: 智能体的唯一标识符
            
        Returns:
            Dict[str, Any]: 智能体的 appModel JSON 内容（包含nodes、edges等工作流结构）
        """
        response = get_app_detail_api(
            agent_id=agent_id,
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )
        
        data = response.get("data", {})
        app_model = data.get("appModel", "{}")
        
        # 如果 appModel 是字符串，解析为 JSON
        if isinstance(app_model, str):
            import json
            try:
                return json.loads(app_model)
            except json.JSONDecodeError:
                print("警告：appModel JSON 解析失败，返回空对象")
                return {}
        
        # 如果已经是字典，直接返回
        return app_model
        
    def merge_update(self,
                    agent_id: int,
                    name: Optional[str] = None, 
                    avatar: Optional[str] = None,
                    intro: Optional[str] = None,
                    chatAvatar: Optional[str] = None,
                    shareAble: Optional[bool] = None,
                    guides: Optional[List] = None,
                    category: Optional[str] = None,
                    state: Optional[int] = None,
                    prologue: Optional[str] = None,
                    extJsonObj: Optional[Dict] = None,
                    allowVoiceInput: Optional[bool] = None,
                    autoSendVoice: Optional[bool] = None,
                    update_workflow: bool = True,  # 是否更新工作流结构
                    **kwargs) -> None:
        """
        增量更新智能体应用
        
        Args:
            agent_id: 要更新的智能体ID
            name: 智能体名称（可选，不提供则保持原值）
            avatar: 头像URL（可选，不提供则保持原值）
            intro: 智能体介绍（可选，不提供则保持原值）
            chatAvatar: 对话头像URL（可选，不提供则保持原值）
            shareAble: 是否可分享（可选，不提供则保持原值）
            guides: 引导配置（可选，不提供则保持原值）
            category: 分类（可选，不提供则保持原值）
            state: 状态（可选，不提供则保持原值）
            prologue: 开场白（可选，不提供则保持原值）
            extJsonObj: 扩展JSON对象（可选，不提供则保持原值）
            allowVoiceInput: 是否允许语音输入（可选，不提供则保持原值）
            autoSendVoice: 是否自动发送语音（可选，不提供则保持原值）
            update_workflow: 是否更新工作流结构（默认True，如果False则保持现有工作流）
            **kwargs: 其他参数
        """
        
        # 获取现有配置（完整的智能体配置，不只是appModel）
        response = get_app_detail_api(
            agent_id=agent_id,
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )
        current_config = response.get("data", {})
        
        # 构建更新数据，只包含提供的参数
        update_params = {}
        
        # 使用提供的参数，如果没有提供则使用现有值
        update_params['name'] = name if name is not None else current_config.get('name', '未命名智能体')
        update_params['avatar'] = avatar if avatar is not None else current_config.get('avatar', 'https://uat.agentspro.cn/assets/agent/avatar.png')
        update_params['intro'] = intro if intro is not None else current_config.get('intro', '')
        update_params['chatAvatar'] = chatAvatar if chatAvatar is not None else current_config.get('chatAvatar', '')
        update_params['shareAble'] = shareAble if shareAble is not None else current_config.get('shareAble', True)
        update_params['guides'] = guides if guides is not None else current_config.get('guides', [])
        update_params['category'] = category if category is not None else current_config.get('category', '')
        update_params['state'] = state if state is not None else current_config.get('state', 1)
        update_params['prologue'] = prologue if prologue is not None else current_config.get('prologue', '')
        update_params['extJsonObj'] = extJsonObj if extJsonObj is not None else current_config.get('extJsonObj', {})
        update_params['allowVoiceInput'] = allowVoiceInput if allowVoiceInput is not None else current_config.get('allowVoiceInput', False)
        update_params['autoSendVoice'] = autoSendVoice if autoSendVoice is not None else current_config.get('autoSendVoice', False)
        
        # 处理工作流结构
        if update_workflow:
            # 更新node里面的targets
            GraphProcessor.update_nodes_targets(self.nodes, self.edges)
            # 使用当前构建的工作流
            update_params['appModel'] = self.to_json()
        else:
            # 保持现有工作流结构
            update_params['appModel'] = current_config.get('appModel', '{}')
        
        # 添加其他kwargs参数
        update_params.update(kwargs)
        
        data = CreateAppParams(**update_params)
        
        response = update_app_api(
            agent_id=agent_id,
            data=data,
            personal_auth_key=self.personal_auth_key, 
            personal_auth_secret=self.personal_auth_secret, 
            base_url=self.base_url,
            jwt_token=self.jwt_token
        )

        updated_workflow_id = response.get("data").get("id")
        
        print("updated_workflow_id:", updated_workflow_id)

        return updated_workflow_id