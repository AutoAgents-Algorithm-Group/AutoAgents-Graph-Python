from copy import deepcopy
from typing import Optional, Union
from .data_converter import DataConverter
from .template_processor import TemplateProcessor
from .state_converter import StateConverter


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
        from ..services.node_registry import NODE_TEMPLATES
        template = deepcopy(NODE_TEMPLATES.get(module_type))
        
        # StateConverter已经处理了state→inputs/outputs的转换
        # 这里只需要将转换后的inputs/outputs与模板合并
        if isinstance(inputs, list):
            # 特殊格式（如addMemoryVariable）直接使用
            final_inputs = inputs
        else:
            # 标准格式，转换并合并
            converted_inputs = DataConverter.json_to_json_list(inputs)
            final_inputs = TemplateProcessor.merge_template_io(template.get("inputs", []), converted_inputs, module_type)
        
        if isinstance(outputs, list):
            # 特殊格式直接使用
            final_outputs = outputs
        else:
            # 标准格式，转换并合并
            converted_outputs = DataConverter.json_to_json_list(outputs)
            final_outputs = TemplateProcessor.merge_template_io(template.get("outputs", []), converted_outputs, module_type)
        
        # 需要导入AgentifyNode类
        from ..services.agentify_graph import AgentifyNode
        return NodeBuilder.create_node_instance(
            id=id,
            module_type=module_type,
            position=position, 
            inputs=final_inputs,
            outputs=final_outputs,
            template=template,
            flow_node_class=AgentifyNode
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

