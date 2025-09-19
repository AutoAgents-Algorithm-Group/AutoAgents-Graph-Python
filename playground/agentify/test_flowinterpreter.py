import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph.agentify import FlowInterpreter, START


def main():    
    # JSON数据：包含完整的工作流信息
    json_data = {
        "nodes": [
            {
                "id": "simpleInputId",
                "type": "custom",
                "initialized": False,
                "position": {"x": 0, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "string", "description": "引用变量：{{userChatInput}}", "label": "文本信息", "type": "source", "targets": [], "key": "userChatInput"},
                        {"valueType": "file", "description": "以JSON数组格式输出用户上传文档列表", "label": "文档信息", "type": "source", "targets": [], "key": "files"},
                        {"valueType": "boolean", "description": "运行完成后开关打开", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "questionInput",
                    "inputs": [
                        {"valueType": "boolean", "label": "输入文本", "type": "switch", "value": True, "key": "inputText"},
                        {"valueType": "boolean", "label": "上传文档", "type": "switch", "value": True, "key": "uploadFile"}
                    ],
                    "name": "用户提问"
                }
            },
            {
                "id": "pdf2md1",
                "type": "custom",
                "position": {"x": 500, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "string", "label": "识别结果", "type": "source", "targets": [], "key": "pdf2mdResult"},
                        {"valueType": "boolean", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "pdf2md",
                    "inputs": [
                        {"valueType": "file", "label": "文档信息", "type": "target", "key": "files"},
                        {"valueType": "selectPdf2mdModel", "label": "选择模型", "value": "deep_pdf2md", "key": "pdf2mdType"}
                    ],
                    "name": "通用文档解析"
                }
            },
            {
                "id": "confirmreply1",
                "type": "custom",
                "position": {"x": 1000, "y": 300},
                "data": {
                    "outputs": [
                        {"valueType": "string", "label": "回复内容", "type": "source", "key": "text"},
                        {"valueType": "boolean", "label": "模块运行结束", "type": "source", "targets": [], "key": "finish"}
                    ],
                    "moduleType": "confirmreply",
                    "inputs": [
                        {"valueType": "boolean", "label": "回复对用户可见", "type": "switch", "value": True, "key": "stream"},
                        {"valueType": "string", "label": "回复内容", "type": "textarea", "value": "文件内容：{{@pdf2md1_pdf2mdResult}}", "key": "text"}
                    ],
                    "name": "确定回复"
                }
            }
        ],
        "edges": [
            {"source": "simpleInputId", "target": "pdf2md1", "sourceHandle": "finish", "targetHandle": "switchAny"},
            {"source": "simpleInputId", "target": "pdf2md1", "sourceHandle": "files", "targetHandle": "files"},
            {"source": "pdf2md1", "target": "confirmreply1", "sourceHandle": "finish", "targetHandle": "switchAny"}
        ]
    }

    # 创建FlowInterpreter实例
    interpreter = FlowInterpreter(
        auth_key="7217394b7d3e4becab017447adeac239",
        auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )
    
    # 生成SDK代码
    generated_code = interpreter.from_json_to_code(json_data)

    # 保存生成的代码
    with open("generated_workflow.py", "w", encoding="utf-8") as f:
        f.write(generated_code)


if __name__ == "__main__":
    main()