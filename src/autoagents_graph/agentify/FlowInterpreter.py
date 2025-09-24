from typing import List
from .NodeRegistry import NODE_TEMPLATES
from .models.GraphTypes import (
    QuestionInputState, AiChatState, ConfirmReplyState, 
    KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,
    InfoClassState, CodeFragmentState, ForEachState, HttpInvokeState
)


class FlowInterpreter:
    """
    流程图解释器，负责将JSON格式的流程图数据转换为SDK代码
    """
    
    def __init__(self, auth_key: str, auth_secret: str, base_url: str = "https://uat.agentspro.cn"):
        self.auth_key = auth_key
        self.auth_secret = auth_secret
        self.base_url = base_url
    
    @staticmethod
    def _extract_custom_inputs(node_data: dict) -> dict:
        """提取用户自定义的inputs，包含所有用户明确指定的参数"""
        module_type = node_data.get("moduleType")
        template = NODE_TEMPLATES.get(module_type, {})
        template_inputs = template.get("inputs", [])
        node_inputs = node_data.get("inputs", [])
        
        custom_inputs = {}
        
        if module_type == "addMemoryVariable":
            # 特殊处理addMemoryVariable
            memory_vars = []
            for inp in node_inputs:
                if inp.get("type") == "agentMemoryVar":
                    memory_vars.append({
                        "key": inp.get("key"),
                        "value_type": inp.get("valueType", "String")
                    })
            return memory_vars
        
        # 创建模板字段的映射，包含类型信息
        template_fields = {}
        for template_input in template_inputs:
            key = template_input.get("key")
            template_fields[key] = {
                "default_value": template_input.get("value"),
                "type": template_input.get("type"),
                "keyType": template_input.get("keyType")
            }
        
        # 提取用户明确指定的参数值
        for node_input in node_inputs:
            key = node_input.get("key")
            value = node_input.get("value")
            
            # 跳过trigger相关的系统字段
            if key in template_fields:
                field_info = template_fields[key]
                key_type = field_info.get("keyType")
                field_type = field_info.get("type")
                
                # 跳过trigger类型的字段（这些是系统字段）
                if key_type in ["trigger", "triggerAny"]:
                    continue
                    
                # 跳过target类型但不是用户输入的字段
                if field_type == "target" and key not in ["text", "images", "files", "knSearch"]:
                    continue
            
            # 包含用户明确指定的所有参数值
            if "value" in node_input:
                custom_inputs[key] = value
                
        return custom_inputs
    
    @staticmethod
    def _format_value(value) -> str:
        """格式化Python值"""
        if isinstance(value, str):
            # 处理多行字符串
            if '\n' in value:
                # 使用三重引号处理多行字符串
                escaped_value = value.replace('\\', '\\\\').replace('"""', '\\"""')
                return f'"""{escaped_value}"""'
            else:
                # 处理单行字符串，转义引号
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"')
                return f'"{escaped_value}"'
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, list):
            return str(value)
        elif isinstance(value, dict):
            return str(value)
        else:
            return f'"{str(value)}"'
    
    @staticmethod
    def _sanitize_variable_name(node_id: str, module_type: str, node_counter: dict) -> str:
        """将节点ID转换为有效的Python变量名"""
        # 如果是有意义的ID（不包含连字符或UUID格式），直接使用
        if node_id and not any(char in node_id for char in ['-', ' ']) and node_id.replace('_', '').isalnum():
            return node_id
        
        # 根据模块类型生成有意义的变量名
        type_mapping = {
            "questionInput": "user_input",
            "aiChat": "ai_chat", 
            "confirmreply": "confirm_reply",
            "knowledgesSearch": "kb_search",
            "databaseQuery": "kb_search",  # 添加对databaseQuery的支持
            "pdf2md": "doc_parser",
            "addMemoryVariable": "memory_var",
            "infoClass": "info_class",
            "codeFragment": "code_fragment",
            "forEach": "for_each",
            "httpInvoke": "http_invoke"
        }
        
        base_name = type_mapping.get(module_type, "node")
        
        # 处理重复的变量名
        if base_name not in node_counter:
            node_counter[base_name] = 0
            return base_name
        else:
            node_counter[base_name] += 1
            return f"{base_name}_{node_counter[base_name]}"

    @staticmethod
    def _generate_node_code(node: dict, node_counter: dict) -> str:
        """生成单个节点的代码"""
        node_id = node.get("id")
        module_type = node["data"].get("moduleType")
        position = node.get("position", {"x": 0, "y": 0})
        
        # 生成有效的Python变量名
        var_name = FlowInterpreter._sanitize_variable_name(node_id, module_type, node_counter)
        
        # 根据module_type获取对应的State类名
        state_class_name = FlowInterpreter._get_state_class_name(module_type)
        if not state_class_name:
            raise ValueError(f"Unsupported module type: {module_type}")
        
        # 生成添加节点的代码，直接传递State类
        code_lines = []
        code_lines.append(f"    # 添加{module_type}节点")
        code_lines.append("    graph.add_node(")
        code_lines.append(f'        id="{var_name}",')
        code_lines.append(f"        position={position},")
        code_lines.append(f"        state={state_class_name}")
        code_lines.append("    )")
        
        return "\n".join(code_lines)
    
    @staticmethod
    def _get_state_class_name(module_type: str) -> str:
        """根据module_type获取对应的State类名称字符串"""
        state_name_mapping = {
            "questionInput": "QuestionInputState",
            "aiChat": "AiChatState",
            "confirmreply": "ConfirmReplyState",
            "knowledgesSearch": "KnowledgeSearchState",
            "databaseQuery": "KnowledgeSearchState",  # 添加对databaseQuery的支持
            "pdf2md": "Pdf2MdState",
            "addMemoryVariable": "AddMemoryVariableState",
            "infoClass": "InfoClassState",
            "codeFragment": "CodeFragmentState",
            "forEach": "ForEachState",
            "httpInvoke": "HttpInvokeState",
        }
        return state_name_mapping.get(module_type)

    @staticmethod
    def _get_state_class(module_type: str):
        """根据module_type获取对应的State类"""
        state_mapping = {
            "questionInput": QuestionInputState,
            "aiChat": AiChatState,
            "confirmreply": ConfirmReplyState,
            "knowledgesSearch": KnowledgeSearchState,
            "databaseQuery": KnowledgeSearchState,  # 添加对databaseQuery的支持(假装有)
            "pdf2md": Pdf2MdState,
            "addMemoryVariable": AddMemoryVariableState,
            "infoClass": InfoClassState,
            "codeFragment": CodeFragmentState,
            "forEach": ForEachState,
            "httpInvoke": HttpInvokeState,
        }
        return state_mapping.get(module_type)
    
    @staticmethod
    def _generate_edge_code(edge: dict, id_mapping: dict = None) -> str:
        """生成单个边的代码"""
        source = edge.get("source")
        target = edge.get("target")
        source_handle = edge.get("sourceHandle", "")
        target_handle = edge.get("targetHandle", "")
        
        # 如果提供了ID映射，则使用新的节点ID
        if id_mapping:
            source = id_mapping.get(source, source)
            target = id_mapping.get(target, target)
        
        return f'    graph.add_edge("{source}", "{target}", "{source_handle}", "{target_handle}")'
    
    def _generate_header_code(self) -> List[str]:
        """生成代码头部（导入和初始化部分）"""
        code_lines = []
        code_lines.append("from autoagents_graph.agentify import FlowGraph, START")
        code_lines.append("from autoagents_graph.agentify.models.GraphTypes import (")
        code_lines.append("    QuestionInputState, AiChatState, ConfirmReplyState,")
        code_lines.append("    KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,")
        code_lines.append("    InfoClassState, CodeFragmentState, ForEachState, HttpInvokeState")
        code_lines.append(")")
        code_lines.append("")
        code_lines.append("def main():")
        code_lines.append("    graph = FlowGraph(")
        code_lines.append(f'            personal_auth_key="{self.auth_key}",')
        code_lines.append(f'            personal_auth_secret="{self.auth_secret}",')
        code_lines.append(f'            base_url="{self.base_url}"')
        code_lines.append("        )")
        code_lines.append("")
        return code_lines
    
    @staticmethod
    def _generate_footer_code() -> List[str]:
        """生成代码尾部（编译和main函数）"""
        code_lines = []
        code_lines.append("")
        code_lines.append("    # 编译, 导入配置，点击确定")
        code_lines.append("    graph.compile(")
        code_lines.append('            name="从JSON生成的工作流",')
        code_lines.append('            intro="这是从JSON数据反向生成的工作流",')
        code_lines.append('            category="自动生成",')
        code_lines.append('            prologue="你好！这是自动生成的工作流。",')
        code_lines.append('            shareAble=True,')
        code_lines.append('            allowVoiceInput=False,')
        code_lines.append('            autoSendVoice=False')
        code_lines.append("        )")
        code_lines.append("")
        code_lines.append('if __name__ == "__main__":')
        code_lines.append("    main()")
        return code_lines
    
    def from_json_to_code(self, json_data: dict) -> str:
        """
        将JSON格式的流程图数据转换为SDK代码
        
        Args:
            json_data: 包含nodes和edges的JSON数据
            
        Returns:
            生成的Python SDK代码字符串
        """
        code_lines = []
        node_counter = {}  # 用于跟踪节点类型计数
        id_mapping = {}    # 原始ID到新ID的映射
        
        # 1. 生成头部代码
        code_lines.extend(self._generate_header_code())
        
        # 2. 先建立ID映射
        nodes = json_data.get("nodes", [])
        for node in nodes:
            node_id = node.get("id")
            module_type = node["data"].get("moduleType")
            var_name = FlowInterpreter._sanitize_variable_name(node_id, module_type, node_counter)
            id_mapping[node_id] = var_name
        
        # 重置计数器用于生成代码
        node_counter.clear()
        
        # 3. 生成节点代码
        code_lines.append("    # 添加节点")
        for node in nodes:
            code_lines.append(FlowInterpreter._generate_node_code(node, node_counter))
            code_lines.append("")
        
        # 4. 生成边代码
        code_lines.append("    # 添加连接边")
        edges = json_data.get("edges", [])
        for edge in edges:
            code_lines.append(FlowInterpreter._generate_edge_code(edge, id_mapping))
        
        # 5. 生成尾部代码
        code_lines.extend(self._generate_footer_code())
        
        return "\n".join(code_lines)