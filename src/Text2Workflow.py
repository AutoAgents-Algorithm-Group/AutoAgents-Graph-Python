from typing import Optional, Dict, Any, Union
from pydantic import BaseModel
from .agentify.FlowGraph import FlowGraph
from .dify.DifyGraph import DifyGraphBuilder


class Text2Workflow:
    """
    文本到工作流的统一转换器，支持多个平台
    """
    
    def __init__(self, 
                 platform: str = "agentify",
                 personal_auth_key: Optional[str] = None,
                 personal_auth_secret: Optional[str] = None,
                 base_url: str = "https://uat.agentspro.cn",
                 **platform_kwargs):
        """
        初始化Text2Workflow
        
        Args:
            platform: 目标平台 ("agentify" 或 "dify")
            personal_auth_key: AgentsPro平台的认证密钥 (仅agentify平台需要)
            personal_auth_secret: AgentsPro平台的认证密码 (仅agentify平台需要)
            base_url: API基础URL (仅agentify平台需要)
            **platform_kwargs: 平台特定的参数
        """
        self.platform = platform.lower()
        
        if self.platform not in ["agentify", "dify"]:
            raise ValueError(f"Unsupported platform: {platform}. Supported platforms: 'agentify', 'dify'")
        
        # 初始化对应平台的图构建器
        if self.platform == "agentify":
            if not personal_auth_key or not personal_auth_secret:
                raise ValueError("AgentsPro platform requires personal_auth_key and personal_auth_secret")
            
            self.graph = FlowGraph(
                personal_auth_key=personal_auth_key,
                personal_auth_secret=personal_auth_secret,
                base_url=base_url
            )
        
        elif self.platform == "dify":
            # Dify平台的参数
            dify_kwargs = {
                "app_name": platform_kwargs.get("app_name", "AutoAgents工作流"),
                "app_description": platform_kwargs.get("app_description", "基于AutoAgents SDK构建的工作流"),
                "app_icon": platform_kwargs.get("app_icon", "🤖"),
                "app_icon_background": platform_kwargs.get("app_icon_background", "#FFEAD5")
            }
            
            self.graph = DifyGraphBuilder(**dify_kwargs)
    
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
        
        # Dify State类型到节点类型的映射
        dify_state_mapping = {
            "QuestionInputState": "start",
            "AiChatState": "llm",
            "ConfirmReplyState": "end", 
            "KnowledgeSearchState": "knowledge-retrieval",
            "DifyStartNodeData": "start",
            "DifyLLMNodeData": "llm",
            "DifyKnowledgeRetrievalNodeData": "knowledge-retrieval",
            "DifyEndNodeData": "end"
        }
        
        state_class_name = state.__class__.__name__
        
        if self.platform == "agentify":
            return agentify_state_mapping.get(state_class_name, "unknown")
        elif self.platform == "dify":
            return dify_state_mapping.get(state_class_name, "unknown")
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")
    
    def add_node(self, 
                 node_id: str,
                 state: BaseModel,
                 position: Optional[Dict[str, float]] = None) -> Any:
        """
        通用节点添加方法，根据传入的BaseModel自动判断节点类型
        
        Args:
            node_id: 节点ID
            state: BaseModel实例，用于确定节点类型和配置
            position: 节点位置
            
        Returns:
            创建的节点实例
        """
        if not isinstance(state, BaseModel):
            raise ValueError("state must be a BaseModel instance")
        
        if self.platform == "agentify":
            # AgentsPro平台直接使用FlowGraph的add_node
            return self.graph.add_node(
                id=node_id,
                position=position or {"x": 100, "y": 200},
                state=state
            )
        
        elif self.platform == "dify":
            # Dify平台需要转换状态到节点类型
            node_type = self._get_node_type_from_state(state)
            
            # 处理特殊的Dify原生节点数据
            if state.__class__.__name__.startswith('Dify'):  # Dify原生节点数据
                # 直接使用Dify节点数据，跳过create_dify_node_data
                node_data = state.dict()
                # 创建节点时直接使用节点数据
                node = self.graph._create_node_direct(node_id, node_type, position or {"x": 100, "y": 200}, node_data)
                self.graph.nodes.append(node)
                return node
            else:
                # 从AgentsPro状态转换为Dify节点数据
                node_data = self._convert_agentify_state_to_dify_data(state, node_type)
                
                return self.graph.add_node(
                    node_id=node_id,
                    node_type=node_type,
                    position=position or {"x": 100, "y": 200},
                    **node_data
                )
    
    def _convert_agentify_state_to_dify_data(self, state: BaseModel, node_type: str) -> Dict[str, Any]:
        """
        将AgentsPro状态转换为Dify节点数据
        
        Args:
            state: AgentsPro状态实例
            node_type: Dify节点类型
            
        Returns:
            Dify节点数据字典
        """
        state_dict = state.dict() if hasattr(state, 'dict') else {}
        
        if node_type == "llm":
            # AiChatState -> LLM节点
            return {
                "model": {
                    "completion_params": {"temperature": state_dict.get("temperature", 0.7)},
                    "mode": "chat",
                    "name": state_dict.get("model", "doubao-deepseek-v3"),
                    "provider": ""
                },
                "prompt_template": [{"role": "system", "text": state_dict.get("text", "")}],
                "title": "LLM"
            }
        
        elif node_type == "knowledge-retrieval":
            # KnowledgeSearchState -> 知识检索节点
            return {
                "dataset_ids": state_dict.get("datasets", []),
                "multiple_retrieval_config": {
                    "reranking_enable": state_dict.get("enableRerank", False),
                    "top_k": state_dict.get("topK", 4)
                },
                "title": "知识检索"
            }
        
        elif node_type == "start":
            # QuestionInputState -> 开始节点
            return {
                "title": "开始",
                "variables": []
            }
        
        elif node_type == "end":
            # ConfirmReplyState -> 结束节点
            return {
                "title": "结束",
                "outputs": []
            }
        
        else:
            # 其他类型使用默认配置
            return {"title": node_type.title()}
    
    
    
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
        if self.platform == "agentify":
            return self.graph.add_edge(source, target, source_handle, target_handle)
        
        elif self.platform == "dify":
            # Dify平台的默认句柄处理
            if not source_handle:
                source_handle = "source"
            if not target_handle:
                target_handle = "target"
            
            return self.graph.add_edge(source, target, source_handle, target_handle)
    
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
    
    def get_graph(self) -> Union[FlowGraph, DifyGraphBuilder]:
        """获取底层图对象"""
        return self.graph
