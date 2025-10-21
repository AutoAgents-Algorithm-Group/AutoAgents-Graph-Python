from typing import Optional, Dict, Any, Union
from pydantic import BaseModel
from ..engine.agentify.services import AgentifyGraph
from ..engine.dify.services import DifyGraph
from .config import AgentifyConfig, DifyConfig


class NL2Workflow:
    """
    自然语言到工作流的转换器，支持多个平台
    """
    
    def __init__(self, 
                 platform: str,
                 config: Union[AgentifyConfig, DifyConfig]):
        """
        初始化NL2Workflow
        
        Args:
            platform: 目标平台 ("agentify" 或 "dify")
            config: 平台配置对象 (AgentifyConfig 或 DifyConfig)
        """
        self.platform = platform.lower()
        
        if self.platform not in ["agentify", "dify"]:
            raise ValueError(f"Unsupported platform: {platform}. Supported platforms: 'agentify', 'dify'")
        
        if config is None:
            raise ValueError(f"config is required for {platform} platform")
        
        # 初始化对应平台的图构建器
        if self.platform == "agentify":
            if not isinstance(config, AgentifyConfig):
                raise TypeError("For agentify platform, config must be an instance of AgentifyConfig")
            
            self.graph = AgentifyGraph(
                personal_auth_key=config.personal_auth_key,
                personal_auth_secret=config.personal_auth_secret,
                jwt_token=config.jwt_token,
                base_url=config.base_url
            )
        
        elif self.platform == "dify":
            if not isinstance(config, DifyConfig):
                raise TypeError("For dify platform, config must be an instance of DifyConfig")
            
            self.graph = DifyGraph(
                app_name=config.app_name,
                app_description=config.app_description,
                app_icon=config.app_icon,
                app_icon_background=config.app_icon_background
            )
    
    def _get_node_type_from_state(self, state: BaseModel) -> str:
        """
        根据State类型获取对应的节点类型
        
        Args:
            state: BaseModel实例
            
        Returns:
            节点类型字符串
        """
        # AgentsPro State类型到节点类型的映射
        agentify_state_mapping = {
            "QuestionInputState": "questionInput",
            "AiChatState": "aiChat", 
            "ConfirmReplyState": "confirmreply",
            "KnowledgeSearchState": "knowledgesSearch",
            "HttpInvokeState": "httpInvoke",
            "Pdf2MdState": "pdf2md",
            "AddMemoryVariableState": "addMemoryVariable",
            "InfoClassState": "infoClass",
            "CodeFragmentState": "codeFragment",
            "ForEachState": "forEach"
        }
        
        # Dify State类型到节点类型的映射（只使用DifyTypes）
        dify_state_mapping = {
            "DifyStartState": "start",
            "DifyLLMState": "llm",
            "DifyKnowledgeRetrievalState": "knowledge-retrieval",
            "DifyEndState": "end",
            "DifyAnswerState": "answer",
            "DifyCodeState": "code",
            "DifyToolState": "tool",
            "DifyIfElseState": "if-else"
        }
        
        state_class_name = state.__class__.__name__
        
        if self.platform == "agentify":
            return agentify_state_mapping.get(state_class_name, "unknown")
        elif self.platform == "dify":
            return dify_state_mapping.get(state_class_name, "unknown")
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")
    
    def add_node(self, 
                 id: str,
                 state: BaseModel,
                 position: Optional[Dict[str, float]] = None) -> Any:
        """
        通用节点添加方法，根据传入的BaseModel自动判断节点类型
        
        Args:
            id: 节点ID
            state: BaseModel实例，用于确定节点类型和配置
            position: 节点位置
            
        Returns:
            创建的节点实例
        """
        if not isinstance(state, BaseModel):
            raise ValueError("state must be a BaseModel instance")
        
        if self.platform == "agentify":
            return self.graph.add_node(
                id=id, 
                position=position, 
                state=state
            )
        
        elif self.platform == "dify":
            # Dify平台只使用DifyTypes中定义的类型
            node_type = self._get_node_type_from_state(state)
            
            if node_type == "unknown":
                raise ValueError(f"Unsupported state type for Dify platform: {state.__class__.__name__}. Please use DifyTypes (DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState, DifyEndState, DifyAnswerState, DifyCodeState, DifyToolState, DifyIfElseState).")
            
            # 直接使用Dify节点数据
            node_data = state.dict()
            
            # 创建节点时直接使用节点数据
            node = self.graph._create_node_direct(id, node_type, position or {"x": 100, "y": 200}, node_data)
            self.graph.nodes.append(node)
            return node
    
    
    def add_edge(self, 
                source: str, 
                target: str,
                source_handle: str = "",
                target_handle: str = "") -> Any:
        """
        添加连接边
        
        Args:
            source: 源节点ID
            target: 目标节点ID
            source_handle: 源句柄
            target_handle: 目标句柄
            
        Returns:
            创建的边实例
        """
        return self.graph.add_edge(
            source=source, 
            target=target, 
            source_handle=source_handle, 
            target_handle=target_handle
        )
    
    def compile(self, **kwargs) -> Union[None, str]:
        """
        编译工作流
        
        Args:
            **kwargs: 编译参数
            
        Returns:
            AgentsPro平台返回None（直接发布），Dify平台返回YAML字符串
        """
        if self.platform == "agentify":
            # AgentsPro平台直接编译发布
            return self.graph.compile(**kwargs)
        
        elif self.platform == "dify":
            # Dify平台返回YAML配置
            return self.graph.to_yaml()
    
    def save(self, file_path: str, **kwargs):
        """
        保存工作流到文件
        
        Args:
            file_path: 文件路径
            **kwargs: 保存参数
        """
        if self.platform == "agentify":
            # AgentsPro平台保存JSON格式
            import json
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "nodes": [node.to_dict() for node in self.graph.nodes],
                    "edges": [edge.to_dict() for edge in self.graph.edges],
                    "viewport": self.graph.viewport
                }, f, indent=2, ensure_ascii=False)
        
        elif self.platform == "dify":
            # Dify平台保存YAML格式
            self.graph.save_yaml(file_path, **kwargs)
    
    def get_platform(self) -> str:
        """获取当前平台"""
        return self.platform
    
    def get_graph(self) -> Union[AgentifyGraph, DifyGraph]:
        """获取底层图对象"""
        return self.graph