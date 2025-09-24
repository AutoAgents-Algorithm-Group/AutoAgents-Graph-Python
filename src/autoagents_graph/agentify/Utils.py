from copy import deepcopy
from typing import Dict, List, Any, Optional, Union
from .models.GraphTypes import (
    BaseNodeState, HttpInvokeState, QuestionInputState, AiChatState,
    ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,
    InfoClassState, CodeFragmentState, ForEachState
)


# ===== 数据转换工具类 =====

class DataConverter:
    """数据格式转换工具类"""
    
    @staticmethod
    def json_to_json_list(data: Optional[Union[Dict, List]]) -> Optional[List[Dict]]:
        """
        转换简化格式为展开的列表格式
        
        Args:
            data: 可以是 None 或 dict
                - None: 返回 None
                - dict: 简化格式 {"key1": "value1", "key2": "value2"} 
                  转换为 [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
                
        Returns:
            None 或 list 格式的数据
        """
        if data is None:
            return None
        
        if isinstance(data, dict):
            # 字典格式：直接包含键值对
            # {"key1": "value1", "key2": "value2"} 转换为 [{"key": "key1", "value": "value1"}, {"key": "key2", "value": "value2"}]
            converted = []
            for key, value in data.items():
                converted.append({"key": key, "value": value})
            return converted
        
        # 其他类型不支持
        raise ValueError(f"Unsupported input format: {type(data)}. Expected dict or None.")


