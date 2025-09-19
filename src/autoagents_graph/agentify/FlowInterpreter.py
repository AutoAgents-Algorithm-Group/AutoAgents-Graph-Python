from typing import Dict, Any, List
from .NodeRegistry import NODE_TEMPLATES


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
    def _generate_node_code(node: dict) -> str:
        """生成单个节点的代码"""
        node_id = node.get("id")
        module_type = node["data"].get("moduleType")
        position = node.get("position", {"x": 0, "y": 0})
        
        custom_inputs = FlowInterpreter._extract_custom_inputs(node["data"])
        
        if module_type == "addMemoryVariable":
            # 特殊处理addMemoryVariable
            code_lines = []
            code_lines.append(f"    memory_variable_inputs = []")
            
            for var in custom_inputs:
                var_name = var["key"]
                var_type = var["value_type"]
                code_lines.append(f"    {var_name} = {{")
                code_lines.append(f'        "key": "{var_name}",')
                code_lines.append(f'        "value_type": "{var_type}"')
                code_lines.append(f"    }}")
                code_lines.append(f"    memory_variable_inputs.append({var_name})")
            
            code_lines.append("")
            code_lines.append(f"    graph.add_node(")
            code_lines.append(f'        node_id="{node_id}",')
            code_lines.append(f'        module_type="{module_type}",')
            code_lines.append(f"        position={position},")
            code_lines.append(f"        inputs=memory_variable_inputs")
            code_lines.append(f"    )")
            
            return "\n".join(code_lines)
        else:
            # 普通节点处理
            code_lines = []
            code_lines.append(f"    graph.add_node(")
            code_lines.append(f'        node_id="{node_id}",')
            code_lines.append(f'        module_type="{module_type}",')
            code_lines.append(f"        position={position},")
            
            if custom_inputs:
                code_lines.append(f"        inputs={{")
                for key, value in custom_inputs.items():
                    formatted_value = FlowInterpreter._format_value(value)
                    code_lines.append(f'            "{key}": {formatted_value},')
                code_lines.append(f"        }}")
            
            code_lines.append(f"    )")
            
            return "\n".join(code_lines)
    
    @staticmethod
    def _generate_edge_code(edge: dict) -> str:
        """生成单个边的代码"""
        source = edge.get("source")
        target = edge.get("target")
        source_handle = edge.get("sourceHandle", "")
        target_handle = edge.get("targetHandle", "")
        
        return f'    graph.add_edge("{source}", "{target}", "{source_handle}", "{target_handle}")'
    
    def _generate_header_code(self) -> List[str]:
        """生成代码头部（导入和初始化部分）"""
        code_lines = []
        code_lines.append("from autoagentsai.graph import FlowGraph")
        code_lines.append("")
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
        
        # 1. 生成头部代码
        code_lines.extend(self._generate_header_code())
        
        # 2. 生成节点代码
        code_lines.append("    # 添加节点")
        nodes = json_data.get("nodes", [])
        for node in nodes:
            code_lines.append(FlowInterpreter._generate_node_code(node))
            code_lines.append("")
        
        # 3. 生成边代码
        code_lines.append("    # 添加连接边")
        edges = json_data.get("edges", [])
        for edge in edges:
            code_lines.append(FlowInterpreter._generate_edge_code(edge))
        
        # 4. 生成尾部代码
        code_lines.extend(self._generate_footer_code())
        
        return "\n".join(code_lines)