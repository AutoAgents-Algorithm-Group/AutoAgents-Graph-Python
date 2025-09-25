from typing import List
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
        node_inputs = node_data.get("inputs", [])
        
        custom_inputs = {}
        
        if module_type == "addMemoryVariable":
            # 特殊处理addMemoryVariable - 返回空字典，因为它没有特殊参数
            return custom_inputs
        
        # 提取用户明确指定的参数值，只提取非系统字段的重要参数
        for node_input in node_inputs:
            key = node_input.get("key")
            value = node_input.get("value")
            field_type = node_input.get("type", "")
            key_type = node_input.get("keyType", "")
            
            # 跳过trigger相关的系统字段
            if key_type in ["trigger", "triggerAny"]:
                continue
                
            # 跳过target类型的字段（这些是连接字段，不是配置参数）
            if field_type == "target":
                continue
            
            # 只包含有意义的配置参数
            meaningful_keys = {
                "inputText", "uploadFile", "uploadPicture", "fileUpload", "fileContrast",
                "initialInput", "stream", "pdf2mdType", "datasets", "similarity", 
                "vectorSimilarWeight", "topK", "expandChunks", "enablePermission",
                "enableRerank", "rerankModelType", "rerankTopK", "historyText",
                "model", "systemPrompt", "quotePrompt", "temperature", "topP", "maxToken",
                "text"  # 对于confirmreply的预设文本
            }
            
            # 包含有意义的参数，且值不为默认值的情况
            if key in meaningful_keys and "value" in node_input:
                # 过滤掉一些明显的默认值
                if key == "initialInput" and value is True:
                    continue  # 跳过默认的initialInput=True
                if key in ["switch", "switchAny"] and value is False:
                    continue  # 跳过默认的trigger值
                if key == "stream" and value is True:
                    continue  # 跳过默认的stream=True
                if key == "historyText" and value == 3:
                    continue  # 跳过默认的historyText=3
                if key == "topP" and value == 1:
                    continue  # 跳过默认的topP=1
                if key == "maxToken" and value == 5000:
                    continue  # 跳过默认的maxToken=5000
                if key == "similarity" and value == 0.3:
                    continue  # 跳过默认的similarity=0.3
                if key == "topK" and value == 5:
                    continue  # 跳过默认的topK=5
                if key == "vectorSimilarWeight" and value == 1:
                    continue  # 跳过默认的vectorSimilarWeight=1
                if key == "temperature" and value == 0.2:
                    continue  # 跳过默认的temperature=0.2
                if key == "rerankTopK" and value == 10:
                    continue  # 跳过默认的rerankTopK=10
                if key in ["expandChunks", "enablePermission", "enableRerank"] and value is False:
                    continue  # 跳过默认的False值
                if key == "text" and value == "":
                    continue  # 跳过空的text值
                if key == "datasets" and (value == [] or not value):
                    continue  # 跳过空的datasets
                if key == "systemPrompt" and value == "":
                    continue  # 跳过空的systemPrompt
                    
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
        
        # 生成有效的Python变量名
        var_name = FlowInterpreter._sanitize_variable_name(node_id, module_type, node_counter)
        
        # 根据module_type获取对应的State类名
        state_class_name = FlowInterpreter._get_state_class_name(module_type)
        if not state_class_name:
            raise ValueError(f"Unsupported module type: {module_type}")
        
        # 提取用户自定义的参数
        custom_inputs = FlowInterpreter._extract_custom_inputs(node["data"])
        
        # 生成添加节点的代码，实例化State类并传入参数
        code_lines = []
        code_lines.append(f"    # {node['data'].get('name', module_type)}节点")
        code_lines.append("    graph.add_node(")
        
        # 处理START节点的特殊情况
        if module_type == "questionInput" and node_id == "simpleInputId":
            code_lines.append("        id=START,")
        else:
            code_lines.append(f'        id="{var_name}",')
        
        # 如果有自定义参数，则生成带参数的实例化代码
        if custom_inputs:
            code_lines.append(f"        state={state_class_name}(")
            for key, value in custom_inputs.items():
                formatted_value = FlowInterpreter._format_value(value)
                code_lines.append(f"            {key}={formatted_value},")
            code_lines.append("        )")
        else:
            code_lines.append(f"        state={state_class_name}()")
        
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
        
        # 处理START节点的特殊情况
        source_formatted = "START" if source == "START" else f'"{source}"'
        target_formatted = "START" if target == "START" else f'"{target}"'
            
        return f'    graph.add_edge({source_formatted}, {target_formatted}, "{source_handle}", "{target_handle}")'
    
    def _generate_header_code(self) -> List[str]:
        """生成代码头部（导入和初始化部分）"""
        code_lines = []
        code_lines.append("from autoagents_graph.agentify import FlowGraph, START")
        code_lines.append("from autoagents_graph.agentify.models import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState")
        code_lines.append("")
        code_lines.append("def main():")
        code_lines.append("    graph = FlowGraph(")
        code_lines.append(f'        personal_auth_key="{self.auth_key}",')
        code_lines.append(f'        personal_auth_secret="{self.auth_secret}",')
        code_lines.append(f'        base_url="{self.base_url}"')
        code_lines.append("    )")
        code_lines.append("")
        return code_lines
    
    @staticmethod
    def _generate_footer_code() -> List[str]:
        """生成代码尾部（编译和main函数）"""
        code_lines = []
        code_lines.append("")
        code_lines.append("    # 编译")
        code_lines.append("    graph.compile(")
        code_lines.append('        name="知识库问答助手",')
        code_lines.append('        intro="基于知识库的智能问答系统",')
        code_lines.append('        category="问答助手",')
        code_lines.append('        prologue="您好！我是知识库问答助手，请提出您的问题。"')
        code_lines.append("    )")
        code_lines.append("")
        code_lines.append('if __name__ == "__main__":')
        code_lines.append("    main()")
        return code_lines
    
    def from_json_to_code(self, json_data: dict, output_path: str = None) -> str:
        """
        将JSON格式的流程图数据转换为SDK代码
        
        Args:
            json_data: 包含nodes和edges的JSON数据
            output_path: 可选的输出文件路径，如果提供则自动保存代码到文件
            
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
            
            # 处理START节点的特殊情况
            if module_type == "questionInput" and node_id == "simpleInputId":
                id_mapping[node_id] = "START"
            else:
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
        
        # 6. 生成最终代码字符串
        generated_code = "\n".join(code_lines)
        
        # 7. 如果提供了输出路径，保存到文件
        if output_path:
            import os
            # 确保输出目录存在
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # 保存代码到文件
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(generated_code)
            print(f"代码已保存到: {output_path}")
        
        return generated_code
    
    def generate_workflow_file(self, json_data: dict, output_path: str = "generated_workflow.py", overwrite: bool = False) -> bool:
        """
        生成工作流Python文件的便捷方法
        
        Args:
            json_data: 包含nodes和edges的JSON数据
            output_path: 输出文件路径，默认为"generated_workflow.py"
            overwrite: 是否覆盖已存在的文件，默认False
            
        Returns:
            成功返回True，失败返回False
        """
        import os
        
        # 检查文件是否已存在
        if os.path.exists(output_path) and not overwrite:
            print(f"文件 {output_path} 已存在，如需覆盖请设置 overwrite=True")
            return False
        
        try:
            # 生成并保存代码
            self.from_json_to_code(json_data, output_path)
            return True
        except Exception as e:
            print(f"生成工作流文件失败: {str(e)}")
            return False