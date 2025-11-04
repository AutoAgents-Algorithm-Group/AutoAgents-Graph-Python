import yaml
import uuid
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
        
        # 设置节点的源和目标位置
        if type == "start":
            node.sourcePosition = "right"
            node.targetPosition = "left"
        elif type == "end":
            node.sourcePosition = "right"
            node.targetPosition = "left"
        else:
            node.sourcePosition = "right"
            node.targetPosition = "left"
        
        self.nodes.append(node)
        return node
    
    def _create_node_direct(self, id: str, type: str, position: Dict[str, float], node_data: Dict[str, Any]) -> DifyNode:
        """
        直接创建节点，跳过数据验证（用于处理已验证的Dify原生数据）
        
        Args:
            id: 节点ID
            type: 节点类型
            position: 节点位置
            node_data: 节点数据
            
        Returns:
            创建的DifyNode实例
        """
        # 创建节点
        node = DifyNode(
            id=id,
            type="custom",
            position=position,
            positionAbsolute=position.copy(),
            width=244,
            height=54,
            data=node_data
        )
        
        # 设置节点的源和目标位置
        if type == "start":
            node.sourcePosition = "right"
            node.targetPosition = "left"
        elif type == "end":
            node.sourcePosition = "right"
            node.targetPosition = "left"
        else:
            node.sourcePosition = "right"
            node.targetPosition = "left"
        
        return node
    
    def add_edge(self, 
                 source: str, 
                 target: str,
                 source_handle: str = "",
                 target_handle: str = "") -> DifyEdge:
        """
        添加边连接两个节点
        
        Args:
            source: 源节点ID
            target: 目标节点ID
            source_handle: 源句柄（默认为"source"）
            target_handle: 目标句柄（默认为"target"）
            
        Returns:
            创建的DifyEdge实例
        """
        # Dify平台的默认句柄处理
        if not source_handle:
            source_handle = "source"
        if not target_handle:
            target_handle = "target"
            
        # 生成边ID
        edge_id = f"{source}-{source_handle}-{target}-{target_handle}"
        
        # 获取节点类型用于边数据
        source_node = next((n for n in self.nodes if n.id == source), None)
        target_node = next((n for n in self.nodes if n.id == target), None)
        
        edge_data = {
            "isInLoop": False,
            "sourceType": source_node.data.get("type", "unknown") if source_node else "unknown",
            "targetType": target_node.data.get("type", "unknown") if target_node else "unknown"
        }
        
        edge = DifyEdge(
            id=edge_id,
            source=source,
            target=target,
            sourceHandle=source_handle,
            targetHandle=target_handle,
            data=edge_data
        )
        
        self.edges.append(edge)
        return edge
    
    def set_viewport(self, x: float = 0, y: float = 0, zoom: float = 1.0):
        """设置视口"""
        self.workflow.graph.viewport = {"x": x, "y": y, "zoom": zoom}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        # 如果有原始数据，使用原始数据作为基础
        if hasattr(self, '_original_data') and self._original_data:
            result = self._original_data.copy()
            
            # 更新图数据
            result["workflow"]["graph"]["edges"] = [edge.dict() for edge in self.edges]
            result["workflow"]["graph"]["nodes"] = [node.dict() for node in self.nodes]
            
            # 更新应用信息
            result["app"]["name"] = self.app.name
            result["app"]["description"] = self.app.description
            result["app"]["icon"] = self.app.icon
            result["app"]["icon_background"] = self.app.icon_background
            
            return result
        else:
            # 创建图模型
            graph = DifyGraphModel(
                edges=[edge.dict() for edge in self.edges],
                nodes=[node.dict() for node in self.nodes],
                viewport=self.workflow.graph.viewport
            )
            
            # 更新工作流图
            self.workflow.graph = graph
            
            # 创建完整配置
            config = DifyWorkflowConfig(
                app=self.app,
                workflow=self.workflow
            )
            
            return config.dict()
    
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
        
        return yaml.dump(self.to_dict(), **default_kwargs)
    
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
    
    def add_dependency(self, plugin_id: str):
        """添加插件依赖"""
        if not hasattr(self, 'dependencies'):
            self.dependencies = []
        
        dependency = {
            "current_identifier": None,
            "type": "marketplace",
            "value": {
                "marketplace_plugin_unique_identifier": plugin_id
            }
        }
        self.dependencies.append(dependency)
    
    def set_environment_variable(self, name: str, value: str, description: str = ""):
        """设置环境变量"""
        if not hasattr(self.workflow, 'environment_variables'):
            self.workflow.environment_variables = []
        
        env_var = {
            "description": description,
            "id": str(uuid.uuid4()),
            "name": name,
            "selector": ["env", name],
            "value": value,
            "value_type": "string"
        }
        self.workflow.environment_variables.append(env_var)
    
    def enable_file_upload(self, allowed_extensions: List[str] = None, 
                          allowed_types: List[str] = None, 
                          number_limits: int = 3):
        """启用文件上传功能"""
        if allowed_extensions is None:
            allowed_extensions = [".JPG", ".JPEG", ".PNG", ".GIF", ".WEBP", ".SVG"]
        if allowed_types is None:
            allowed_types = ["image"]
        
        self.workflow.features["file_upload"]["enabled"] = True
        self.workflow.features["file_upload"]["allowed_file_extensions"] = allowed_extensions
        self.workflow.features["file_upload"]["allowed_file_types"] = allowed_types
        self.workflow.features["file_upload"]["number_limits"] = number_limits
    
    def set_opening_statement(self, statement: str):
        """设置开场白"""
        self.workflow.features["opening_statement"] = statement
    
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