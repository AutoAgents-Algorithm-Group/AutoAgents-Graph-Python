# Dify节点注册表
# 定义了Dify平台支持的所有节点类型及其配置

DIFY_NODE_TEMPLATES = {
    "start": {
        "name": "开始",
        "description": "工作流的起始节点，定义输入变量",
        "category": "系统节点",
        "state_class": "DifyStartState",
        "default_params": {
            "title": "开始",
            "desc": "",
            "selected": False,
            "type": "start",
            "variables": [
                {
                    "label": "系统输入",
                    "max_length": 48000,
                    "options": [],
                    "required": True,
                    "type": "text-input",
                    "variable": "sys_input"
                }
            ]
        },
        "param_mapping": {
            "title": "title",
            "variables": "variables",
            "desc": "desc"
        }
    },
    
    "llm": {
        "name": "LLM",
        "description": "大语言模型对话节点，支持各种AI模型调用",
        "category": "AI节点",
        "state_class": "DifyLLMState",
        "default_params": {
            "title": "LLM",
            "desc": "",
            "selected": False,
            "type": "llm",
            "model": {
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "",
                "provider": ""
            },
            "prompt_template": [{"role": "system", "text": ""}],
            "context": {"enabled": False, "variable_selector": []},
            "variables": [],
            "vision": {"enabled": False},
            "structured_output": None,
            "structured_output_enabled": False
        },
        "param_mapping": {
            "title": "title",
            "model": "model",
            "prompt_template": "prompt_template",
            "context": "context",
            "variables": "variables",
            "desc": "desc",
            # 迭代相关字段（用于iteration内的节点）
            "isInIteration": "isInIteration",
            "iteration_id": "iteration_id",
            "isInLoop": "isInLoop"
        }
    },
    
    "knowledge-retrieval": {
        "name": "知识检索",
        "description": "从知识库中检索相关信息",
        "category": "知识库",
        "state_class": "DifyKnowledgeRetrievalState",
        "default_params": {
            "title": "知识检索",
            "desc": "",
            "selected": False,
            "type": "knowledge-retrieval",
            "dataset_ids": [],
            "query_variable_selector": [],
            "retrieval_mode": "multiple",
            "multiple_retrieval_config": {
                "reranking_enable": False,
                "top_k": 4
            }
        },
        "param_mapping": {
            "title": "title",
            "dataset_ids": "dataset_ids",
            "query_variable_selector": "query_variable_selector",
            "multiple_retrieval_config": "multiple_retrieval_config",
            "desc": "desc"
        }
    },
    
    "code": {
        "name": "代码执行",
        "description": "执行Python或JavaScript代码",
        "category": "工具节点",
        "state_class": "DifyCodeState",
        "default_params": {
            "title": "代码执行",
            "desc": "",
            "selected": False,
            "type": "code",
            "code": "",
            "code_language": "python3",
            "outputs": {},
            "variables": []
        },
        "param_mapping": {
            "title": "title",
            "code": "code",
            "code_language": "code_language",
            "outputs": "outputs",
            "variables": "variables",
            "desc": "desc"
        }
    },
    
    "tool": {
        "name": "工具调用",
        "description": "调用外部工具和API",
        "category": "工具节点",
        "state_class": "DifyToolState",
        "default_params": {
            "title": "工具调用",
            "desc": "",
            "selected": False,
            "type": "tool",
            "provider_id": "",
            "provider_name": "",
            "provider_type": "builtin",
            "tool_configurations": {},
            "tool_description": "",
            "tool_label": "",
            "tool_name": "",
            "tool_parameters": {}
        },
        "param_mapping": {
            "title": "title",
            "provider_id": "provider_id",
            "provider_name": "provider_name",
            "provider_type": "provider_type",
            "tool_configurations": "tool_configurations",
            "tool_description": "tool_description",
            "tool_label": "tool_label",
            "tool_name": "tool_name",
            "tool_parameters": "tool_parameters",
            "desc": "desc"
        }
    },
    
    "if-else": {
        "name": "条件分支",
        "description": "基于条件进行流程分支",
        "category": "逻辑节点",
        "state_class": "DifyIfElseState",
        "default_params": {
            "title": "条件分支",
            "desc": "",
            "selected": False,
            "type": "if-else",
            "conditions": [],
            "logical_operator": "and"
        },
        "param_mapping": {
            "title": "title",
            "conditions": "conditions",
            "logical_operator": "logical_operator",
            "desc": "desc"
        }
    },
    
    "answer": {
        "name": "直接回复",
        "description": "直接向用户输出回复内容",
        "category": "输出节点",
        "state_class": "DifyAnswerState",
        "default_params": {
            "title": "直接回复",
            "desc": "",
            "selected": False,
            "type": "answer",
            "answer": "",
            "variables": []
        },
        "param_mapping": {
            "title": "title",
            "answer": "answer",
            "variables": "variables",
            "desc": "desc"
        }
    },
    
    "end": {
        "name": "结束",
        "description": "工作流的结束节点，定义输出变量",
        "category": "系统节点",
        "state_class": "DifyEndState",
        "default_params": {
            "title": "结束",
            "desc": "",
            "selected": False,
            "type": "end",
            "outputs": []
        },
        "param_mapping": {
            "title": "title",
            "outputs": "outputs",
            "desc": "desc"
        }
    },
    
    "iteration": {
        "name": "迭代",
        "description": "循环遍历数组数据，对每个元素执行相同的操作",
        "category": "逻辑节点",
        "state_class": "DifyIterationState",
        "default_params": {
            "title": "迭代",
            "desc": "",
            "selected": False,
            "type": "iteration",
            "error_handle_mode": "terminated",
            "input_parameters": [],
            "is_array_input": True,
            "is_parallel": False,
            "iterator_selector": [],
            "output_selector": [],
            "output_type": "array[string]",
            "parallel_nums": 10,
            "start_node_id": ""
        },
        "param_mapping": {
            "title": "title",
            "error_handle_mode": "error_handle_mode",
            "input_parameters": "input_parameters",
            "is_array_input": "is_array_input",
            "is_parallel": "is_parallel",
            "iterator_selector": "iterator_selector",
            "output_selector": "output_selector",
            "output_type": "output_type",
            "parallel_nums": "parallel_nums",
            "start_node_id": "start_node_id",
            "desc": "desc",
            # iteration 容器节点的尺寸
            "width": "width",
            "height": "height"
        }
    },
    
    "iteration-start": {
        "name": "迭代开始",
        "description": "迭代块的起始节点，标记迭代循环的开始",
        "category": "系统节点",
        "state_class": "DifyIterationStartState",
        "default_params": {
            "title": "",
            "desc": "",
            "selected": False,
            "type": "iteration-start",
            "isInIteration": True
            # 注意：iteration_id 和 parentId 是节点层级属性，不在 State 的 data 中
        },
        "param_mapping": {
            "title": "title",
            "isInIteration": "isInIteration",
            "desc": "desc"
            # 注意：不映射 iteration_id 和 parentId，它们不是 State 的字段
        }
    },
    
    # 扩展节点类型 
    "http-request": {
        "name": "HTTP请求",
        "description": "发送HTTP请求到外部API",
        "category": "工具节点", 
        "state_class": "DifyHttpRequestState",
        "default_params": {
            "title": "HTTP请求",
            "desc": "",
            "selected": False,
            "type": "http-request",
            "method": "POST",
            "url": "",
            "headers": {},
            "params": {},
            "body": {},
            "timeout": 30
        },
        "param_mapping": {
            "title": "title",
            "method": "method",
            "url": "url", 
            "headers": "headers",
            "params": "params",
            "body": "body",
            "timeout": "timeout",
            "desc": "desc"
        }
    },
    
    "variable-assigner": {
        "name": "变量赋值",
        "description": "对工作流变量进行赋值操作",
        "category": "逻辑节点",
        "state_class": "DifyVariableAssignerState", 
        "default_params": {
            "title": "变量赋值",
            "desc": "",
            "selected": False,
            "type": "variable-assigner",
            "variables": []
        },
        "param_mapping": {
            "title": "title",
            "variables": "variables",
            "desc": "desc"
        }
    }
}


