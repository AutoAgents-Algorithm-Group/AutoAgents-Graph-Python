import yaml
from typing import Optional, List, Dict, Any

from ..models.dify_types import (
    DifyWorkflowConfig, DifyApp, DifyWorkflow, DifyGraph as DifyGraphModel,
    DifyNode, DifyEdge, create_dify_node_state
)

# Dify工作流常量
START = "start"
END = "end"


class DifyGraph:
    """
    Dify图构建器，类似于AgentifyGraph但针对Dify平台
    """
    
    def __init__(self, 
                 app_name: str = "AutoAgents工作流",
                 app_description: str = "基于AutoAgents SDK构建的工作流",
                 app_icon: str = "🤖",
                 app_icon_background: str = "#FFEAD5"):
        """
        初始化DifyGraph构建器
        
        Args:
            app_name: 应用名称
            app_description: 应用描述
            app_icon: 应用图标
            app_icon_background: 应用图标背景色
        """
        # 初始化应用配置
        self.app = DifyApp(
            name=app_name,
            description=app_description,
            icon=app_icon,
            icon_background=app_icon_background
        )
        
        # 初始化工作流配置
        self.workflow = DifyWorkflow()
        
        # 节点和边列表
        self.nodes: List[DifyNode] = []
        self.edges: List[DifyEdge] = []

        # 设置默认viewport
        self.workflow.graph.viewport = {"x": 0, "y": 0, "zoom": 1.0}

        # 默认特性配置
        self._init_default_features()
    
    def _init_default_features(self):
        """初始化默认特性配置"""
        self.workflow.features = {
            "file_upload": {
                "allowed_file_extensions": [".JPG", ".JPEG", ".PNG", ".GIF", ".WEBP", ".SVG"],
                "allowed_file_types": ["image"],
                "allowed_file_upload_methods": ["local_file", "remote_url"],
                "enabled": False,
                "fileUploadConfig": {
                    "audio_file_size_limit": 50,
                    "batch_count_limit": 5,
                    "file_size_limit": 15,
                    "image_file_size_limit": 10,
                    "video_file_size_limit": 100,
                    "workflow_file_upload_limit": 10
                },
                "image": {
                    "enabled": False,
                    "number_limits": 3,
                    "transfer_methods": ["local_file", "remote_url"]
                },
                "number_limits": 3
            },
            "opening_statement": "",
            "retriever_resource": {
                "enabled": True
            },
            "sensitive_word_avoidance": {
                "enabled": False
            },
            "speech_to_text": {
                "enabled": False
            },
            "suggested_questions": [],
            "suggested_questions_after_answer": {
                "enabled": False
            },
            "text_to_speech": {
                "enabled": False,
                "language": "",
                "voice": ""
            }
        }
    
    def add_node(self, 
                 id: str,
                 type: str,
                 position: Dict[str, float],
                 title: Optional[str] = None,
                 width: int = 244,
                 height: int = 54,
                 **node_data_kwargs) -> DifyNode:
        """
        添加节点到Dify工作流中
        
        Args:
            id: 节点ID
            type: 节点类型 (start, llm, knowledge-retrieval, end等)
            position: 节点位置 {"x": 100, "y": 200}
            title: 节点标题，如果不提供则使用默认值
            width: 节点宽度
            height: 节点高度
            **node_data_kwargs: 节点特定的数据参数
            
        Returns:
            创建的DifyNode实例
        """
        # 创建节点数据
        node_data = create_dify_node_state(type, **node_data_kwargs)
        
        # 如果提供了title，更新节点数据
        if title:
            node_data.title = title
        
        # 创建节点
        node = DifyNode(
            id=id,
            type="custom",
            position=position,
            positionAbsolute=position.copy(),
            width=width,
            height=height,
            data=node_data.dict()
        )
        
        # 设置节点的源和目标位置（所有节点都使用相同的位置）
        node.sourcePosition = "right"
        node.targetPosition = "left"
        
        self.nodes.append(node)
        return node
    
    def _create_node_direct(self, id: str, type: str, position: Dict[str, float], node_data: Dict[str, Any], parent_id: Optional[str] = None) -> DifyNode:
        """
        直接创建节点，跳过数据验证（用于处理已验证的Dify原生数据）
        
        Args:
            id: 节点ID
            type: 节点类型
            position: 节点位置
            node_data: 节点数据
            parent_id: 父节点ID（用于iteration等嵌套结构）
            
        Returns:
            创建的DifyNode实例
        """
        # 根据节点类型确定尺寸（从 data 中获取，如果有的话）
        node_type = node_data.get("type", "")
        
        # 使用 data 中的 width 和 height（如果存在）
        width = node_data.get("width", 244)
        height = node_data.get("height", 54)
        
        # 特殊节点类型的默认尺寸和属性
        custom_type = "custom"
        draggable = None
        selectable = None
        
        if node_type == "iteration" and width == 244:
            # iteration 节点作为容器需要更大的尺寸
            width = 497
            height = 268
        elif node_type == "iteration-start":
            # iteration-start 节点的特殊属性
            custom_type = "custom-iteration-start"
            width = 55
            height = 60
            draggable = False
            selectable = False
        
        # 设置 zIndex：iteration 内部的节点需要更高的层级（1002）
        zIndex = 1002 if parent_id else None
        
        # 创建节点
        node = DifyNode(
            id=id,
            type=custom_type,
            position=position,
            positionAbsolute=position.copy(),
            width=width,
            height=height,
            data=node_data,
            parentId=parent_id,  # 设置父节点ID
            zIndex=zIndex,  # 设置层级
            draggable=draggable,
            selectable=selectable
        )
        
        # 设置节点的源和目标位置（所有节点都使用相同的位置）
        node.sourcePosition = "right"
        node.targetPosition = "left"
        
        return node
    
    def add_edge(self, 
                 source: str, 
                 target: str,
                 source_handle: str = "source",
                 target_handle: str = "target",
                 edge_id: str = None,
                 edge_data: Dict[str, Any] = None) -> DifyEdge:
        """
        添加边连接两个节点
        
        Args:
            source: 源节点ID
            target: 目标节点ID
            source_handle: 源句柄（默认为"source"，if-else节点可能是"true"或"false"）
            target_handle: 目标句柄（默认为"target"）
            edge_id: 可选的自定义边ID
            edge_data: 可选的边数据字典（包含 iteration_id, isInIteration 等）
            
        Returns:
            创建的DifyEdge实例
        """
        # 生成边ID（如果未提供）
        if not edge_id:
            edge_id = f"{source}-{source_handle}-{target}-{target_handle}"
            
        # 获取节点类型和iteration信息
        source_node = next((n for n in self.nodes if n.id == source), None)
        target_node = next((n for n in self.nodes if n.id == target), None)
        
        # 构建边数据
        if edge_data is None:
            edge_data = {}
        
        # 设置基本字段（如果未提供）
        if "isInLoop" not in edge_data:
            edge_data["isInLoop"] = False
        if "sourceType" not in edge_data:
            edge_data["sourceType"] = source_node.data.get("type", "unknown") if source_node else "unknown"
        if "targetType" not in edge_data:
            edge_data["targetType"] = target_node.data.get("type", "unknown") if target_node else "unknown"
        
        # 检测是否在iteration内：如果源节点或目标节点有parentId，则这条边在iteration内
        is_in_iteration = False
        if source_node and source_node.parentId:
            is_in_iteration = True
            if "isInIteration" not in edge_data:
                edge_data["isInIteration"] = True
            if "iteration_id" not in edge_data:
                edge_data["iteration_id"] = source_node.parentId
        elif target_node and target_node.parentId:
            is_in_iteration = True
            if "isInIteration" not in edge_data:
                edge_data["isInIteration"] = True
            if "iteration_id" not in edge_data:
                edge_data["iteration_id"] = target_node.parentId
        
        # 设置 zIndex：iteration 内部的边需要更高的层级（1002）以在容器上方显示
        zIndex = 1002 if is_in_iteration else 0
        
        edge = DifyEdge(
            id=edge_id,
            source=source,
            target=target,
            sourceHandle=source_handle,
            targetHandle=target_handle,
            data=edge_data,
            zIndex=zIndex
        )
        
        self.edges.append(edge)
        return edge
    
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        # 如果有原始数据，使用原始数据作为基础
        if hasattr(self, '_original_data') and self._original_data:
            result = self._original_data.copy()
            
            # 更新图数据 - 使用exclude_none和by_alias确保完整性
            result["workflow"]["graph"]["edges"] = [
                edge.dict(exclude_none=False, by_alias=True) for edge in self.edges
            ]
            
            # 序列化节点并清理不应该在data里的字段
            nodes_list = []
            for node in self.nodes:
                node_dict = node.dict(exclude_none=False, by_alias=True)
                
                # 清理 iteration-start 节点的 data 中不应该存在的字段
                if node_dict.get('data', {}).get('type') == 'iteration-start':
                    # iteration-start 的 data 里不应该有 parentId 和 iteration_id
                    node_dict['data'].pop('parentId', None)
                    node_dict['data'].pop('iteration_id', None)
                
                # 清理节点层级的 None 值字段（除非是明确设置为 False 的字段）
                # 只有 iteration-start 节点才应该有 draggable=False, selectable=False
                if node_dict.get('data', {}).get('type') != 'iteration-start':
                    # 对于普通节点，移除值为 None 的 draggable 和 selectable
                    if node_dict.get('draggable') is None:
                        node_dict.pop('draggable', None)
                    if node_dict.get('selectable') is None:
                        node_dict.pop('selectable', None)
                
                nodes_list.append(node_dict)
            
            result["workflow"]["graph"]["nodes"] = nodes_list
            
            # 更新应用信息
            result["app"]["name"] = self.app.name
            result["app"]["description"] = self.app.description
            result["app"]["icon"] = self.app.icon
            result["app"]["icon_background"] = self.app.icon_background
            
            return result
        else:
            # 序列化节点并清理不应该在data里的字段
            nodes_list = []
            for node in self.nodes:
                node_dict = node.dict(exclude_none=False, by_alias=True)
                
                # 清理 iteration-start 节点的 data 中不应该存在的字段
                if node_dict.get('data', {}).get('type') == 'iteration-start':
                    # iteration-start 的 data 里不应该有 parentId 和 iteration_id
                    node_dict['data'].pop('parentId', None)
                    node_dict['data'].pop('iteration_id', None)
                
                # 清理节点层级的 None 值字段（除非是明确设置为 False 的字段）
                # 只有 iteration-start 节点才应该有 draggable=False, selectable=False
                if node_dict.get('data', {}).get('type') != 'iteration-start':
                    # 对于普通节点，移除值为 None 的 draggable 和 selectable
                    if node_dict.get('draggable') is None:
                        node_dict.pop('draggable', None)
                    if node_dict.get('selectable') is None:
                        node_dict.pop('selectable', None)
                
                nodes_list.append(node_dict)
            
            # 创建图模型
            graph = DifyGraphModel(
                edges=[edge.dict(exclude_none=False, by_alias=True) for edge in self.edges],
                nodes=nodes_list,
                viewport=self.workflow.graph.viewport
            )
            
            # 更新工作流图
            self.workflow.graph = graph
            
            # 创建完整配置
            config = DifyWorkflowConfig(
                app=self.app,
                workflow=self.workflow
            )
            
            return config.dict(exclude_none=False, by_alias=True)
    
    def to_yaml(self, **yaml_kwargs) -> str:
        """
        导出为YAML格式
        
        Args:
            **yaml_kwargs: yaml.dump的参数
            
        Returns:
            YAML格式的字符串
        """
        # 设置默认的YAML导出参数
        default_kwargs = {
            "default_flow_style": False,
            "allow_unicode": True,
            "sort_keys": False,
            "indent": 2
        }
        default_kwargs.update(yaml_kwargs)
        
        # 获取字典并清理 None 值
        data_dict = self.to_dict()
        self._clean_none_values(data_dict)
        
        return yaml.dump(data_dict, **default_kwargs)
    
    def _clean_none_values(self, obj):
        """
        递归清理字典中的 None 值（但保留明确设置为 False 的值）
        特殊规则：只有 iteration-start 节点才保留 draggable=False
        """
        if isinstance(obj, dict):
            # 获取需要删除的键
            keys_to_delete = []
            
            for key, value in obj.items():
                if value is None:
                    # 特殊处理：如果是节点且是 iteration-start 类型，保留某些字段
                    if key in ['draggable', 'selectable', 'zIndex', 'parentId']:
                        # 检查是否是 iteration-start 节点
                        node_type = obj.get('data', {}).get('type') if isinstance(obj.get('data'), dict) else None
                        
                        # iteration-start 的 draggable 和 selectable 应该是 False，不是 None
                        # 其他节点的 None 值都应该删除
                        if node_type != 'iteration-start':
                            keys_to_delete.append(key)
                    else:
                        keys_to_delete.append(key)
                elif isinstance(value, (dict, list)):
                    self._clean_none_values(value)
            
            for key in keys_to_delete:
                del obj[key]
                
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._clean_none_values(item)
    
    def save_yaml(self, file_path: str, **yaml_kwargs):
        """
        保存为YAML文件
        
        Args:
            file_path: 文件路径
            **yaml_kwargs: yaml.dump的参数
        """
        yaml_content = self.to_yaml(**yaml_kwargs)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
    
    @classmethod
    def from_yaml(cls, yaml_content: str) -> 'DifyGraph':
        """
        从YAML内容创建DifyGraph实例
        
        Args:
            yaml_content: YAML格式的内容
            
        Returns:
            DifyGraph实例
        """
        data = yaml.safe_load(yaml_content)
        
        # 创建实例
        builder = cls(
            app_name=data.get("app", {}).get("name", ""),
            app_description=data.get("app", {}).get("description", ""),
            app_icon=data.get("app", {}).get("icon", "🤖"),
            app_icon_background=data.get("app", {}).get("icon_background", "#FFEAD5")
        )
        
        # 保存原始数据以便完整重建
        builder._original_data = data
        
        # 加载工作流配置
        workflow_data = data.get("workflow", {})
        builder.workflow = DifyWorkflow(**workflow_data)
        
        # 加载节点和边
        graph_data = workflow_data.get("graph", {})
        
        # 加载节点
        for node_data in graph_data.get("nodes", []):
            node = DifyNode(**node_data)
            builder.nodes.append(node)
        
        # 加载边
        for edge_data in graph_data.get("edges", []):
            edge = DifyEdge(**edge_data)
            builder.edges.append(edge)
        
        return builder
    
    
    @classmethod
    def from_yaml_file(cls, file_path: str) -> 'DifyGraph':
        """
        从YAML文件创建DifyGraph实例
        
        Args:
            file_path: YAML文件路径
            
        Returns:
            DifyGraph实例
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        return cls.from_yaml(yaml_content)