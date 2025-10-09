from typing import List


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
        from .graph_processor import GraphProcessor
        
        source_node = GraphProcessor.find_node_by_id(nodes, source)
        target_node = GraphProcessor.find_node_by_id(nodes, target)
        
        if not source_node:
            raise ValueError(f"Source node '{source}' not found")
        
        if not target_node:
            raise ValueError(f"Target node '{target}' not found")