class DifyNodeRegistry:
    """Dify节点注册表管理器"""
    
    @staticmethod
    def get_node_template(node_type: str) -> dict:
        """
        获取指定节点类型的模板配置
        
        Args:
            node_type: 节点类型
            
        Returns:
            节点模板配置字典
            
        Raises:
            KeyError: 当节点类型不存在时
        """
        if node_type not in DIFY_NODE_TEMPLATES:
            raise KeyError(f"未知的Dify节点类型: {node_type}")
        return DIFY_NODE_TEMPLATES[node_type]
    
    @staticmethod
    def get_supported_node_types() -> list:
        """获取所有支持的节点类型列表"""
        return list(DIFY_NODE_TEMPLATES.keys())
    
    @staticmethod
    def get_node_categories() -> dict:
        """获取按分类组织的节点类型"""
        categories = {}
        for node_type, template in DIFY_NODE_TEMPLATES.items():
            category = template["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(node_type)
        return categories
    
    @staticmethod
    def extract_node_params(node_data: dict, node_type: str) -> dict:
        """
        根据注册表配置从节点数据中提取参数
        
        Args:
            node_data: 节点的data字段
            node_type: 节点类型
            
        Returns:
            提取的参数字典
        """
        template = DifyNodeRegistry.get_node_template(node_type)
        param_mapping = template.get("param_mapping", {})
        default_params = template.get("default_params", {})
        
        params = {}
        
        # 根据参数映射提取数据
        for param_key, data_key in param_mapping.items():
            if data_key in node_data:
                params[param_key] = node_data[data_key]
            elif param_key in default_params:
                params[param_key] = default_params[param_key]
        
        return params
    
    @staticmethod
    def get_state_class_name(node_type: str) -> str:
        """
        根据节点类型获取对应的State类名
        
        Args:
            node_type: 节点类型
            
        Returns:
            State类名
        """
        template = DifyNodeRegistry.get_node_template(node_type)
        return template["state_class"]
    
    @staticmethod
    def create_default_node_config(node_type: str, **overrides) -> dict:
        """
        创建节点的默认配置
        
        Args:
            node_type: 节点类型
            **overrides: 需要覆盖的参数
            
        Returns:
            节点配置字典
        """
        template = DifyNodeRegistry.get_node_template(node_type)
        config = template["default_params"].copy()
        config.update(overrides)
        return config
