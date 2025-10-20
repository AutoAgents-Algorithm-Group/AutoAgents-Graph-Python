from typing import List, Dict, Any
import yaml
import json
from .dify_node_registry import DifyNodeRegistry


class DifyParser:
    """
    Dify工作流解析器，负责将Dify导出的YAML格式转换为SDK代码
    """
    
    def __init__(self):
        """初始化DifyParser"""
        pass
    
    @staticmethod
    def _extract_node_params(node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从节点数据中提取参数（使用注册表）
        
        Args:
            node_data: 节点的data字段
            
        Returns:
            提取的参数字典
        """
        node_type = node_data.get("type", "")
        
        try:
            # 使用注册表提取参数
            return DifyNodeRegistry.extract_node_params(node_data, node_type)
        except KeyError:
            # 如果节点类型不在注册表中，回退到原始逻辑
            return DifyParser._extract_node_params_legacy(node_data)
    
    @staticmethod
    def _extract_node_params_legacy(node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        从节点数据中提取参数（原始逻辑，用作回退）
        
        Args:
            node_data: 节点的data字段
            
        Returns:
            提取的参数字典
        """
        params = {}
        node_type = node_data.get("type", "")
        
        # 根据不同节点类型提取参数
        if node_type == "start":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "variables" in node_data:
                params["variables"] = node_data["variables"]
                
        elif node_type == "llm":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "model" in node_data:
                params["model"] = node_data["model"]
            if "prompt_template" in node_data:
                params["prompt_template"] = node_data["prompt_template"]
            if "context" in node_data:
                params["context"] = node_data["context"]
            if "variables" in node_data:
                params["variables"] = node_data["variables"]
            # 迭代相关字段（用于iteration内的节点）
            if "isInIteration" in node_data:
                params["isInIteration"] = node_data["isInIteration"]
            if "iteration_id" in node_data:
                params["iteration_id"] = node_data["iteration_id"]
            if "isInLoop" in node_data:
                params["isInLoop"] = node_data["isInLoop"]
                
        elif node_type == "knowledge-retrieval":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "dataset_ids" in node_data:
                params["dataset_ids"] = node_data["dataset_ids"]
            if "query_variable_selector" in node_data:
                params["query_variable_selector"] = node_data["query_variable_selector"]
            if "multiple_retrieval_config" in node_data:
                params["multiple_retrieval_config"] = node_data["multiple_retrieval_config"]

        elif node_type == "end":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "outputs" in node_data:
                params["outputs"] = node_data["outputs"]
                
        elif node_type == "answer":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "variables" in node_data:
                params["variables"] = node_data["variables"]
                
        elif node_type == "code":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "code" in node_data:
                params["code"] = node_data["code"]
            if "code_language" in node_data:
                params["code_language"] = node_data["code_language"]
            if "outputs" in node_data:
                params["outputs"] = node_data["outputs"]
            if "variables" in node_data:
                params["variables"] = node_data["variables"]
                
        elif node_type == "tool":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "provider_id" in node_data:
                params["provider_id"] = node_data["provider_id"]
            if "provider_name" in node_data:
                params["provider_name"] = node_data["provider_name"]
            if "provider_type" in node_data:
                params["provider_type"] = node_data["provider_type"]
            if "tool_configurations" in node_data:
                params["tool_configurations"] = node_data["tool_configurations"]
            if "tool_description" in node_data:
                params["tool_description"] = node_data["tool_description"]
            if "tool_label" in node_data:
                params["tool_label"] = node_data["tool_label"]
            if "tool_name" in node_data:
                params["tool_name"] = node_data["tool_name"]
            if "tool_parameters" in node_data:
                params["tool_parameters"] = node_data["tool_parameters"]
                
        elif node_type == "if-else":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "cases" in node_data:
                params["cases"] = node_data["cases"]
            if "logical_operator" in node_data:
                params["logical_operator"] = node_data["logical_operator"]
                
        elif node_type == "iteration":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "error_handle_mode" in node_data:
                params["error_handle_mode"] = node_data["error_handle_mode"]
            if "input_parameters" in node_data:
                params["input_parameters"] = node_data["input_parameters"]
            if "is_array_input" in node_data:
                params["is_array_input"] = node_data["is_array_input"]
            if "is_parallel" in node_data:
                params["is_parallel"] = node_data["is_parallel"]
            if "iterator_selector" in node_data:
                params["iterator_selector"] = node_data["iterator_selector"]
            if "output_selector" in node_data:
                params["output_selector"] = node_data["output_selector"]
            if "output_type" in node_data:
                params["output_type"] = node_data["output_type"]
            if "parallel_nums" in node_data:
                params["parallel_nums"] = node_data["parallel_nums"]
            if "start_node_id" in node_data:
                params["start_node_id"] = node_data["start_node_id"]
            # iteration 节点的尺寸信息（容器节点需要）
            if "width" in node_data:
                params["width"] = node_data["width"]
            if "height" in node_data:
                params["height"] = node_data["height"]
                
        elif node_type == "iteration-start":
            if "title" in node_data:
                params["title"] = node_data["title"]
            if "isInIteration" in node_data:
                params["isInIteration"] = node_data["isInIteration"]
            # 注意：parentId 是节点层级属性，不在 data 中
            # iteration_id 对 iteration-start 也不需要
        
        return params
    
    @staticmethod
    def _get_state_class_name(node_type: str) -> str:
        """根据节点类型获取State类名（使用注册表）"""
        try:
            return DifyNodeRegistry.get_state_class_name(node_type)
        except KeyError:
            # 如果节点类型不在注册表中，回退到原始映射
            return DifyParser._get_state_class_name_legacy(node_type)
    
    @staticmethod
    def _get_state_class_name_legacy(node_type: str) -> str:
        """根据节点类型获取State类名（原始逻辑）"""
        type_mapping = {
            "start": "DifyStartState",
            "llm": "DifyLLMState",
            "knowledge-retrieval": "DifyKnowledgeRetrievalState",
            "end": "DifyEndState",
            "answer": "DifyAnswerState",
            "code": "DifyCodeState",
            "tool": "DifyToolState",
            "if-else": "DifyIfElseState",
            "iteration": "DifyIterationState",
            "iteration-start": "DifyIterationStartState",
        }
        return type_mapping.get(node_type, None)
    
    @staticmethod
    def _format_value(value: Any) -> str:
        """格式化Python值"""
        if isinstance(value, str):
            if '\n' in value:
                escaped_value = value.replace('\\', '\\\\').replace('"""', '\\"""')
                return f'"""{escaped_value}"""'
            else:
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
    def _sanitize_node_id(node_id: str, node_type: str) -> str:
        """将节点ID转换为有效的Python变量名"""
        # START和END节点特殊处理
        if node_type == "start":
            return "START"
        if node_type == "end":
            return "END"
        
        # 移除特殊字符，保留下划线和字母数字
        sanitized = ''.join(c if c.isalnum() or c == '_' else '_' for c in node_id)
        
        # 如果以数字开头，添加前缀
        if sanitized and sanitized[0].isdigit():
            sanitized = f"node_{sanitized}"
        
        return sanitized or "node"
    
    @staticmethod
    def _generate_node_code(node: Dict[str, Any], id_mapping: Dict[str, str]) -> str:
        """生成单个节点的代码"""
        node_id = node.get("id")
        node_data = node.get("data", {})
        position = node.get("position", {"x": 0, "y": 0})
        parent_id = node.get("parentId")  # 获取节点层级的 parentId
        node_type = node_data.get("type", "")
        
        # 对于特殊节点类型，使用常量；否则直接使用原始ID
        if node_type == "start":
            id_for_code = "START"
        elif node_type == "end":
            id_for_code = "END"
        else:
            # 直接使用原始节点ID，不进行sanitize
            id_for_code = f'"{node_id}"'
        
        # 获取State类名
        state_class = DifyParser._get_state_class_name(node_type)
        if not state_class:
            return f"    # 未知节点类型: {node_type}"
        
        # 提取参数
        params = DifyParser._extract_node_params(node_data)
        
        # 生成代码
        code_lines = []
        code_lines.append(f"    # 添加{node_data.get('title', node_type)}节点")
        code_lines.append("    workflow.add_node(")
        
        # ID参数 - 直接使用原始ID
        code_lines.append(f"        id={id_for_code},")
        
        # position参数
        code_lines.append(f"        position={DifyParser._format_value(position)},")
        
        # state参数
        has_parent = bool(parent_id)
        if params:
            code_lines.append(f"        state={state_class}(")
            for key, value in params.items():
                formatted_value = DifyParser._format_value(value)
                code_lines.append(f"            {key}={formatted_value},")
            code_lines.append("        )" + ("," if has_parent else ""))
        else:
            code_lines.append(f"        state={state_class}()" + ("," if has_parent else ""))
        
        # 如果有 parentId，添加 parent_id 参数
        if parent_id:
            code_lines.append(f"        parent_id=\"{parent_id}\"")
        
        code_lines.append("    )")
        
        return "\n".join(code_lines)
    
    @staticmethod
    def _generate_edge_code(edge: Dict[str, Any], id_mapping: Dict[str, Any]) -> str:
        """生成单个边的代码"""
        source = edge.get("source")
        target = edge.get("target")
        source_handle = edge.get("sourceHandle", "source")
        target_handle = edge.get("targetHandle", "target")
        
        # 确定节点类型以判断是否使用常量
        # 通过id_mapping查找节点类型（如果有的话）
        source_type = id_mapping.get(source, {}).get("type") if isinstance(id_mapping.get(source), dict) else None
        target_type = id_mapping.get(target, {}).get("type") if isinstance(id_mapping.get(target), dict) else None
        
        # 格式化源节点ID
        if source == "start" or source_type == "start":
            source_formatted = "START"
        elif source == "end" or source_type == "end":
            source_formatted = "END"
        else:
            source_formatted = f'"{source}"'
        
        # 格式化目标节点ID
        if target == "start" or target_type == "start":
            target_formatted = "START"
        elif target == "end" or target_type == "end":
            target_formatted = "END"
        elif target == "answer":
            target_formatted = '"answer"'
        else:
            target_formatted = f'"{target}"'
        
        # 如果是if-else的边，需要传递source_handle
        if source_handle in ["true", "false"]:
            return f'    workflow.add_edge({source_formatted}, {target_formatted}, source_handle="{source_handle}")'
        else:
            return f'    workflow.add_edge({source_formatted}, {target_formatted})'
    
    @staticmethod
    def _generate_header_code() -> List[str]:
        """生成代码头部"""
        return [
            "import os",
            "import sys",
            "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))",
            "",
            "from src.autoagents_graph import NL2Workflow, DifyConfig",
            "from src.autoagents_graph.engine.dify import (",
            "    DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState,",
            "    DifyEndState, DifyAnswerState, DifyCodeState, DifyToolState,",
            "    DifyIfElseState, DifyIterationState, DifyIterationStartState,",
            "    START, END",
            ")",
            "",
            "",
            "def main():",
            "    # 创建Dify工作流",
            "    workflow = NL2Workflow(",
            '        platform="dify",',
            "        config=DifyConfig(",
            '            app_name="从Dify导出的工作流",',
            '            app_description="通过DifyParser自动生成",',
            '            app_icon="🤖",',
            '            app_icon_background="#FFEAD5"',
            "        )",
            "    )",
            "",
        ]
    
    @staticmethod
    def _generate_footer_code() -> List[str]:
        """生成代码尾部"""
        return [
            "",
            "    # 编译并保存",
            "    yaml_result = workflow.compile()",
            '    workflow.save("playground/dify/outputs/dify_workflow_output.yaml")',
            "    print(f\"工作流已生成，YAML长度: {len(yaml_result)} 字符\")",
            "",
            "",
            'if __name__ == "__main__":',
            "    main()",
        ]
    
    def from_yaml_file(self, yaml_file_path: str, output_path: str = None) -> str:
        """
        从YAML文件转换为SDK代码
        
        Args:
            yaml_file_path: YAML文件路径
            output_path: 可选的输出文件路径
            
        Returns:
            生成的Python SDK代码字符串
        """
        # 读取YAML文件
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        # 解析YAML
        data = yaml.safe_load(yaml_content)
        
        # 获取工作流数据
        workflow_data = data.get("workflow", {})
        graph_data = workflow_data.get("graph", {})
        nodes = graph_data.get("nodes", [])
        edges = graph_data.get("edges", [])
        
        # 建立ID映射（包含节点类型信息，供边生成时使用）
        id_mapping = {}
        for node in nodes:
            node_id = node.get("id")
            node_type = node.get("data", {}).get("type", "")
            # 保存节点类型信息，用于边生成时判断
            id_mapping[node_id] = {"type": node_type}
        
        # 生成代码
        code_lines = []
        
        # 1. 头部
        code_lines.extend(DifyParser._generate_header_code())
        
        # 2. 节点
        code_lines.append("    # 添加节点")
        for node in nodes:
            code_lines.append(DifyParser._generate_node_code(node, id_mapping))
            code_lines.append("")
        
        # 3. 边
        code_lines.append("    # 添加连接边")
        for edge in edges:
            code_lines.append(DifyParser._generate_edge_code(edge, id_mapping))
        
        # 4. 尾部
        code_lines.extend(DifyParser._generate_footer_code())
        
        # 生成最终代码
        generated_code = "\n".join(code_lines)
        
        # 保存到文件
        if output_path:
            import os
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(generated_code)
            print(f"代码已保存到: {output_path}")
        
        return generated_code

