from typing import Dict, Any
from ..models.graph_types import (
    BaseNodeState, HttpInvokeState, QuestionInputState, AiChatState,
    ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,
    InfoClassState, CodeFragmentState, ForEachState, OfficeWordExportState,
    MarkdownToWordState, CodeExtractState, DatabaseQueryState
)


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
            OfficeWordExportState: "officeWordExport",
            MarkdownToWordState: "markdownToWord",
            CodeExtractState: "codeExtract",
            DatabaseQueryState: "databaseQuery",
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
                "pdf2mdType": state_dict.get("pdf2mdType", "deep_pdf2md")
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
                from ..services.node_registry import NODE_TEMPLATES
                from .template_processor import TemplateProcessor
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
            # 代码块模块 - 只处理基本配置参数，动态参数在TemplateProcessor中处理
            inputs.update({
                "_language_": state_dict.get("language", "js"),
                "_description_": state_dict.get("description", ""),
                "_code_": state_dict.get("code", "")
            })
            
            # 将动态inputs/outputs信息保留，让TemplateProcessor处理插入顺序
            if state_dict.get("inputs"):
                # 将动态inputs信息转换为列表格式，供TemplateProcessor使用
                dynamic_inputs = state_dict["inputs"]
                for param_name, param_info in dynamic_inputs.items():
                    # 创建连接点格式的参数，但不直接添加到inputs字典
                    # 而是通过特殊的key标记，让TemplateProcessor处理
                    inputs[f"_dynamic_input_{param_info['key']}"] = {
                        "key": param_info["key"],
                        "type": param_info.get("type", "target"),
                        "label": param_name,
                        "valueType": param_info.get("valueType", "string"),
                        "description": param_info.get("description", ""),
                        "connected": param_info.get("connected", True)
                    }
                    if "value" in param_info:
                        inputs[f"_dynamic_input_{param_info['key']}"]["value"] = param_info["value"]
            
            # 处理动态outputs
            if state_dict.get("outputs"):
                dynamic_outputs = state_dict["outputs"]
                for param_name, param_info in dynamic_outputs.items():
                    outputs[f"_dynamic_output_{param_info['key']}"] = {
                        "key": param_info["key"],
                        "type": param_info.get("type", "source"),
                        "label": param_name,
                        "valueType": param_info.get("valueType", "string"),
                        "description": param_info.get("description", ""),
                        "targets": param_info.get("targets", [])
                    }
                    if "value" in param_info:
                        outputs[f"_dynamic_output_{param_info['key']}"]["value"] = param_info["value"]
                
        elif module_type == "forEach":
            # 循环模块（index、item、length 会自动生成为字符串格式，如 "a545776c.index"）
            inputs.update({
                "items": state_dict.get("items", []),
                "index": state_dict.get("index", ""),  # 自动生成的变量名字符串
                "item": state_dict.get("item", ""),    # 自动生成的变量名字符串
                "length": state_dict.get("length", ""), # 自动生成的变量名字符串
                "loopEnd": state_dict.get("loopEnd", False)
            })
            
        elif module_type == "officeWordExport":
            # 文档输出模块
            inputs.update({
                "text": state_dict.get("text", ""),
                "templateFile": state_dict.get("templateFile")
            })
        elif module_type == "markdownToWord":
            # Markdown转Word模块
            inputs.update({
                "markdown": state_dict.get("markdown", ""),
                "word": state_dict.get("word", ""),
                "fileInfo": state_dict.get("fileInfo", "")
            })
        elif module_type in ["codeExtract"]:
            # 代码提取器模块
            inputs.update({
                "markdown": state_dict.get("markdown", ""),
                "codeType": state_dict.get("codeType", "SQL")
            })
        elif module_type == "DatabaseQuery":
            # 数据库查询模块
            inputs.update({
                "sql": state_dict.get("sql", ""),
                "database": state_dict.get("database", ""),
                "showTable": state_dict.get("showTable", True)
            })
            outputs.update({
                "queryResult": state_dict.get("queryResult", ""),
                "success": state_dict.get("success", False),
                "failed": state_dict.get("failed", False)
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
        state,  # 可以是BaseNodeState实例或类
        node_id: str,
        position: Dict[str, float]
    ) -> tuple[str, str, Dict[str, float], Dict[str, Any], Dict[str, Any]]:
        """
        从State对象或类创建节点所需的所有参数
        
        Args:
            state: 节点状态对象或状态类
            node_id: 节点ID
            position: 节点位置
            
        Returns:
            tuple[node_id, module_type, position, inputs, outputs]
        """
        # 如果state是类，创建一个默认实例
        if isinstance(state, type) and issubclass(state, BaseNodeState):
            state = state()
        
        module_type = StateConverter.to_module_type(state)
        inputs, outputs = StateConverter.to_inputs_outputs(state)
        
        return node_id, module_type, position, inputs, outputs

