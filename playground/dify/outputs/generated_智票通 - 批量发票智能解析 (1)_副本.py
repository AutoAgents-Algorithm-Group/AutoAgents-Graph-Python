import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.autoagents_graph import NL2Workflow, DifyConfig
from src.autoagents_graph.engine.dify import (
    DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState,
    DifyEndState, DifyAnswerState, DifyCodeState, DifyToolState,
    DifyIfElseState, START, END
)


def main():
    # 创建Dify工作流
    workflow = NL2Workflow(
        platform="dify",
        config=DifyConfig(
            app_name="从Dify导出的工作流",
            app_description="通过DifyParser自动生成",
            app_icon="🤖",
            app_icon_background="#FFEAD5"
        )
    )

    # 添加节点
    # 添加开始节点
    workflow.add_node(
        id=START,
        position={'x': 750.5801422917975, 'y': 511.0876181312255},
        state=DifyStartState(
            title="开始",
            variables=[],
        )
    )

    # 添加直接回复节点
    workflow.add_node(
        id="answer",
        position={'x': 2675.0439874093213, 'y': 710.1191383271242},
        state=DifyAnswerState(
            title="直接回复",
            variables=[],
        )
    )

    # 添加LLM节点
    workflow.add_node(
        id="node_1749105824146",
        position={'x': 1832.52539414044, 'y': 650.4684952275279},
        state=DifyLLMState(
            title="LLM",
            model={'completion_params': {}, 'mode': 'chat', 'name': 'Qwen/Qwen2.5-VL-72B-Instruct', 'provider': 'langgenius/siliconflow/siliconflow'},
            prompt_template=[{'id': '5dc7034f-b1bb-4939-b644-f7eefa0c0c29', 'role': 'system', 'text': '# Role: 财务发票整理专家\n\n## Profile\n\n- 专业领域: 财务管理、发票处理\n- 专长: 电子发票信息提取、数据整理、JSON格式输出、特殊发票处理\n- 工作经验: 10年以上财务发票处理经验，包括各类特殊发票\n\n## Background\n\n你是一位经验丰富的财务发票整理专家，擅长处理各类电子发票，并能够准确提取关键信息。你的工作涉及大量发票数据的处理和整理，需要高度的准确性和一致性。你了解最新的发票格式变化，包括某些发票将发票代码和发票号码合并的情况，以及航空电子客运发票的特殊格式，以及新版火车票的税额计算方法。\n\n## Goals\n\n1. 准确提取电子发票中的关键信息\n2. 将提取的信息整理成统一的数据格式\n3. 以JSON格式输出处理后的发票数据\n4. 确保所有必要字段都被正确识别和填充\n5. 正确处理发票代码和发票号码合并的情况\n6. 适当处理航空电子客运发票的特殊格式\n7. 对于新版火车票，在无法直接提取税额时进行准确计算\n\n## Skills\n\n- 精通各类电子发票结构和内容，包括最新的格式变化和特殊发票类型\n- 熟练使用图像识别技术提取发票信息\n- 擅长数据整理和格式化\n- 熟悉JSON数据格式\n- 注重细节，保证数据的准确性和完整性\n- 能够灵活处理不同格式的发票信息，包括航空电子客运发票\n- 熟悉特殊发票的税额计算方法\n\n## Workflows\n\n1. 接收电子发票图像链接\n2. 使用图像识别工具提取发票信息\n3. 识别发票类型和格式\n4. 根据发票类型采取相应的信息提取策略：\n   - 普通发票：正常提取所有字段\n   - 合并格式发票：将完整号码放入"发票号码"字段\n   - 航空电子客运发票：将电子客票号码放入"发票号码"字段\n   - 新版火车票：尝试提取税额，如果无法提取则根据金额计算\n5. 整理提取的信息，确保包含所有必要字段\n6. 对于新版火车票，如果税额未提取到，进行税额计算\n7. 将整理后的信息转换为JSON格式\n8. 检查输出数据的完整性和准确性\n9. 返回最终的JSON格式数据\n\n## Rules\n\n1. 必须提取的字段包括: "发票代码"、"发票号码"、"开票日期"、"开票类目"、"金额"、"税额"、"发票类型"\n2. 所有提取的信息必须准确无误\n3. 输出必须使用JSON格式\n4. 如果某个字段在发票中不存在，应在JSON中将该字段值设为""\n5. 对于发票代码和发票号码合并的新格式发票：\n   - 将完整的合并号码填入"发票号码"字段\n   - "发票代码"字段应设置为""\n6. 对于航空电子客运发票：\n   - 将电子客票号码填入"发票号码"字段\n   - "发票代码"字段应设置为""\n7. 对于新版火车票：\n   - 如果无法直接提取税额，使用以下公式计算：\n     税额 = 票面金额 ÷ (1 + 9%) × 9%\n   - 计算结果保留两位小数\n8. "发票类型"字段应准确反映发票的类型，如"增值税电子普通发票"、"航空电子客运发票"、"铁路电子客票"等\n9. 保持数据格式的一致性，即使处理多张不同类型的发票\n\n## Output Format\n\n{\n  "发票代码": "string or  ",\n  "发票号码": "string",\n  "开票日期": "string",\n  "开票类目": "string",\n  "金额": "number",\n  "税额": "number",\n  "发票类型": "string"\n}\n\n## Initialization\n\n作为财务发票整理专家，我已准备好协助您处理各种类型的电子发票信息。我了解不同发票格式的特点，包括新格式发票将发票代码和发票号码合并的情况，以及航空电子客运发票只有电子客票号码的特殊情况。我会根据实际情况灵活处理这些信息，确保输出的JSON数据格式统一且准确。请提供需要处理的电子发票图像链接，我将为您提取关键信息并以JSON格式输出。如果您有任何特殊要求或额外的处理需求，请告诉我。让我们开始工作吧！'}, {'id': 'b071a2e9-7551-467d-8798-86220c5d8b2e', 'role': 'user', 'text': '{{#sys.files#}}'}],
            context={'enabled': False, 'variable_selector': []},
            variables=[],
        )
    )

    # 添加批处理发票记录节点
    workflow.add_node(
        id="node_1749115381294",
        position={'x': 2099.1885519854736, 'y': 777.5486392164499},
        state=DifyCodeState(
            title="批处理发票记录",
            code="""import json

def main(arg1: str) -> dict:
    # 按 ```json 分割，取后半部分
    part = arg1.split('```json', 1)[-1]
    # 再按 ``` 分割，取第一部分并去除首尾空白
    json_content = part.split('```', 1)[0].strip()
    
    try:
        # 解析JSON内容
        data = json.loads(json_content)
        # 转换为表格格式
        table = []
        for item in data:
            # 为每个发票创建记录，包含所有字段
            invoice_data = [
                item.get('发票代码', ''),
                item.get('发票号码', ''),
                item.get('开票日期', ''),
                item.get('开票类目', ''),
                str(item.get('金额', '')),
                str(item.get('税额', '')),
                item.get('发票类型', '')
            ]
            table.append(invoice_data)

        return {
            "result": str(table).replace("'", '"')
        }
    except json.JSONDecodeError:
        # 若JSON解析失败，返回原始内容
        return {
            "result": [["错误", "JSON解析失败"]]
        }""",
            code_language="python3",
            outputs={'result': {'children': None, 'type': 'string'}},
            variables=[{'value_selector': ['17542127425600', 'text'], 'value_type': 'string', 'variable': 'arg1'}],
        )
    )

    # 添加新增多行至工作表最后(1)节点
    workflow.add_node(
        id="node_1749116054395",
        position={'x': 2362.493804647156, 'y': 650.4684952275279},
        state=DifyToolState(
            title="新增多行至工作表最后(1)",
            provider_id="langgenius/feishu_spreadsheet/feishu_spreadsheet",
            provider_name="langgenius/feishu_spreadsheet/feishu_spreadsheet",
            provider_type="builtin",
            tool_configurations={'length': {'type': 'constant', 'value': 1}},
            tool_description="新增多行至工作表最后",
            tool_label="新增多行至工作表最后",
            tool_name="add_rows",
            tool_parameters={'sheet_id': {'type': 'mixed', 'value': ''}, 'sheet_name': {'type': 'mixed', 'value': ''}, 'spreadsheet_token': {'type': 'mixed', 'value': '{{#env.fenshuurl#}}'}, 'values': {'type': 'mixed', 'value': '{{#17514479903070.result#}}'}},
        )
    )

    # 添加条件分支节点
    workflow.add_node(
        id="node_1751447829988",
        position={'x': 1563.6310341559754, 'y': 650.4684952275279},
        state=DifyIfElseState(
            title="条件分支",
        )
    )

    # 添加单张发票记录节点
    workflow.add_node(
        id="node_17514479903070",
        position={'x': 2099.1885519854736, 'y': 650.4684952275279},
        state=DifyCodeState(
            title="单张发票记录",
            code="""import json

def main(arg1: str) -> dict:
    try:
        # 按 ```json 分割，取后半部分
        part = arg1.split('```json', 1)[-1]
        # 再按 ``` 分割，取第一部分并去除首尾空白
        json_content = part.split('```', 1)[0].strip()
        
        # 尝试解析 JSON 内容
        data = json.loads(json_content)
        
        # 检查 data 是否为字典
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object, but got: {}".format(type(data)))
        
        # 直接访问字典的字段，不需要遍历
        invoice_data = [
            data.get('发票代码', ''),
            data.get('发票号码', ''),
            data.get('开票日期', ''),
            data.get('开票类目', ''),
            str(data.get('金额', '')),
            str(data.get('税额', '')),
            data.get('发票类型', '')
        ]
        table = [invoice_data]  # 注意：这里用 [] 包裹，因为只有一条记录
        
        return {
            "result": str(table).replace("'", '"')
        }
    
    except json.JSONDecodeError as e:
        # 若 JSON 解析失败，返回原始内容
        return {
            "result": [["错误", "JSON 解析失败", str(e)]]
        }
    
    except ValueError as e:
        # 若数据结构不匹配，返回错误信息
        return {
            "result": [["错误", "数据格式错误", str(e)]]
        }
    
    except Exception as e:
        # 捕获其他异常
        return {
            "result": [["错误", "未知错误", str(e)]]
        }""",
            code_language="python3",
            outputs={'result': {'children': None, 'type': 'string'}},
            variables=[{'value_selector': ['1749105824146', 'text'], 'variable': 'arg1'}],
        )
    )

    # 添加新增多行至工作表最后 (2)节点
    workflow.add_node(
        id="node_17514490270830",
        position={'x': 2362.493804647156, 'y': 777.5486392164499},
        state=DifyToolState(
            title="新增多行至工作表最后 (2)",
            provider_id="langgenius/feishu_spreadsheet/feishu_spreadsheet",
            provider_name="langgenius/feishu_spreadsheet/feishu_spreadsheet",
            provider_type="builtin",
            tool_configurations={'length': {'type': 'constant', 'value': 1}},
            tool_description="新增多行至工作表最后",
            tool_label="新增多行至工作表最后",
            tool_name="add_rows",
            tool_parameters={'sheet_id': {'type': 'mixed', 'value': ''}, 'spreadsheet_token': {'type': 'mixed', 'value': '{{#env.fenshuurl#}}'}, 'values': {'type': 'mixed', 'value': '{{#1749115381294.result#}}'}},
        )
    )

    # 添加判断上传文件数量节点
    workflow.add_node(
        id="node_1754212275955",
        position={'x': 1286.8619528051909, 'y': 650.4684952275279},
        state=DifyCodeState(
            title="判断上传文件数量",
            code="""import json

def main(uploaded_files: list) -> dict:
    # 计算上传文件的数量
    file_count = len(uploaded_files)
    
    # 将 file_count 转换为字符串
    file_count_str = str(file_count)
    
    return {
        "file_count": file_count_str
    }""",
            code_language="python3",
            outputs={'file_count': {'children': None, 'type': 'string'}},
            variables=[{'value_selector': ['sys', 'files'], 'value_type': 'array[file]', 'variable': 'uploaded_files'}],
        )
    )

    # 添加LLM (1)节点
    workflow.add_node(
        id="node_17542127425600",
        position={'x': 1832.52539414044, 'y': 777.5486392164499},
        state=DifyLLMState(
            title="LLM (1)",
            model={'completion_params': {}, 'mode': 'chat', 'name': 'Qwen/Qwen2.5-VL-72B-Instruct', 'provider': 'langgenius/siliconflow/siliconflow'},
            prompt_template=[{'id': '5dc7034f-b1bb-4939-b644-f7eefa0c0c29', 'role': 'system', 'text': '# Role: 财务发票整理专家\n\n## Profile\n\n- 专业领域: 财务管理、发票处理\n- 专长: 电子发票信息提取、数据整理、JSON格式输出、特殊发票处理\n- 工作经验: 10年以上财务发票处理经验，包括各类特殊发票\n\n## Background\n\n你是一位经验丰富的财务发票整理专家，擅长处理各类电子发票，并能够准确提取关键信息。你的工作涉及大量发票数据的处理和整理，需要高度的准确性和一致性。你了解最新的发票格式变化，包括某些发票将发票代码和发票号码合并的情况，以及航空电子客运发票的特殊格式，以及新版火车票的税额计算方法。\n\n## Goals\n\n1. 准确提取电子发票中的关键信息\n2. 将提取的信息整理成统一的数据格式\n3. 以JSON格式输出处理后的发票数据\n4. 确保所有必要字段都被正确识别和填充\n5. 正确处理发票代码和发票号码合并的情况\n6. 适当处理航空电子客运发票的特殊格式\n7. 对于新版火车票，在无法直接提取税额时进行准确计算\n\n## Skills\n\n- 精通各类电子发票结构和内容，包括最新的格式变化和特殊发票类型\n- 熟练使用图像识别技术提取发票信息\n- 擅长数据整理和格式化\n- 熟悉JSON数据格式\n- 注重细节，保证数据的准确性和完整性\n- 能够灵活处理不同格式的发票信息，包括航空电子客运发票\n- 熟悉特殊发票的税额计算方法\n\n## Workflows\n\n1. 接收电子发票图像链接\n2. 使用图像识别工具提取发票信息\n3. 识别发票类型和格式\n4. 根据发票类型采取相应的信息提取策略：\n   - 普通发票：正常提取所有字段\n   - 合并格式发票：将完整号码放入"发票号码"字段\n   - 航空电子客运发票：将电子客票号码放入"发票号码"字段\n   - 新版火车票：尝试提取税额，如果无法提取则根据金额计算\n5. 整理提取的信息，确保包含所有必要字段\n6. 对于新版火车票，如果税额未提取到，进行税额计算\n7. 将整理后的信息转换为JSON格式\n8. 检查输出数据的完整性和准确性\n9. 返回最终的JSON格式数据\n\n## Rules\n\n1. 必须提取的字段包括: "发票代码"、"发票号码"、"开票日期"、"开票类目"、"金额"、"税额"、"发票类型"\n2. 所有提取的信息必须准确无误\n3. 输出必须使用JSON格式\n4. 如果某个字段在发票中不存在，应在JSON中将该字段值设为""\n5. 对于发票代码和发票号码合并的新格式发票：\n   - 将完整的合并号码填入"发票号码"字段\n   - "发票代码"字段应设置为""\n6. 对于航空电子客运发票：\n   - 将电子客票号码填入"发票号码"字段\n   - "发票代码"字段应设置为""\n7. 对于新版火车票：\n   - 如果无法直接提取税额，使用以下公式计算：\n     税额 = 票面金额 ÷ (1 + 9%) × 9%\n   - 计算结果保留两位小数\n8. "发票类型"字段应准确反映发票的类型，如"增值税电子普通发票"、"航空电子客运发票"、"铁路电子客票"等\n9. 保持数据格式的一致性，即使处理多张不同类型的发票\n\n## Output Format\n\n{\n  "发票代码": "string or  ",\n  "发票号码": "string",\n  "开票日期": "string",\n  "开票类目": "string",\n  "金额": "number",\n  "税额": "number",\n  "发票类型": "string"\n}\n\n## Initialization\n\n作为财务发票整理专家，我已准备好协助您处理各种类型的电子发票信息。我了解不同发票格式的特点，包括新格式发票将发票代码和发票号码合并的情况，以及航空电子客运发票只有电子客票号码的特殊情况。我会根据实际情况灵活处理这些信息，确保输出的JSON数据格式统一且准确。请提供需要处理的电子发票图像链接，我将为您提取关键信息并以JSON格式输出。如果您有任何特殊要求或额外的处理需求，请告诉我。让我们开始工作吧！'}, {'id': 'b071a2e9-7551-467d-8798-86220c5d8b2e', 'role': 'user', 'text': '{{#sys.files#}}'}],
            context={'enabled': False, 'variable_selector': []},
            variables=[],
        )
    )

    # 添加条件分支 5节点
    workflow.add_node(
        id="node_1754375238834",
        position={'x': 1009.5132630354576, 'y': 511.0876181312255},
        state=DifyIfElseState(
            title="条件分支 5",
        )
    )

    # 添加直接回复 2 (1)节点
    workflow.add_node(
        id="node_17543752722170",
        position={'x': 1286.8619528051909, 'y': 486.80694330551114},
        state=DifyAnswerState(
            title="直接回复 2 (1)",
            variables=[],
        )
    )

    # 添加连接边
    workflow.add_edge("node_17514479903070", "node_1749116054395")
    workflow.add_edge("node_1749116054395", "answer")
    workflow.add_edge("node_1749115381294", "node_17514490270830")
    workflow.add_edge("node_17514490270830", "answer")
    workflow.add_edge("node_1749105824146", "node_17514479903070")
    workflow.add_edge("node_1751447829988", "node_1749105824146")
    workflow.add_edge("node_17542127425600", "node_1749115381294")
    workflow.add_edge("node_1751447829988", "node_17542127425600")
    workflow.add_edge("node_1754212275955", "node_1751447829988")
    workflow.add_edge(START, "node_1754375238834")
    workflow.add_edge("node_1754375238834", "node_17543752722170")
    workflow.add_edge("node_1754375238834", "node_1754212275955")

    # 编译并保存
    yaml_result = workflow.compile()
    workflow.save("playground/dify/outputs/dify_workflow_output.yaml")
    print(f"工作流已生成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()