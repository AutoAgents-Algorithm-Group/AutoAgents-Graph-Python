from copy import deepcopy
from typing import Dict, List, Any, Optional


class TemplateProcessor:
    """模板处理工具类"""
    
    @staticmethod
    def merge_template_io(template_io: List[Dict[str, Any]], custom_io: Optional[List[Dict[str, Any]]], module_type: str = None) -> List[Dict[str, Any]]:
        """
        合并模板IO配置和用户自定义IO配置
        
        Args:
            template_io: 模板中inputs或outputs列表，每个元素是一个字段的字典，字段完整
            custom_io: 用户传入的inputs或outputs列表，通常是部分字段，可能只有部分key覆盖
            module_type: 模块类型，用于特殊插入逻辑
            
        Returns:
            合并后的IO配置列表
        """
        if not custom_io:
            # 如果用户没有传自定义字段，直接返回模板的完整字段（深拷贝避免修改原数据）
            return deepcopy(template_io)

        merged = []
        template_keys = set()
        dynamic_items = []  # 存储动态参数
        
        # 先收集动态参数 - 通过type=parameter来识别
        if custom_io:
            for c_item in custom_io:
                # 识别动态参数（通过type=parameter且不在模板中）
                item_key = c_item.get("key", "")
                item_type = c_item.get("type", "")
                
                # 检查是否是动态参数：type为parameter且不在模板的默认keys中
                template_default_keys = {"switch", "switchAny", "_language_", "_description_", "_code_", 
                                       "_runSuccess_", "_runFailed_", "_runResult_", "finish"}
                
                if item_type == "parameter" and item_key not in template_default_keys:
                    dynamic_items.append(deepcopy(c_item))
        
        # 遍历模板里的所有字段
        for t_item in template_io:
            template_keys.add(t_item.get("key"))
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
                
            # 对于codeFragment的inputs，在switchAny之后插入动态输入参数
            if (module_type == "codeFragment" and 
                t_item.get("key") == "switchAny" and
                dynamic_items):
                # 插入动态参数到当前位置
                merged.extend(dynamic_items)

        # 对于非codeFragment，在末尾添加模板中没有的自定义字段（非动态参数）
        if module_type != "codeFragment":
            for c_item in custom_io:
                if (c_item.get("key") not in template_keys and 
                    not c_item.get("key", "").startswith("_dynamic_")):
                    merged.append(deepcopy(c_item))

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

