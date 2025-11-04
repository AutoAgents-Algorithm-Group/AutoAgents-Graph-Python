from typing import List
from ..models.graph_types import NODE_STATE_FACTORY


class AgentifyParser:
    """
    流程图解析器，负责将JSON格式的流程图数据转换为SDK代码
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
            # 特殊处理addMemoryVariable - 提取记忆变量信息
            variables = {}
            for node_input in node_inputs:
                if node_input.get("type") == "agentMemoryVar":
                    key = node_input.get("key")
                    value_type = node_input.get("valueType", "string")
                    if key:
                        variables[key] = value_type
            
            if variables:
                custom_inputs["variables"] = variables
            return custom_inputs
        
        if module_type == "forEach":
            # 特殊处理forEach - 提取循环参数信息
            for node_input in node_inputs:
                if node_input.get("type") == "loopMemoryVar":
                    key = node_input.get("key")
                    value = node_input.get("value")
                    if key and value:
                        custom_inputs[key] = value
            return custom_inputs
        
        if module_type in ["codeFragment", "codeExtract"]:
            # 特殊处理codeFragment/codeExtract - 提取代码相关参数
            inputs_dict = {}
            outputs_dict = {}
            
            # 处理inputs
            for node_input in node_inputs:
                key = node_input.get("key")
                value = node_input.get("value")
                field_type = node_input.get("type", "")
                key_type = node_input.get("keyType", "")
                label = node_input.get("label", "")
                
                # 跳过trigger相关的系统字段
                if key_type in ["trigger", "triggerAny"]:
                    continue
                
                if key == "_code_" and value:
                    # 将_code_映射到code字段
                    custom_inputs["code"] = value
                elif key == "_language_" and value:
                    # 将_language_映射到language字段
                    custom_inputs["language"] = value
                elif key == "_description_" and value:
                    # 将_description_映射到description字段
                    custom_inputs["description"] = value
                elif field_type in ["parameter", "target"] and key not in ["switch", "switchAny"]:
                    # 提取自定义输入参数，使用label作为参数名
                    param_name = label if label else key
                    inputs_dict[param_name] = {
                        "key": key,
                        "type": field_type,
                        "valueType": node_input.get("valueType", "string"),
                        "description": node_input.get("description", ""),
                        "connected": node_input.get("connected", False)
                    }
                    if value is not None:
                        inputs_dict[param_name]["value"] = value
            
            # 处理outputs
            node_outputs = node_data.get("outputs", [])
            for node_output in node_outputs:
                key = node_output.get("key")
                field_type = node_output.get("type", "")
                label = node_output.get("label", "")
                
                # 只处理自定义的输出参数（parameter类型），跳过系统输出
                if field_type == "parameter" and key not in ["_runSuccess_", "_runFailed_", "_runResult_", "finish"]:
                    param_name = label if label else key
                    outputs_dict[param_name] = {
                        "key": key,
                        "type": field_type,
                        "valueType": node_output.get("valueType", "string"),
                        "description": node_output.get("description", ""),
                        "targets": node_output.get("targets", [])
                    }
                    if "value" in node_output:
                        outputs_dict[param_name]["value"] = node_output.get("value")
            
            # 如果有自定义参数，添加到custom_inputs中
            if inputs_dict:
                custom_inputs["inputs"] = inputs_dict
            if outputs_dict:
                custom_inputs["outputs"] = outputs_dict
                
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
                "initialInput", "isvisible", "pdf2mdType", "datasets", "similarity", 
                "vectorSimilarWeight", "topK", "expandChunks", "enablePermission",
                "enableRerank", "rerankModelType", "rerankTopK", "historyText",
                "model", "systemPrompt", "quotePrompt", "temperature", "topP", "maxToken",
                "text",  # 对于confirmreply的预设文本
                "items", "index", "item", "length", "loopEnd", "loopStart",  # forEach相关参数
                "_code_", "language", "description",  # codeFragment/codeExtract相关参数
                "templateFile"  
                "markdown", "word" , "fileInfo" 
                "code", "fileInfo" 
                "sql", "database", "showTable", "queryResult", "success", "failed" 
            }
            
            # 包含有意义的参数，且值不为默认值的情况
            if key in meaningful_keys and "value" in node_input:
                # 过滤掉一些明显的默认值
                if key == "initialInput" and value is True:
                    continue  # 跳过默认的initialInput=True
                if key in ["switch", "switchAny"] and value is False:
                    continue  # 跳过默认的trigger值
                if key == "isvisible" and value is True:
                    continue  # 跳过默认的isvisible=True
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
            "pdf2md": "doc_parser",
            "addMemoryVariable": "memory_var",
            "infoClass": "info_class",
            "codeFragment": "code_fragment",
            "forEach": "for_each",
            "httpInvoke": "http_invoke",
            "officeWordExport": "word_export",
            "markdownToWord": "markdown_to_word",
            "codeExtract": "code_extract",
            "databaseQuery": "database_query",
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
    def _generate_node_code(node: dict, node_counter: dict, labels_vars: dict = None) -> str:
        """生成单个节点的代码"""
        node_id = node.get("id")
        module_type = node["data"].get("moduleType")
        
        # 生成有效的Python变量名
        var_name = AgentifyParser._sanitize_variable_name(node_id, module_type, node_counter)
        
        # 根据module_type获取对应的State类名
        state_class_name = AgentifyParser._get_state_class_name(module_type)
        if not state_class_name:
            raise ValueError(f"Unsupported module type: {module_type}")
        
        # 提取用户自定义的参数
        
        custom_inputs = AgentifyParser._extract_custom_inputs(node["data"])
        
        # 提取position信息
        position = node.get("position")
        
        # 生成添加节点的代码，实例化State类并传入参数
        code_lines = []
        code_lines.append(f"    # {node['data'].get('name', module_type)}节点")
        
        # 对于InfoClassState，需要特殊处理labels
        if module_type == "infoClass" and labels_vars is not None:
            labels_dict = AgentifyParser._extract_labels_from_node(node)
            if labels_dict:
                labels_var_name = f"{var_name}_labels"
                labels_vars[node_id] = labels_var_name
                code_lines.append(f"    {labels_var_name} = {AgentifyParser._format_value(labels_dict)}")
                # 更新custom_inputs中的labels为变量引用
                custom_inputs["labels"] = f"__{labels_var_name}__"  # 特殊标记，稍后替换
        
        code_lines.append("    workflow.add_node(")
        
        # 处理START节点的特殊情况
        if module_type == "questionInput" and node_id == "simpleInputId":
            code_lines.append("        id=START,")
        else:
            code_lines.append(f'        id="{var_name}",')
        
        # 添加position参数
        if position:
            code_lines.append(f"        position={AgentifyParser._format_value(position)},")
        
        # 如果有自定义参数，则生成带参数的实例化代码
        if custom_inputs:
            code_lines.append(f"        state={state_class_name}(")
            for key, value in custom_inputs.items():
                if isinstance(value, str) and value.startswith("__") and value.endswith("__"):
                    # 处理变量引用
                    var_ref = value[2:-2]  # 去掉前后的__
                    code_lines.append(f"            {key}={var_ref},")
                else:
                    formatted_value = AgentifyParser._format_value(value)
                    code_lines.append(f"            {key}={formatted_value},")
            code_lines.append("        )")
        else:
            code_lines.append(f"        state={state_class_name}()")
        
        code_lines.append("    )")
        
        return "\n".join(code_lines)
    
    @staticmethod
    def _extract_labels_from_node(node: dict) -> dict:
        """从InfoClassState节点中提取labels字典"""
        inputs = node["data"].get("inputs", [])
        for input_item in inputs:
            if input_item.get("key") == "labels":
                labels_value = input_item.get("value", [])
                # 将列表格式转换为字典格式
                labels_dict = {}
                for label_item in labels_value:
                    key = label_item.get("key")
                    value = label_item.get("value")
                    if key and value:
                        labels_dict[key] = value
                return labels_dict
        return {}
    
    @staticmethod
    def _get_state_class_name(module_type: str) -> str:
        """根据module_type获取对应的State类名称字符串"""
        state_class = NODE_STATE_FACTORY.get(module_type)
        if state_class:
            return state_class.__name__
        return None
    
    @staticmethod
    def _generate_edge_code(edge: dict, id_mapping: dict = None, nodes: list = None, labels_vars: dict = None) -> str:
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
        
        # 处理InfoClassState的特殊情况：如果sourceHandle是UUID格式（InfoClassState的labels键）
        if nodes and source_handle and AgentifyParser._is_uuid_format(source_handle) and labels_vars:
            # 查找源节点
            source_node = AgentifyParser._find_node_by_id(nodes, edge.get("source"))
            if source_node and source_node["data"].get("moduleType") == "infoClass":
                # 获取对应的labels变量名
                labels_var_name = labels_vars.get(edge.get("source"))
                if labels_var_name:
                    # 获取UUID键在labels中的索引
                    labels_dict = AgentifyParser._extract_labels_from_node(source_node)
                    uuid_keys = list(labels_dict.keys())
                    if source_handle in uuid_keys:
                        index = uuid_keys.index(source_handle)
                        return f'    workflow.add_edge({source_formatted}, {target_formatted}, list({labels_var_name}.keys())[{index}], "{target_handle}")'
            
        return f'    workflow.add_edge({source_formatted}, {target_formatted}, "{source_handle}", "{target_handle}")'
    
    @staticmethod
    def _is_uuid_format(text: str) -> bool:
        """检查字符串是否是UUID格式"""
        import re
        # UUID格式：8-4-4-4-12个十六进制字符
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, text, re.IGNORECASE))
    
    @staticmethod
    def _find_node_by_id(nodes: list, node_id: str) -> dict:
        """根据ID查找节点"""
        for node in nodes:
            if node.get("id") == node_id:
                return node
        return None
    
    
    def _generate_header_code(self, has_infoclass: bool = False) -> List[str]:
        """生成代码头部（导入和初始化部分）"""
        code_lines = []
        code_lines.append("from autoagents_graph import NL2Workflow")
        code_lines.append("from autoagents_graph.engine.agentify import START")
        code_lines.append("from autoagents_graph.engine.agentify.models import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,CodeFragmentState,InfoClassState,ForEachState,OfficeWordExportState,MarkdownToWordState,CodeExtractState,DatabaseQueryState")
        if has_infoclass:
            code_lines.append("import uuid")
        code_lines.append("")
        code_lines.append("def main():")
        code_lines.append("    workflow = NL2Workflow(")
        code_lines.append('        platform="agentify",')
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
        code_lines.append("    workflow.compile(")
        code_lines.append('        name="从json导出的工作流",')
        code_lines.append('        intro="",')
        code_lines.append('        category="自动生成",')
        code_lines.append('        prologue="您好！我是从json导出的工作流"')
        code_lines.append("    )")
        code_lines.append("")
        code_lines.append('if __name__ == "__main__":')
        code_lines.append("    main()")
        return code_lines
    
    @staticmethod
    def _preprocess_json_data(json_data: dict) -> dict:
        """
        预处理JSON数据，将stream字段重命名为isvisible
        
        Args:
            json_data: 原始JSON数据
            
        Returns:
            处理后的JSON数据
        """
        import copy
        # 深拷贝以避免修改原始数据
        processed_data = copy.deepcopy(json_data)
        
        # 遍历所有节点
        for node in processed_data.get("nodes", []):
            # 遍历节点的inputs
            for node_input in node.get("data", {}).get("inputs", []):
                # 如果key是stream，将其改为isvisible
                if node_input.get("key") == "stream":
                    node_input["key"] = "isvisible"
        
        return processed_data
    
    def from_json_to_code(self, json_data: dict, output_path: str = None) -> str:
        """
        将JSON格式的流程图数据转换为SDK代码
        
        Args:
            json_data: 包含nodes和edges的JSON数据
            output_path: 可选的输出文件路径，如果提供则自动保存代码到文件
            
        Returns:
            生成的Python SDK代码字符串
        """
        # 预处理JSON数据：将stream字段重命名为isvisible
        json_data = self._preprocess_json_data(json_data)
        
        code_lines = []
        node_counter = {}  # 用于跟踪节点类型计数
        id_mapping = {}    # 原始ID到新ID的映射
        labels_vars = {}   # InfoClassState节点的labels变量映射
        
        # 1. 获取节点数据
        nodes = json_data.get("nodes", [])
        
        # 2. 检查是否有InfoClassState节点
        has_infoclass = any(node["data"].get("moduleType") == "infoClass" for node in nodes)
        
        # 3. 生成头部代码
        code_lines.extend(self._generate_header_code(has_infoclass))
        
        # 4. 先建立ID映射
        for node in nodes:
            node_id = node.get("id")
            module_type = node["data"].get("moduleType")
            
            # 处理START节点的特殊情况
            if module_type == "questionInput" and node_id == "simpleInputId":
                id_mapping[node_id] = "START"
            else:
                var_name = AgentifyParser._sanitize_variable_name(node_id, module_type, node_counter)
                id_mapping[node_id] = var_name
        
        # 重置计数器用于生成代码
        node_counter.clear()
        
        # 5. 生成节点代码
        code_lines.append("    # 添加节点")
        for node in nodes:
            code_lines.append(AgentifyParser._generate_node_code(node, node_counter, labels_vars))
            code_lines.append("")
        
        # 6. 生成边代码
        code_lines.append("    # 添加连接边")
        edges = json_data.get("edges", [])
        for edge in edges:
            code_lines.append(AgentifyParser._generate_edge_code(edge, id_mapping, nodes, labels_vars))
        
        # 7. 生成尾部代码
        code_lines.extend(self._generate_footer_code())
        
        # 8. 生成最终代码字符串
        generated_code = "\n".join(code_lines)
        
        # 9. 如果提供了输出路径，保存到文件
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

