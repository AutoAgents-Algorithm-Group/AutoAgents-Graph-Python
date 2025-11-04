from typing import Dict, List, Any, Optional, Union


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
            # 字典格式：可能是简单键值对，也可能是完整的字段定义
            converted = []
            for key, value in data.items():
                if isinstance(value, dict):
                    # 如果value是字典，说明是完整的字段定义，保留所有字段
                    field_def = {"key": key, **value}
                    converted.append(field_def)
                else:
                    # 如果value是简单值，转换为基本格式
                    converted.append({"key": key, "value": value})
            return converted
        
        # 其他类型不支持
        raise ValueError(f"Unsupported input format: {type(data)}. Expected dict or None.")