class TemplateProcessor:
    """模板处理工具类"""
    
    @staticmethod
    def merge_template_io(template_io: List[Dict[str, Any]], custom_io: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        合并模板IO配置和用户自定义IO配置
        
        Args:
            template_io: 模板中inputs或outputs列表，每个元素是一个字段的字典，字段完整
            custom_io: 用户传入的inputs或outputs列表，通常是部分字段，可能只有部分key覆盖
            
        Returns:
            合并后的IO配置列表
        """
        if not custom_io:
            # 如果用户没有传自定义字段，直接返回模板的完整字段（深拷贝避免修改原数据）
            return deepcopy(template_io)

        merged = []
        # 遍历模板里的所有字段
        for t_item in template_io:
            # 在用户自定义列表中找有没有和当前模板字段 key 一样的字段
            c_item = next((c for c in custom_io if c.get("key") == t_item.get("key")), None)

            if c_item:
                # 找到了用户自定义字段
                merged_item = deepcopy(t_item)  # 先复制模板字段（保证完整结构）
                merged_item.update(c_item)  # 用用户的字段内容覆盖模板字段（例如value、description等被覆盖）
                merged.append(merged_item)
            else:
                # 用户没定义，直接用模板字段完整拷贝
                merged.append(deepcopy(t_item))

        return merged

    @staticmethod
    def process_add_memory_variable(template_input: Dict[str, Any], data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        将用户提供的字段转换为多个"记忆变量"，每个基于模板生成。

        Args:
            template_input: 模板字段结构（完整字段定义）
            data: 用户提供的字段列表，每项包含至少 key，可能包含 label/valueType

        Returns:
            List of memory variable dicts
        """
        if not data:
            return []

        return [
            {
                **deepcopy(template_input),
                "key": item["key"],
                "label": item["key"],
                "valueType": item.get("valueType", "string")
            }
            for item in data if "key" in item
        ]

class StateConverter:
    """状态转换器类"""
    
    @staticmethod
    def to_module_type(state: BaseNodeState) -> str:
        """
        根据State类型推断module_type
        
        Args:
            state: 节点状态对象
            
        Returns:
            module_type字符串
            
        Raises:
            ValueError: 如果无法识别state类型
        """
        type_mapping = {
            HttpInvokeState: "httpInvoke",
            QuestionInputState: "questionInput", 
            AiChatState: "aiChat",
            ConfirmReplyState: "confirmreply",
            KnowledgeSearchState: "knowledgesSearch",
            Pdf2MdState: "pdf2md",
            AddMemoryVariableState: "addMemoryVariable",
            InfoClassState: "infoClass",
            CodeFragmentState: "codeFragment",
            ForEachState: "forEach",
        }
        
        for state_class, module_type in type_mapping.items():
            if isinstance(state, state_class):
                return module_type
                
        raise ValueError(f"Unknown state type: {type(state)}")

    @staticmethod
    def to_inputs_outputs(state: BaseNodeState) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        从State对象转换为inputs和outputs配置
        
        Args:
            state: 节点状态对象
            
        Returns:
            tuple[inputs_dict, outputs_dict]: 输入和输出配置的元组
        """
        # 获取state的所有字段值
        state_dict = state.model_dump(exclude_none=True)
        
        # 提取基础字段（这些是inputs中的trigger相关字段）
        base_fields = {"switch", "switchAny", "finish"}
        inputs = {}
        outputs = {}
        
        # 根据不同的state类型进行特殊处理
        module_type = StateConverter.to_module_type(state)
        
        if module_type == "httpInvoke":
            # HTTP调用模块
            inputs.update({
                "url": state_dict.get("url", ""),
                "_requestBody_": state_dict.get("requestBody", "")
            })
            # outputs中的success/failed等由模板默认提供
            
        elif module_type == "questionInput":
            # 用户提问模块
            inputs.update({
                "inputText": state_dict.get("inputText", True),
                "uploadFile": state_dict.get("uploadFile", False),
                "uploadPicture": state_dict.get("uploadPicture", False),
                "fileUpload": state_dict.get("fileUpload", False),
                "fileContrast": state_dict.get("fileContrast", False),
                "fileInfo": state_dict.get("fileInfo", []),
                "initialInput": state_dict.get("initialInput", True)
            })
            
        elif module_type == "aiChat":
            # 智能对话模块 - 将isvisible映射为stream
            inputs.update({
                "text": state_dict.get("text", ""),
                "images": state_dict.get("images", []),
                "knSearch": state_dict.get("knSearch", ""),
                "knConfig": state_dict.get("knConfig", ""),
                "historyText": state_dict.get("historyText", 3),
                "model": state_dict.get("model", "doubao-deepseek-v3"),
                "quotePrompt": state_dict.get("quotePrompt", ""),
                "stream": state_dict.get("isvisible", True),  # 用户使用isvisible，内部映射为stream
                "temperature": state_dict.get("temperature", 0.1),
                "maxToken": state_dict.get("maxToken", 5000)
            })
            
        elif module_type == "confirmreply":
            # 确定回复模块 - 将isvisible映射为stream
            inputs.update({
                "stream": state_dict.get("isvisible", True),  # 用户使用isvisible，内部映射为stream
                "text": state_dict.get("text", "")
            })
            
        elif module_type == "knowledgesSearch":
            # 知识库搜索模块
            inputs.update({
                "text": state_dict.get("text", ""),
                "datasets": state_dict.get("datasets", []),
                "similarity": state_dict.get("similarity", 0.2),
                "vectorSimilarWeight": state_dict.get("vectorSimilarWeight", 1.0),
                "topK": state_dict.get("topK", 20),
                "enableRerank": state_dict.get("enableRerank", False),
                "rerankModelType": state_dict.get("rerankModelType", "oneapi-xinference:bce-rerank"),
                "rerankTopK": state_dict.get("rerankTopK", 10)
            })
            
        elif module_type == "pdf2md":
            # 通用文档解析模块
            inputs.update({
                "files": state_dict.get("files", []),
                "pdf2mdType": state_dict.get("pdf2mdType", "general")
            })
            
        elif module_type == "addMemoryVariable":
            # 添加记忆变量模块（特殊处理）
            variables = state_dict.get("variables", {})
            if variables:
                # 将variables字典转换为memory variable格式
                memory_inputs = []
                for key, value in variables.items():
                    memory_inputs.append({
                        "key": key,
                        "value_type": "string"  # 默认类型
                    })
                # 导入NODE_TEMPLATES来获取模板
                from .NodeRegistry import NODE_TEMPLATES
                template = NODE_TEMPLATES.get("addMemoryVariable")
                final_inputs = TemplateProcessor.process_add_memory_variable(template.get("inputs", [])[0], memory_inputs)
                return final_inputs, []  # 返回处理后的inputs
            else:
                inputs.update({
                    "feedback": state_dict.get("feedback", "")
                })
        
        elif module_type == "infoClass":
            # 信息分类模块（特殊处理labels）
            labels = state_dict.get("labels", {})
            processed_labels = StateConverter._convert_labels_dict_to_list(labels)
            
            inputs.update({
                "text": state_dict.get("text", ""),
                "knSearch": state_dict.get("knSearch", ""),
                "knConfig": state_dict.get("knConfig", ""),
                "historyText": state_dict.get("historyText", 3),
                "model": state_dict.get("model", "doubao-deepseek-v3"),
                "quotePrompt": state_dict.get("quotePrompt", ""),
                "labels": processed_labels
            })
            
            # 自动生成outputs
            output_keys = []
            if isinstance(labels, dict):
                output_keys = list(labels.keys())
            elif isinstance(labels, list):
                output_keys = [item.get("key") for item in labels if item.get("key")]
            
            for key in output_keys:
                outputs[key] = {
                    "valueType": "boolean",
                    "type": "source",
                    "key": key,
                    "targets": []
                }
            
        elif module_type == "codeFragment":
            # 代码块模块
            inputs.update({
                "_language_": state_dict.get("language", "js"),
                "_description_": state_dict.get("description", ""),
                "_code_": state_dict.get("code", "")
            })
            # 如果有动态inputs/outputs，也需要处理
            if state_dict.get("inputs"):
                inputs.update(state_dict["inputs"])
            if state_dict.get("outputs"):
                outputs.update(state_dict["outputs"])
                
        elif module_type == "forEach":
            # 循环模块
            inputs.update({
                "items": state_dict.get("items", []),
                "index": state_dict.get("index", 0),
                "item": state_dict.get("item"),
                "length": state_dict.get("length", 0),
                "loopEnd": state_dict.get("loopEnd", False)
            })
        
        return inputs, outputs

    @staticmethod
    def _convert_labels_dict_to_list(labels):
        """
        将labels字典格式转换为数组格式
        
        Args:
            labels: 字典格式的labels，如 {key1: "value1", key2: "value2"}
            
        Returns:
            数组格式的labels，如 [{"key": key1, "value": "value1"}, {"key": key2, "value": "value2"}]
        """
        if isinstance(labels, dict):
            return [{"key": key, "value": value} for key, value in labels.items()]
        elif isinstance(labels, list):
            # 如果已经是数组格式，直接返回
            return labels
        else:
            # 其他情况返回空数组
            return []

    @staticmethod
    def create_node_from_state(
        state: BaseNodeState,
        node_id: str,
        position: Dict[str, float]
    ) -> tuple[str, str, Dict[str, float], Dict[str, Any], Dict[str, Any]]:
        """
        从State对象创建节点所需的所有参数
        
        Args:
            state: 节点状态对象
            node_id: 节点ID
            position: 节点位置
            
        Returns:
            tuple[node_id, module_type, position, inputs, outputs]
        """
        module_type = StateConverter.to_module_type(state)
        inputs, outputs = StateConverter.to_inputs_outputs(state)
        
        return node_id, module_type, position, inputs, outputs


# ===== FlowGraph工具类 =====

class NodeValidator:
    """节点验证工具类"""
    
    @staticmethod
    def validate_node_params(id: str, state):
        """验证节点参数"""
        if not isinstance(state, BaseNodeState):
            raise ValueError("state parameter must be an instance of BaseNodeState")
        
        if not id or not isinstance(id, str):
            raise ValueError("node id must be a non-empty string")

    @staticmethod
    def validate_position(position: Optional[dict]) -> dict:
        """验证并解析节点位置"""
        if position is None:
            return None
        
        # 验证位置格式
        if not isinstance(position, dict) or "x" not in position or "y" not in position:
            raise ValueError("position must be a dict with 'x' and 'y' keys")
        
        return position


class EdgeValidator:
    """边验证工具类"""
    
    @staticmethod
    def validate_edge_params(source: str, target: str, source_handle: str, target_handle: str):
        """验证边参数"""
        if not source or not isinstance(source, str):
            raise ValueError("source must be a non-empty string")
        
        if not target or not isinstance(target, str):
            raise ValueError("target must be a non-empty string")
        
        if not isinstance(source_handle, str):
            raise ValueError("source_handle must be a string")
        
        if not isinstance(target_handle, str):
            raise ValueError("target_handle must be a string")

    @staticmethod
    def validate_nodes_exist(source: str, target: str, nodes: List):
        """检查节点是否存在"""
        source_node = GraphProcessor.find_node_by_id(nodes, source)
        target_node = GraphProcessor.find_node_by_id(nodes, target)
        
        if not source_node:
            raise ValueError(f"Source node '{source}' not found")
        
        if not target_node:
            raise ValueError(f"Target node '{target}' not found")


class NodeBuilder:
    """节点构建工具类"""
    
    @staticmethod
    def resolve_node_position(position: Optional[dict], existing_nodes_count: int) -> dict:
        """解析节点位置，如果未提供则自动布局"""
        if position is None:
            # 简单的自动布局：水平排列，每个节点间距500px
            return {"x": existing_nodes_count * 500, "y": 300}
        
        return position

    @staticmethod
    def extract_node_config(state, id: str, position: dict):
        """从state中提取节点配置"""
        _, module_type, _, inputs, outputs = StateConverter.create_node_from_state(state, id, position)
        return module_type, inputs, outputs

    @staticmethod
    def create_node(id: str, position: dict, module_type: str, inputs: Union[dict, list], outputs: dict):
        """创建节点"""
        from .NodeRegistry import NODE_TEMPLATES
        template = deepcopy(NODE_TEMPLATES.get(module_type))
        
        # StateConverter已经处理了state→inputs/outputs的转换
        # 这里只需要将转换后的inputs/outputs与模板合并
        if isinstance(inputs, list):
            # 特殊格式（如addMemoryVariable）直接使用
            final_inputs = inputs
        else:
            # 标准格式，转换并合并
            converted_inputs = DataConverter.json_to_json_list(inputs)
            final_inputs = TemplateProcessor.merge_template_io(template.get("inputs", []), converted_inputs)
        
        if isinstance(outputs, list):
            # 特殊格式直接使用
            final_outputs = outputs
        else:
            # 标准格式，转换并合并
            converted_outputs = DataConverter.json_to_json_list(outputs)
            final_outputs = TemplateProcessor.merge_template_io(template.get("outputs", []), converted_outputs)
        
        # 需要导入FlowNode类
        from .FlowGraph import FlowNode
        return NodeBuilder.create_node_instance(
            id=id,
            module_type=module_type,
            position=position, 
            inputs=final_inputs,
            outputs=final_outputs,
            template=template,
            flow_node_class=FlowNode
        )

    @staticmethod
    def create_node_instance(id: str, module_type: str, position: dict, 
                           inputs: list, outputs: list, template: dict, flow_node_class):
        """创建节点实例的通用方法"""
        node = flow_node_class(
            node_id=id,
            module_type=module_type,
            position=position,
            inputs=inputs,
            outputs=outputs
        )
        
        # 设置模板信息
        node.data["name"] = template.get("name")
        node.data["intro"] = template.get("intro")
        if template.get("category") is not None:
            node.data["category"] = template["category"]
        
        return node


class GraphProcessor:
    """图处理工具类"""
    
    @staticmethod
    def find_node_by_id(nodes: List, node_id: str) -> Optional:
        """根据ID查找节点"""
        for node in nodes:
            if node.id == node_id:
                return node
        return None

    @staticmethod
    def find_output_key_by_handle(node, source_handle):
        """
        根据source_handle查找对应的输出键
        
        Args:
            node: 节点对象
            source_handle: 源句柄
            
        Returns:
            匹配的输出键，如果没找到则返回None
        """
        for output in node.data.get("outputs", []):
            # 检查输出字段中是否有值等于source_handle的键
            for key, value in output.items():
                if value == source_handle:
                    return output.get("key")
        return None

    @staticmethod
    def check_and_fix_handle_type(source: str, target: str, source_handle: str, target_handle: str, nodes: List) -> tuple[str, str]:
        """
        检查 source_handle 与 target_handle 是否类型一致。
        若不一致，则清空 target_handle。
        """
        def get_field_type(node_id: str, field_key: str, field_category: str) -> Optional[str]:
            """
            从节点中查找字段类型
            
            Args:
                node_id: 节点ID
                field_key: 字段键名
                field_category: 字段类别 ('inputs' 或 'outputs')
            """
            for node in nodes:
                if node.id == node_id:
                    for field in node.data.get(field_category, []):
                        if field.get("key") == field_key:
                            return field.get("valueType")
                    break
            return None
        
        source_type = get_field_type(source, source_handle, "outputs")
        target_type = get_field_type(target, target_handle, "inputs")

        # 如果 source_type 或 target_type 为 "any"，则不需要检查类型一致性
        type_compatible = (source_type == "any" or target_type == "any") or (source_type == target_type)
        
        return (
            source_handle,
            target_handle if source_handle and target_handle and type_compatible else ""
        )

    @staticmethod
    def update_nodes_targets(nodes: List, edges: List):
        """
        高效更新节点的输出连接目标
        时间复杂度: O(edges + nodes + outputs) vs 原来的 O(edges * nodes * outputs)
        """
        # 1. 构建节点索引，避免线性搜索
        node_map = {node.id: node for node in nodes}
        
        # 2. 构建输出键到输出对象的映射，便于快速定位
        output_map = {}  # {node_id: {output_key: output_object}}
        for node in nodes:
            output_map[node.id] = {}
            for output in node.data.get("outputs", []):
                output_key = output.get("key")
                if output_key:
                    output_map[node.id][output_key] = output
        
        # 3. 构建连接映射：直接从边构建最终的连接关系
        connections = {}  # {node_id: {output_key: [target_info]}}
        
        for edge in edges:
            source_node = node_map.get(edge.source)
            if not source_node:
                continue
                
            # 查找匹配的输出键
            source_output_key = GraphProcessor.find_output_key_by_handle(source_node, edge.sourceHandle)
            if not source_output_key:
                continue
                
            # 构建目标信息
            target_info = {
                "target": edge.target,
                "targetHandle": edge.targetHandle
            }
            
            # 添加到连接映射中
            if edge.source not in connections:
                connections[edge.source] = {}
            if source_output_key not in connections[edge.source]:
                connections[edge.source][source_output_key] = []
            connections[edge.source][source_output_key].append(target_info)
        
        # 4. 去重并应用连接关系到节点
        for node_id, node_connections in connections.items():
            for output_key, targets in node_connections.items():
                # 去重：使用set去除重复的连接
                unique_targets = []
                seen = set()
                for target in targets:
                    target_tuple = (target["target"], target["targetHandle"])
                    if target_tuple not in seen:
                        seen.add(target_tuple)
                        unique_targets.append(target)
                
                # 应用到对应的输出对象
                if node_id in output_map and output_key in output_map[node_id]:
                    output_map[node_id][output_key]["targets"] = unique_targets