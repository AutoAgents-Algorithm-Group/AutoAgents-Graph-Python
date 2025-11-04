from typing import Optional
from ..models.graph_types import BaseNodeState


class NodeValidator:
    """节点验证工具类"""
    
    @staticmethod
    def validate_node_params(id: str, state):
        """验证节点参数"""
        # 检查state是否是BaseNodeState的实例或子类
        if not (isinstance(state, BaseNodeState) or 
                (isinstance(state, type) and issubclass(state, BaseNodeState))):
            raise ValueError("state parameter must be an instance of BaseNodeState or a BaseNodeState subclass")
        
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

