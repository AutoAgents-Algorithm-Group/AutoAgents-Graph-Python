import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.autoagents_graph.engine.agentify import AgentifyParser


def main():
    # JSON数据：包含完整的工作流信息
    json_data = {
    "nodes": [
        {
            "id": "simpleInputId",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": -2050.0187299418194,
                "y": 168.1277274588137
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "引用变量：{{userChatInput}}",
                        "label": "文本信息",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "text",
                                "target": "info_class"
                            },
                            {
                                "targetHandle": "text",
                                "target": "ai_chat_2"
                            }
                        ],
                        "key": "userChatInput"
                    },
                    {
                        "valueType": "file",
                        "description": "以JSON数组格式输出用户上传文档列表，若为文档比对，包含分组信息",
                        "label": "文档信息",
                        "type": "source",
                        "targets": [],
                        "key": "files"
                    },
                    {
                        "valueType": "image",
                        "description": "以JSON数组格式输出用户上传的图片列表",
                        "label": "图片信息",
                        "type": "source",
                        "targets": [],
                        "key": "images"
                    },
                    {
                        "valueType": "boolean",
                        "description": "当未点击任何按钮时值为True",
                        "label": "未点击按钮",
                        "type": "source",
                        "targets": [],
                        "key": "unclickedButton"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "info_class"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "questionInput",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "valueType": "boolean",
                        "description": "输入文本开关",
                        "label": "输入文本",
                        "type": "switch",
                        "value": True,
                        "key": "inputText"
                    },
                    {
                        "valueType": "boolean",
                        "description": "上传文档开关",
                        "label": "上传文档",
                        "type": "switch",
                        "value": False,
                        "key": "uploadFile"
                    },
                    {
                        "valueType": "boolean",
                        "description": "上传图片开关",
                        "label": "上传图片",
                        "type": "switch",
                        "value": False,
                        "key": "uploadPicture"
                    },
                    {
                        "valueType": "boolean",
                        "description": "文档审查开关",
                        "label": "文档审查",
                        "type": "switch",
                        "value": False,
                        "key": "fileUpload"
                    },
                    {
                        "valueType": "boolean",
                        "description": "是否开启文档比对功能",
                        "label": "是否文档对比",
                        "type": "checkBox",
                        "value": False,
                        "key": "fileContrast"
                    },
                    {
                        "valueType": "any",
                        "description": "上传的文件列表,如果开启了文档对比,每个分组只能上传一个文件",
                        "label": "文档分组",
                        "type": "table",
                        "value": [],
                        "key": "fileInfo"
                    },
                    {
                        "valueType": "boolean",
                        "description": "是否作为初始全局input",
                        "label": "是否作为初始全局input",
                        "type": "hidden",
                        "value": True,
                        "key": "initialInput"
                    }
                ],
                "intro": "用户输入入口,对话中用户的输入信息,与其他模块连接,一般作为起始模块",
                "name": "用户提问",
                "disabled": False,
                "category": "用户提问"
            }
        },
        {
            "id": "confirm_reply_3",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": -873.0587219566071,
                "y": 2123.791172048472
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": True,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "不同设备类型正在开发中，敬请期待！",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "ai_chat_2",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": -861.8967916173706,
                "y": 187.8637781812438
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "boolean",
                        "description": "当模型运行结束，生成所有内容后，则回复结束下游组件开启。",
                        "label": "回复结束",
                        "type": "source",
                        "targets": [],
                        "key": "isResponseAnswerText"
                    },
                    {
                        "valueType": "string",
                        "description": "大模型处理完的信息，将作为回复内容进行输出。引用变量：",
                        "label": "回复内容",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "input_key",
                                "target": "code_fragment_1"
                            }
                        ],
                        "key": "answerText"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "code_fragment_1"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "aiChat",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "引用变量：{{text}}",
                        "label": "信息输入",
                        "type": "target",
                        "value": "",
                        "key": "text"
                    },
                    {
                        "connected": True,
                        "valueType": "image",
                        "description": "引用变量：{{images}}",
                        "label": "图片输入",
                        "type": "target",
                        "value": [],
                        "key": "images"
                    },
                    {
                        "connected": True,
                        "valueType": "search",
                        "description": "引用变量：{{knSearch}}",
                        "label": "知识库搜索结果",
                        "type": "target",
                        "value": "",
                        "key": "knSearch"
                    },
                    {
                        "connected": False,
                        "valueType": "text",
                        "description": "知识库高级配置",
                        "label": "知识库高级配置",
                        "type": "target",
                        "value": "",
                        "key": "knConfig"
                    },
                    {
                        "connected": False,
                        "min": 0,
                        "max": 6,
                        "valueType": "chatHistory",
                        "description": "",
                        "step": 1,
                        "label": "聊天上下文",
                        "type": "inputNumber",
                        "value": 3,
                        "key": "historyText"
                    },
                    {
                        "valueType": "string",
                        "description": "",
                        "label": "选择模型",
                        "type": "selectChatModel",
                        "value": "oneapi-siliconflow:deepseek-ai/DeepSeek-R1",
                        "key": "model",
                        "required": True
                    },
                    {
                        "valueType": "string",
                        "description": "设定模型的角色和行为模式，如设定人设和回复逻辑。",
                        "label": "系统提示词",
                        "type": "textarea",
                        "value": "",
                        "key": "systemPrompt"
                    },
                    {
                        "valueType": "string",
                        "description": "用户输入的具体问题或请求，向模型提供用户指令。",
                        "label": "用户提示词",
                        "type": "textarea",
                        "value": "",
                        "key": "quotePrompt"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": False,
                        "key": "stream"
                    },
                    {
                        "min": 0,
                        "max": 1,
                        "markList": {
                            "0": "严谨",
                            "1": "创意"
                        },
                        "valueType": "number",
                        "description": "控制回复创意性，如果想要和输入信息一致的答案，数值越小越好；如果想要模型发挥创意性，数值越大越好。",
                        "step": 0.1,
                        "label": "回复创意性",
                        "type": "slider",
                        "value": 0,
                        "key": "temperature"
                    },
                    {
                        "min": 0,
                        "max": 1,
                        "markList": {
                            "0": "0",
                            "1": "1"
                        },
                        "valueType": "number",
                        "description": "控制输出的多样性,值越大输出包括更多单词选项；值越小，输出内容更集中在高概率单词上，即输出更确定但缺少多样性。一般【回复创意性】和【核采样TOP_P】只设置一个。",
                        "step": 0.1,
                        "label": "核采样TOP_P",
                        "type": "slider",
                        "value": 1,
                        "key": "topP"
                    },
                    {
                        "min": 100,
                        "max": 4096,
                        "markList": {
                            "4096": 4096,
                            "5000": "5000"
                        },
                        "valueType": "number",
                        "step": 50,
                        "label": "回复字数上限",
                        "type": "slider",
                        "value": 4096,
                        "key": "maxToken"
                    }
                ],
                "intro": "AI 对话模型，根据信息输入和提示词（Prompt）加工生成所需信息，展示给用户，完成与用户互动。",
                "name": "智能对话",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "confirm_reply_5",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 1050.058092873814,
                "y": 114.82823978954264
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [
                            {
                                "targetHandle": "sql",
                                "target": "database_query_1"
                            }
                        ],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_7"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": False,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "SELECT\n  SBLX AS \"设备类型\",\n  EQUIP_NAME AS \"设备名称\",\n  SCCJ AS \"生产厂家\",\n  TYRQ AS \"投运日期\"\nFROM nusp_fac_equipment\nWHERE xjdw LIKE {{geo}};",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "code_fragment_1",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": -319.49586685447025,
                "y": 155.25565264027563
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "boolean",
                        "description": "代码执行成功",
                        "label": "执行成功",
                        "type": "source",
                        "targets": [],
                        "key": "_runSuccess_"
                    },
                    {
                        "valueType": "boolean",
                        "description": "代码执行异常",
                        "label": "执行异常",
                        "type": "source",
                        "targets": [],
                        "key": "_runFailed_"
                    },
                    {
                        "valueType": "string",
                        "description": "代码执行的全部结果",
                        "label": "执行结果",
                        "type": "source",
                        "targets": [],
                        "key": "_runResult_"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_6"
                            }
                        ],
                        "key": "finish",
                        "required": False
                    },
                    {
                        "valueType": "string",
                        "description": "",
                        "label": "output_key",
                        "type": "parameter",
                        "targets": [
                            {
                                "targetHandle": "geo",
                                "target": "memory_var_1"
                            },
                            {
                                "targetHandle": "text",
                                "target": "confirm_reply_6"
                            }
                        ],
                        "key": "output_key"
                    }
                ],
                "moduleType": "codeFragment",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "",
                        "label": "input_key",
                        "type": "parameter",
                        "key": "input_key"
                    },
                    {
                        "valueType": "string",
                        "options": [
                            {
                                "label": "javascript",
                                "value": "js"
                            },
                            {
                                "label": "python",
                                "value": "python"
                            }
                        ],
                        "description": "选择编程语言",
                        "label": "语言",
                        "type": "radio",
                        "value": "python",
                        "key": "_language_"
                    },
                    {
                        "connected": False,
                        "valueType": "string",
                        "description": "代码描述，非必填",
                        "label": "代码描述",
                        "type": "textarea",
                        "value": "",
                        "key": "_description_"
                    },
                    {
                        "connected": False,
                        "valueType": "string",
                        "description": "用户编写的函数，Python函数名需指定为userFunction，输入输出为Key-Value数据类型，Key为String类型，Key和入参和岀参的设置对应",
                        "label": "代码内容",
                        "type": "textarea",
                        "value": "import re\n\ndef userFunction(params):\n    def extract_after_think(info):\n        # 使用正则表达式匹配第一个</think>之后的所有内容\n        match = re.search(r'</think>(.*)', info, re.DOTALL)\n        if match:\n            return match.group(1).strip()  # 返回匹配到的内容并去除首尾空白\n        else:\n            return info\n\n    result = {}\n    try:\n        # 提取内容并保存到result中\n         temp = extract_after_think(params['input_key'])\n         temprp = temp.replace('\\n', '')\n         result['output_key'] = \"'%\" + temprp +\"%'\"\n    except Exception as e:\n        # 捕获可能的异常并记录错误信息\n        result['error'] = str(e)\n\n    return result",
                        "key": "_code_"
                    }
                ],
                "intro": "通过编写代码对输入数据进行精确的处理与加工",
                "name": "代码块",
                "disabled": False,
                "category": "高阶能力"
            }
        },
        {
            "id": "memory_var_1",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 187.41334017570892,
                "y": 131.6960333509331
            },
            "data": {
                "outputs": [],
                "moduleType": "addMemoryVariable",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "",
                        "label": "geo",
                        "type": "agentMemoryVar",
                        "targets": [],
                        "key": "geo"
                    }
                ],
                "intro": "使用该组件将变量存为记忆变量后，可以在智能体的其他组件中引用",
                "name": "添加记忆变量",
                "disabled": False,
                "category": "高阶能力"
            }
        },
        {
            "id": "confirm_reply_6",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 591.6882106464707,
                "y": 135.4006165467965
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_5"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": False,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "database_query_1",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 2402.86927334456,
                "y": 110.86520200031254
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "SQL查询的全部结果",
                        "label": "查询结果",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "queryResult"
                    },
                    {
                        "valueType": "boolean",
                        "description": "SQL查询执行成功",
                        "label": "调用成功",
                        "type": "source",
                        "value": False,
                        "targets": [],
                        "key": "success"
                    },
                    {
                        "valueType": "boolean",
                        "description": "SQL查询执行异常",
                        "label": "调用失败",
                        "type": "source",
                        "value": False,
                        "targets": [],
                        "key": "failed"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_8"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "databaseQuery",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "数据查询sql",
                        "label": "SQL",
                        "type": "target",
                        "value": "",
                        "key": "sql"
                    },
                    {
                        "connected": False,
                        "databaseUuid": "793a32627a094b41a7d52e5443b7857b",
                        "valueType": "string",
                        "description": "查询的数据库",
                        "label": "查询的数据库",
                        "type": "selectDatabase",
                        "value": {},
                        "key": "database"
                    },
                    {
                        "valueType": "boolean",
                        "description": "显示查询结果",
                        "label": "显示查询结果",
                        "type": "switch",
                        "value": True,
                        "key": "showTable"
                    }
                ],
                "intro": "数据库查询",
                "name": "数据库查询",
                "disabled": False,
                "category": "数据库"
            }
        },
        {
            "id": "confirm_reply_7",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 1543.7577279314946,
                "y": 156.21737446259584
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_10"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": True,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "基本信息如下",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "confirm_reply_8",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 1067.1535700820075,
                "y": 890.5267338164495
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [
                            {
                                "targetHandle": "sql",
                                "target": "database_query_2"
                            }
                        ],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_9"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": False,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "SELECT\nCONTENT as '故障事件内容',\nOCCUR_TIME as '故障发生时间',\nBUSI_TYPE_NAME as '故障业务类型名称',\nBUSI_TYPE_SUBCLASS as '故障业务子类名称'\nFROM\n    T_EVENT_ZNJS_DWXXJS t1\nWHERE\n    t1.EQUIP_ID in (select `EQUIP_ID` from nusp_fac_equipment \nwhere xjdw like {{geo}});",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "confirm_reply_9",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 1574.6426907565042,
                "y": 892.7600770675024
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "database_query_2"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": True,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "发生的历史故障如下",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "database_query_2",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 2080.157377078698,
                "y": 864.3978662788228
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "SQL查询的全部结果",
                        "label": "查询结果",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "queryResult"
                    },
                    {
                        "valueType": "boolean",
                        "description": "SQL查询执行成功",
                        "label": "调用成功",
                        "type": "source",
                        "value": False,
                        "targets": [],
                        "key": "success"
                    },
                    {
                        "valueType": "boolean",
                        "description": "SQL查询执行异常",
                        "label": "调用失败",
                        "type": "source",
                        "value": False,
                        "targets": [],
                        "key": "failed"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [],
                        "key": "finish"
                    }
                ],
                "moduleType": "databaseQuery",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "数据查询sql",
                        "label": "SQL",
                        "type": "target",
                        "value": "",
                        "key": "sql"
                    },
                    {
                        "connected": False,
                        "databaseUuid": "793a32627a094b41a7d52e5443b7857b",
                        "valueType": "string",
                        "description": "查询的数据库",
                        "label": "查询的数据库",
                        "type": "selectDatabase",
                        "value": {},
                        "key": "database"
                    },
                    {
                        "valueType": "boolean",
                        "description": "显示查询结果",
                        "label": "显示查询结果",
                        "type": "switch",
                        "value": True,
                        "key": "showTable"
                    }
                ],
                "intro": "数据库查询",
                "name": "数据库查询",
                "disabled": False,
                "category": "数据库"
            }
        },
        {
            "id": "info_class",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": -1479.7489037112273,
                "y": 151.55533226592678
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "以JSON格式输出信息分类结果",
                        "label": "分类结果",
                        "type": "source",
                        "targets": [],
                        "key": "matchResult"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [],
                        "key": "finish"
                    },
                    {
                        "valueType": "boolean",
                        "label": "查询地区设备清单",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "ai_chat_2"
                            }
                        ],
                        "key": "9f4da034-1f5c-44d4-9345-1cb53dfcbd61"
                    },
                    {
                        "valueType": "boolean",
                        "label": "不同设备",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "confirm_reply_3"
                            }
                        ],
                        "key": "1c8384d9-2910-4ae5-bb36-7b2853be955a"
                    }
                ],
                "moduleType": "infoClass",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "引用变量：{{text}}",
                        "label": "信息输入",
                        "type": "target",
                        "value": "",
                        "key": "text"
                    },
                    {
                        "connected": True,
                        "valueType": "search",
                        "description": "引用变量：{{knSearch}}",
                        "label": "知识库搜索结果",
                        "type": "target",
                        "value": "",
                        "key": "knSearch"
                    },
                    {
                        "connected": False,
                        "valueType": "text",
                        "description": "知识库高级配置",
                        "label": "知识库高级配置",
                        "type": "target",
                        "value": "",
                        "key": "knConfig"
                    },
                    {
                        "connected": False,
                        "min": 0,
                        "max": 6,
                        "valueType": "chatHistory",
                        "description": "",
                        "step": 1,
                        "label": "聊天上下文",
                        "type": "inputNumber",
                        "value": 0,
                        "key": "historyText"
                    },
                    {
                        "valueType": "string",
                        "description": "",
                        "label": "选择模型",
                        "type": "selectChatModel",
                        "value": "qwen2.5-72b-instruct",
                        "key": "model",
                        "required": True
                    },
                    {
                        "valueType": "string",
                        "description": "简单分类无需调整提示词，可补充逻辑判断描述。",
                        "label": "提示词 (Prompt)",
                        "type": "textarea",
                        "value": "你是电网行业问数智能体的二分类路由器。你的唯一任务：根据用户输入判定应走哪一个流程，并且只输出对应代号。\n\n输出代号（严格二选一，且必须输出其一）：\n查询地区设备清单\n不同设备：指设备事件/缺陷/跳闸等记录或统计\n决策优先级（从高到低，命中即停）：\n事件/统计关键词命中 → 不同设备。 事件/统计关键词示例（包含但不限于）：跳闸、缺陷、故障、检修、告警、录波、重合、统计、次数、对比、比较、趋势、最近、近一周/上月/季度、原因、厂家、是否遗留、是否移交综合室、值班人、记录、日志、处理、事故。\n清单/罗列关键词命中 → 查询地区设备清单。 清单关键词示例：清单、名单、有哪些、列出、罗列、一览、台账、盘点、汇总、分布、名录、列表。\n地名/站名/区域线索命中（即使是冷门或不在词典中）→ 查询地区设备清单。 判定启发式（任一满足即可视为区域线索）：\n后缀/词形：片区、区、市、县、旗、州、盟、镇、乡、村、园、园区、街、道、路、巷、岭、山、岛、湾、洲、滩、港、口、桥、湖、河、江、水库、矿、厂 等；\n设施/站点：变电站、开闭所、运维站、开关站、枢纽、站、所、#×主变（如“#1主变”常与站点/设备清单相关）；\n编码/别称：看似地名或站/所代号的短词/缩写/拼音/字母数字组合（如“GZ-01”“DF变”“临江新城”“洪泽洲”），即使很冷门也按区域线索处理；\n含“kV + 站/所”（如“110kV××站”）。\n模糊/极短输入的兜底：当未命中1)与2)，且输入很短或语义不明（如仅16个汉字或13个词），一律 → 查询地区设备清单。\n若仍无法判断（几乎不可能出现），绝不空输出，强制 → 查询地区设备清单。\n特殊歧义处理：\n仅出现设备类别或设备名（如“主变”“断路器”“XX线路”）但无事件/统计词且无清单词：默认 → 查询地区设备清单（视为想看该类设备分布/清单）。\n同时出现清单词与事件词时：以事件词优先 → 不同设备。\n输出规范（务必遵守）：\n严格只选择 查询地区设备清单 或 不同设备 之一。\n不输出任何其他字符、标点、空格、换行、前后缀或解释。",
                        "key": "quotePrompt"
                    },
                    {
                        "valueType": "boolean",
                        "description": "引用变量：{{labels}}",
                        "label": "标签",
                        "type": "addLabel",
                        "value": [
                            {
                                "value": "查询地区设备清单",
                                "key": "9f4da034-1f5c-44d4-9345-1cb53dfcbd61"
                            },
                            {
                                "value": "不同设备",
                                "key": "1c8384d9-2910-4ae5-bb36-7b2853be955a"
                            }
                        ],
                        "key": "labels"
                    }
                ],
                "intro": "根据提示词完成信息分类，且不同的信息类型配置不同的回复方式和内容。",
                "name": "信息分类",
                "disabled": False,
                "category": "大模型"
            }
        },
        {
            "id": "confirm_reply_10",
            "type": "custom",
            "initialized": False,
            "position": {
                "x": 1954.5790409016909,
                "y": 156.83070120629836
            },
            "data": {
                "outputs": [
                    {
                        "valueType": "string",
                        "description": "回复内容原样输出。",
                        "label": "回复内容",
                        "type": "source",
                        "value": "",
                        "targets": [],
                        "key": "text"
                    },
                    {
                        "valueType": "boolean",
                        "description": "运行完成后开关打开，下游链接组件开始运行。",
                        "label": "模块运行结束",
                        "type": "source",
                        "targets": [
                            {
                                "targetHandle": "switchAny",
                                "target": "database_query_1"
                            }
                        ],
                        "key": "finish"
                    }
                ],
                "moduleType": "confirmreply",
                "inputs": [
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游所有条件方可激活当前组件执行逻辑",
                        "label": "联动激活",
                        "type": "target",
                        "keyType": "trigger",
                        "value": False,
                        "key": "switch"
                    },
                    {
                        "connected": True,
                        "valueType": "boolean",
                        "description": "同时满足上游任一条件即可激活当前组件执行逻辑",
                        "label": "任一激活",
                        "type": "target",
                        "keyType": "triggerAny",
                        "value": False,
                        "key": "switchAny"
                    },
                    {
                        "connected": False,
                        "valueType": "boolean",
                        "description": "控制回复内容是否输出给用户",
                        "label": "回复对用户可见",
                        "type": "switch",
                        "value": False,
                        "key": "stream"
                    },
                    {
                        "connected": True,
                        "valueType": "string",
                        "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}",
                        "label": "回复内容",
                        "type": "textarea",
                        "value": "SELECT\n  SBLX AS \"设备类型\",\n  EQUIP_NAME AS \"设备名称\",\n  SCCJ AS \"生产厂家\",\n  TYRQ AS \"投运日期\"\nFROM nusp_fac_equipment\nWHERE xjdw LIKE '%慈溪%';",
                        "key": "text"
                    }
                ],
                "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
                "name": "确定回复",
                "disabled": False,
                "category": "大模型"
            }
        }
    ],
    "edges": [
        {
            "id": "ae87bfff-e243-4568-ba5e-abed78f520ca",
            "type": "custom",
            "source": "ai_chat_2",
            "target": "code_fragment_1",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": -537.8967916173706,
            "sourceY": 1736.8637629224547,
            "targetY": 282.7556526402756,
            "targetX": -321.49586685447025,
            "animated": False
        },
        {
            "id": "73854df4-c615-4b89-9745-39f061fb0b9f",
            "type": "custom",
            "source": "code_fragment_1",
            "target": "memory_var_1",
            "sourceHandle": "output_key",
            "targetHandle": "geo",
            "data": {},
            "label": "",
            "sourceX": 36.50413314552975,
            "sourceY": 982.2556221226976,
            "targetY": 216.19604860972217,
            "targetX": 183.41334017570892,
            "animated": False
        },
        {
            "id": "dd3deca5-4016-42da-bf85-94eeffc81c63",
            "type": "custom",
            "source": "code_fragment_1",
            "target": "confirm_reply_6",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 36.50413314552975,
            "sourceY": 936.2556221226976,
            "targetY": 272.9006318055856,
            "targetX": 587.6882106464707,
            "animated": False
        },
        {
            "id": "382f5234-c036-47cb-906e-67dab1170b77",
            "type": "custom",
            "source": "code_fragment_1",
            "target": "confirm_reply_6",
            "sourceHandle": "output_key",
            "targetHandle": "text",
            "data": {},
            "label": "",
            "sourceX": 36.50413314552975,
            "sourceY": 982.2556221226976,
            "targetY": 440.9006318055856,
            "targetX": 587.6882106464707,
            "animated": False
        },
        {
            "id": "fe59a264-47c7-4d36-920f-6937a2b5d1fe",
            "type": "custom",
            "source": "confirm_reply_6",
            "target": "confirm_reply_5",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 915.6882106464707,
            "sourceY": 661.4006318055856,
            "targetY": 252.32823978954264,
            "targetX": 1046.058092873814,
            "animated": False
        },
        {
            "id": "05ff6e28-b2f5-4ed1-82e6-85553e025fc7",
            "type": "custom",
            "source": "confirm_reply_5",
            "target": "confirm_reply_7",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 1374.058092873814,
            "sourceY": 640.8282397895426,
            "targetY": 293.71737446259584,
            "targetX": 1539.7577279314946,
            "animated": False
        },
        {
            "id": "bd4e52a8-21da-45a3-874e-50914e4b72c5",
            "type": "custom",
            "source": "database_query_1",
            "target": "confirm_reply_8",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 2766.86927334456,
            "sourceY": 733.8652325178907,
            "targetY": 1028.0267338164495,
            "targetX": 1063.1535700820075,
            "animated": False
        },
        {
            "id": "64b029e9-0bb8-4283-88f6-90e32346fa71",
            "type": "custom",
            "source": "confirm_reply_8",
            "target": "confirm_reply_9",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 1391.1535700820075,
            "sourceY": 1416.5267338164495,
            "targetY": 1030.2600160323461,
            "targetX": 1570.6426907565042,
            "animated": False
        },
        {
            "id": "7d0e23bf-5bc8-4687-9d61-6be29ab6dbf3",
            "type": "custom",
            "source": "confirm_reply_9",
            "target": "database_query_2",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 1898.6425686861917,
            "sourceY": 1418.7600160323461,
            "targetY": 1001.897927313979,
            "targetX": 2076.157377078698,
            "animated": False
        },
        {
            "id": "8030bed7-8a5b-4059-ad81-762f6125c7ea",
            "type": "custom",
            "source": "confirm_reply_8",
            "target": "database_query_2",
            "sourceHandle": "text",
            "targetHandle": "sql",
            "data": {},
            "label": "",
            "sourceX": 1391.1535700820075,
            "sourceY": 1370.5267338164495,
            "targetY": 1058.897927313979,
            "targetX": 2076.157377078698,
            "animated": False
        },
        {
            "id": "29233f0c-8bb9-423b-86ba-e31b136d0c00",
            "type": "custom",
            "source": "info_class",
            "target": "ai_chat_2",
            "sourceHandle": "9f4da034-1f5c-44d4-9345-1cb53dfcbd61",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": -1115.7489037112273,
            "sourceY": 1097.5553017483487,
            "targetY": 325.3637629224547,
            "targetX": -865.8967916173706,
            "animated": False
        },
        {
            "id": "c448d3e4-70a2-4b71-8b15-d4591bda6487",
            "type": "custom",
            "source": "simpleInputId",
            "target": "info_class",
            "sourceHandle": "userChatInput",
            "targetHandle": "text",
            "data": {},
            "label": "",
            "sourceX": -1726.0187299418194,
            "sourceY": 745.1277427176028,
            "targetY": 346.0553322659268,
            "targetX": -1483.7489037112273,
            "animated": False
        },
        {
            "id": "be70ae29-1ca7-4c3a-bad3-83e81f1d675c",
            "type": "custom",
            "source": "simpleInputId",
            "target": "ai_chat_2",
            "sourceHandle": "userChatInput",
            "targetHandle": "text",
            "data": {},
            "label": "",
            "sourceX": -1726.0187299418194,
            "sourceY": 745.1277427176028,
            "targetY": 382.3637629224547,
            "targetX": -865.8967916173706,
            "animated": False
        },
        {
            "id": "485b9e3d-c021-498d-a00f-c01676e6279d",
            "type": "custom",
            "source": "info_class",
            "target": "confirm_reply_3",
            "sourceHandle": "1c8384d9-2910-4ae5-bb36-7b2853be955a",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": -1115.7489037112273,
            "sourceY": 1143.5553017483487,
            "targetY": 2261.291172048472,
            "targetX": -877.0587219566071,
            "animated": False
        },
        {
            "id": "62933575-0c99-49e2-acfb-a7b26dfb45a8",
            "type": "custom",
            "source": "simpleInputId",
            "target": "info_class",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": -1726.0187299418194,
            "sourceY": 929.1277427176028,
            "targetY": 289.0553322659268,
            "targetX": -1483.7489037112273,
            "animated": False
        },
        {
            "id": "7a9f0d50-f3b3-4653-9445-efea1ebeca59",
            "type": "custom",
            "source": "confirm_reply_7",
            "target": "confirm_reply_10",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 1867.7578500018071,
            "sourceY": 682.217404980174,
            "targetY": 294.3306859475093,
            "targetX": 1950.5790409016909,
            "animated": False
        },
        {
            "id": "d7d1ce51-abdd-4506-b82f-445e521aa971",
            "type": "custom",
            "source": "confirm_reply_5",
            "target": "database_query_1",
            "sourceHandle": "text",
            "targetHandle": "sql",
            "data": {},
            "label": "",
            "sourceX": 1374.058092873814,
            "sourceY": 594.8282397895426,
            "targetY": 305.36520200031254,
            "targetX": 2398.86927334456,
            "animated": False
        },
        {
            "id": "29bdd989-6a29-43a2-beb0-dfe92c6d6fb1",
            "type": "custom",
            "source": "confirm_reply_10",
            "target": "database_query_1",
            "sourceHandle": "finish",
            "targetHandle": "switchAny",
            "data": {},
            "label": "",
            "sourceX": 2278.579040901691,
            "sourceY": 682.8306859475093,
            "targetY": 248.36520200031254,
            "targetX": 2398.86927334456,
            "animated": False
        },
        {
            "id": "vueflow__edge-ai_chat_2answerText-code_fragment_1input_key",
            "type": "custom",
            "source": "ai_chat_2",
            "target": "code_fragment_1",
            "sourceHandle": "answerText",
            "targetHandle": "input_key",
            "data": {},
            "label": "",
            "animated": False,
            "sourceX": -537.8967916173706,
            "sourceY": 1690.8637629224547,
            "targetX": -321.49586685447025,
            "targetY": 375.7556526402756
        }
    ],
    "position": [
        564.0687405660566,
        -186.51099284311113
    ],
    "zoom": 0.4873096957025821,
    "viewport": {
        "x": 564.0687405660566,
        "y": -186.51099284311113,
        "zoom": 0.4873096957025821
    }
}

    # 创建AgentifyParser实例
    interpreter = AgentifyParser(
        auth_key="7217394b7d3e4becab017447adeac239",
        auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn",
    )

    # 方法1: 生成SDK代码并自动保存（推荐）
    success = interpreter.generate_workflow_file(
        json_data, output_path=r"playground/agentify/outputs/generated_workflow.py", overwrite=True
    )

    if success:
        print("✅ 工作流文件生成成功！")
    else:
        print("❌ 工作流文件生成失败！")


if __name__ == "__main__":
    main()