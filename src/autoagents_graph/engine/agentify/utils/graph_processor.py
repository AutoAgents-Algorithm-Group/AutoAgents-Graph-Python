from typing import List, Optional


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

