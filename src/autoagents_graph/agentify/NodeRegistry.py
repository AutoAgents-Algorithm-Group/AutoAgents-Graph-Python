NODE_TEMPLATES = {
    "httpInvoke": {
        "name": "HTTP调用",
        "intro": "1、发出一个HTTP请求，实现与其他应用服务的数据请求操作。\n\n2、可实现如搜索，数据库信息检索等复杂操作。",
        "category": "HTTP操作",
        "moduleType": "httpInvoke",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "url",
                "type": "textarea",
                "label": "请求地址",
                "value": "post(可选get,post,delete,put,patch) https://xxx\ndata-type json(可选json,form,query) \ntoken xxx\nheader2Key header2Value",
                "connected": False,
                "valueType": "string",
                "description": "输入目标请求链接"
            },
            {
                "key": "_requestBody_",
                "type": "target",
                "label": "全部请求参数",
                "connected": True,
                "valueType": "string",
                "description": "输入POST请求体完整的JSON数据"
            }
        ],
        "outputs": [
            {
                "key": "_success_",
                "type": "source",
                "label": "请求成功",
                "targets": [],
                "valueType": "boolean",
                "description": "http请求成功"
            },
            {
                "key": "_failed_",
                "type": "source",
                "label": "请求异常",
                "targets": [],
                "valueType": "boolean",
                "description": "http请求异常"
            },
            {
                "key": "_response_",
                "type": "source",
                "label": "请求结果",
                "targets": [],
                "valueType": "string",
                "description": "http请求返回的全部结果数据"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "请求完成后触发"
            }
        ]
    },
    "questionInput": {
        "name": "用户提问",
        "intro": "用户输入入口,对话中用户的输入信息,与其他模块连接,一般作为起始模块",
        "category": "用户提问",
        "moduleType": "questionInput",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "inputText",
                "type": "switch",
                "label": "输入文本",
                "value": True,
                "valueType": "boolean",
                "description": "输入文本开关"
            },
            {
                "key": "uploadFile",
                "type": "switch",
                "label": "上传文档",
                "value": False,
                "valueType": "boolean",
                "description": "上传文档开关"
            },
            {
                "key": "uploadPicture",
                "type": "switch",
                "label": "上传图片",
                "value": False,
                "valueType": "boolean",
                "description": "上传图片开关"
            },
            {
                "key": "fileUpload",
                "type": "switch",
                "label": "文档审查",
                "value": False,
                "valueType": "boolean",
                "description": "文档审查开关"
            },
            {
                "key": "fileContrast",
                "type": "checkBox",
                "label": "是否文档对比",
                "value": False,
                "valueType": "boolean",
                "description": "是否开启文档比对功能"
            },
            {
                "key": "fileInfo",
                "type": "table",
                "label": "文档分组",
                "value": [],
                "valueType": "any",
                "description": "上传的文件列表,如果开启了文档对比,每个分组只能上传一个文件"
            },
            {
                "key": "initialInput",
                "type": "hidden",
                "label": "是否作为初始全局input",
                "value": True,
                "valueType": "boolean",
                "description": "是否作为初始全局input"
            }
        ],
        "outputs": [
            {
                "key": "userChatInput",
                "type": "source",
                "label": "文本信息",
                "targets": [],
                "valueType": "string",
                "description": "引用变量：{{userChatInput}}"
            },
            {
                "key": "files",
                "type": "source",
                "label": "文档信息",
                "targets": [],
                "valueType": "file",
                "description": "以JSON数组格式输出用户上传文档列表，若为文档比对，包含分组信息"
            },
            {
                "key": "images",
                "type": "source",
                "label": "图片信息",
                "targets": [],
                "valueType": "image",
                "description": "以JSON数组格式输出用户上传的图片列表"
            },
            {
                "key": "unclickedButton",
                "type": "source",
                "label": "未点击按钮",
                "targets": [],
                "valueType": "boolean",
                "description": "当未点击任何按钮时值为true"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后开关打开,下游链接组件开始运行。"
            }
        ]
    },
    "aiChat": {
        "name": "智能对话",
        "intro": "AI 对话模型，根据信息输入和提示词（Prompt）加工生成所需信息，展示给用户，完成与用户互动。",
        "category": "大模型",
        "moduleType": "aiChat",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "text",
                "type": "target",
                "label": "信息输入",
                "value": "",
                "connected": True,
                "valueType": "string",
                "description": "引用变量：{{text}}"
            },
            {
                "key": "images",
                "type": "target",
                "label": "图片输入",
                "value": "",
                "connected": True,
                "valueType": "image",
                "description": "引用变量：{{images}}"
            },
            {
                "key": "knSearch",
                "type": "target",
                "label": "知识库搜索结果",
                "value": "",
                "connected": True,
                "valueType": "search",
                "description": "引用变量：{{knSearch}}"
            },
            {
                "key": "knConfig",
                "type": "target",
                "label": "知识库高级配置",
                "value": "...",
                "connected": False,
                "valueType": "text",
                "description": "知识库高级配置"
            },
            {
                "key": "historyText",
                "type": "inputNumber",
                "label": "聊天上下文",
                "value": 3,
                "min": 0,
                "max": 6,
                "step": 1,
                "connected": False,
                "valueType": "chatHistory",
                "description": ""
            },
            {
                "key": "model",
                "type": "selectChatModel",
                "label": "选择模型",
                "value": "glm-4-airx",
                "required": True,
                "valueType": "string",
                "description": ""
            },
            {
                "key": "quotePrompt",
                "type": "textarea",
                "label": "提示词 (Prompt)",
                "value": "请模拟成AI智能助手...",
                "valueType": "string",
                "description": "模型引导词"
            },
            {
                "key": "stream",
                "type": "switch",
                "label": "回复对用户可见",
                "value": True,
                "connected": False,
                "valueType": "boolean",
                "description": "控制回复内容是否输出给用户"
            },
            {
                "key": "temperature",
                "type": "slider",
                "label": "回复创意性",
                "value": 0,
                "min": 0,
                "max": 1,
                "step": 0.1,
                "markList": {
                    "0": "严谨",
                    "1": "创意"
                },
                "valueType": "number",
                "description": "控制回复创意性"
            },
            {
                "key": "maxToken",
                "type": "slider",
                "label": "回复字数上限",
                "value": 5000,
                "min": 100,
                "max": 5000,
                "step": 50,
                "markList": {
                    "5000": "5000"
                },
                "valueType": "number"
            }
        ],
        "outputs": [
            {
                "key": "isResponseAnswerText",
                "type": "source",
                "label": "回复结束",
                "targets": [],
                "valueType": "boolean",
                "description": "模型运行结束后触发"
            },
            {
                "key": "answerText",
                "type": "source",
                "label": "回复内容",
                "targets": [],
                "valueType": "string",
                "description": "大模型返回结果"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后触发"
            }
        ]
    },
    "confirmreply": {
        "name": "确定回复",
        "intro": "结合触发条件使用，输出预设内容或输出上游模块接入内容。",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "stream",
                "type": "switch",
                "label": "回复对用户可见",
                "value": True,
                "connected": False,
                "valueType": "boolean",
                "description": "控制回复内容是否输出给用户"
            },
            {
                "key": "text",
                "type": "textarea",
                "label": "回复内容",
                "value": "您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
                "connected": True,
                "valueType": "string",
                "description": "可以使用 \\n 来实现连续换行。\n\n可以通过外部模块输入实现回复，外部模块输入时会覆盖当前填写的内容。引用变量：{{text}}"
            }
        ],
        "outputs": [
            {
                "key": "text",
                "type": "source",
                "label": "回复内容",
                "value": "",
                "valueType": "string",
                "description": "回复内容原样输出。"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后开关打开，下游链接组件开始运行。"
            }
        ],
        "category": "大模型",
        "disabled": False,
        "moduleType": "confirmreply"
    },
    "knowledgesSearch": {
        "name": "知识库搜索",
        "intro": "在知识库中搜索结果，智能对话模块根据搜索结果进行回答，让回答更精准。",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "text",
                "type": "target",
                "label": "信息输入",
                "value": "",
                "connected": True,
                "valueType": "string",
                "description": "引用变量：{{text}}"
            },
            {
                "key": "datasets",
                "type": "selectDataset",
                "label": "关联的知识库",
                "value": [],
                "required": True,
                "valueType": "selectDataset",
                "description": ""
            },
            {
                "key": "similarity",
                "max": 1,
                "min": 0,
                "step": 0.01,
                "type": "slider",
                "label": "相似度阈值",
                "value": 0.2,
                "markList": {
                    "0": 0,
                    "1": 1
                },
                "valueType": "number",
                "description": "我们使用混合相似度得分来评估用户问题与知识库切片的相似度。它由关键词相似度和向量余弦相似度加权计算得到。如果问题和切片之间的相似度小于此阈值，则该切片将被过滤掉。"
            },
            {
                "key": "vectorSimilarWeight",
                "max": 1,
                "min": 0,
                "step": 0.01,
                "type": "slider",
                "label": "向量相似度权重",
                "value": 1,
                "markList": {
                    "0": 0,
                    "1": 1
                },
                "valueType": "number",
                "description": "我们使用混合相似度得分来评估用户问题与知识库切片的相似度。它由关键词相似度和向量余弦相似度加权计算得到。两个相似度权重之和为1。例如，向量相似度权重为0.9，则关键词相似度为0.1。默认向量相似度为1，即只使用向量检索。建议当您的问题中存在明确的名称，地址，号码等关键词时，降低向量相似度权重，.00000.使用向量检索与关键词检索混合相似度得分。"
            },
            {
                "key": "topK",
                "max": 100,
                "min": 0,
                "step": 1,
                "type": "slider",
                "label": "召回数",
                "value": 20,
                "markList": {
                    "0": 0,
                    "100": 100
                },
                "valueType": "number",
                "description": "在满足相似度阈值的前提下，按照相似度从大到小排序，召回的相关切片的数量。"
            },
            {
                "key": "enableRerank",
                "type": "switch",
                "label": "是否开启重排序",
                "value": False,
                "valueType": "boolean",
                "description": "重排序模型是用于根据用户问题的相关性对已召回的切片进行重新排序的模型。其主要目的是提高搜索结果的精确度和相关性，确保用户查询能够获得最有价值和最相关的信息。注意：重排序模型资源消耗较大，开启后会降低检索速度。"
            },
            {
                "key": "rerankModelType",
                "type": "selectRerankModel",
                "label": "重排序模型",
                "value": "oneapi-xinference:bce-rerank",
                "required": True,
                "valueType": "selectChatModel",
                "description": ""
            },
            {
                "key": "rerankTopK",
                "max": 20,
                "min": 0,
                "step": 1,
                "type": "slider",
                "label": "重排序召回数",
                "value": 10,
                "markList": {
                    "0": 0,
                    "20": 20
                },
                "valueType": "number",
                "description": "根据重排序模型的打分，按照相关性从大到小排序，召回的相关切片数量。"
            }
        ],
        "outputs": [
            {
                "key": "isEmpty",
                "type": "source",
                "label": "未搜索到相关知识",
                "targets": [],
                "valueType": "boolean",
                "description": "当没有符合要求的文本切片时，该开关打开，可通过连接确定回复或智能对话模块的触发条件，启动下游模块。"
            },
            {
                "key": "unEmpty",
                "type": "source",
                "label": "搜索到相关知识",
                "targets": [],
                "valueType": "boolean",
                "description": "当搜索到符合要求的文本切片时，该开关打开，可通过连接确定回复或智能对话模块的触发条件，启动下游模块。"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后开关打开，下游链接组件开始运行。"
            },
            {
                "key": "quoteQA",
                "type": "source",
                "label": "知识库搜索结果",
                "targets": [],
                "valueType": "search",
                "description": "始终返回数组，内容包含相似度达和切片数量约定的内容，可通过【未搜索到相关知识】和【搜索到相关知识】控制后续回复内容。引用变量：{{quoteQA}}"
            }
        ],
        "category": "知识库",
        "disabled": False,
        "moduleType": "knowledgesSearch"
    },
    "pdf2md": {
        "name": "通用文档解析",
        "intro": "通用文档解析，将pdf/doc等转成markdown格式",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "files",
                "type": "target",
                "label": "文档信息",
                "value": "",
                "connected": True,
                "valueType": "file",
                "description": ""
            },
            {
                "key": "pdf2mdType",
                "type": "selectPdf2mdModel",
                "label": "选择模型",
                "value": "general",
                "required": True,
                "valueType": "selectPdf2mdModel",
                "description": ""
            }
        ],
        "outputs": [
            {
                "key": "pdf2mdResult",
                "type": "source",
                "label": "识别结果",
                "targets": [],
                "valueType": "string",
                "description": "识别结果"
            },
            {
                "key": "success",
                "type": "source",
                "label": "执行成功",
                "targets": [],
                "valueType": "boolean"
            },
            {
                "key": "failed",
                "type": "source",
                "label": "执行异常",
                "targets": [],
                "valueType": "boolean"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后开关打开，下游链接组件开始运行。"
            }
        ],
        "disabled": False,
        "moduleType": "pdf2md"
    },
    "addMemoryVariable": {
        "name": "添加记忆变量",
        "intro": "使用该组件将变量存为记忆变量后，可以在智能体的其他组件中引用",
        "outputs": [],
        "inputs": [
          {
            "key": "feedback",
            "type": "agentMemoryVar",
            "label": "用户反馈内容",
            "description": "",
            "valueType": "string",
            "connected": True,
            "targets": []
          }
        ],
        "category": "高阶能力",
        "moduleType": "addMemoryVariable"
    },
    "infoClass":{
        "name": "信息分类",
        "intro": "根据提示词完成信息分类，且不同的信息类型配置不同的回复方式和内容。",
        "category": "大模型",
        "disabled": False,
        "moduleType": "infoClass",
        "inputs": [
          {
            "key": "switch",
            "type": "target",
            "label": "联动激活",
            "value": False,
            "keyType": "trigger",
            "connected": True,
            "valueType": "boolean",
            "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
          },
          {
            "key": "switchAny",
            "type": "target",
            "label": "任一激活",
            "value": False,
            "keyType": "triggerAny",
            "connected": True,
            "valueType": "boolean",
            "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
          },
          {
            "key": "text",
            "type": "target",
            "label": "信息输入",
            "value": "",
            "connected": True,
            "valueType": "string",
            "description": "引用变量：{{text}}"
          },
          {
            "key": "knSearch",
            "type": "target",
            "label": "知识库搜索结果",
            "value": "",
            "connected": True,
            "valueType": "search",
            "description": "引用变量：{{knSearch}}"
          },
          {
            "key": "knConfig",
            "type": "target",
            "label": "知识库高级配置",
            "value": "## Role:知识问答专家\n        ## Goals:\n        - 根据知识库检索到的知识，结合聊天上下文信息，回答用户提问\n        ## Constrains：\n        - 严格根据知识库内容回答问题\n        - 知识库检索知识无法满足问题回答时，需严谨的回答问题\n        ## Rules\n        - 知识库检索知识中， instruction 是相关知识内容或问答对的问题,answer是预期回答。\n        ## 参考内容：\n        ### 知识库检索知识：\n        \"\"\"\n        {{quote}}\n        \"\"\"\n        ## 用户提问：\n        \"{{question}}\"\n",
            "connected": False,
            "valueType": "text",
            "description": "知识库高级配置"
          },
          {
            "key": "historyText",
            "max": 6,
            "min": 0,
            "step": 1,
            "type": "inputNumber",
            "label": "聊天上下文",
            "value": 3,
            "connected": False,
            "valueType": "chatHistory",
            "description": ""
          },
          {
            "key": "model",
            "type": "selectChatModel",
            "label": "选择模型",
            "value": "",
            "required": True,
            "valueType": "string",
            "description": ""
          },
          {
            "key": "quotePrompt",
            "type": "textarea",
            "label": "提示词 (Prompt)",
            "value": "请扮演文本分类器，根据信息输入和聊天上下文，判断输入信息属于哪种分类，以JSON格式输出分类信息。",
            "valueType": "string",
            "description": "简单分类无需调整提示词，可补充逻辑判断描述。"
          },
          {
            "key": "labels",
            "type": "addLabel",
            "label": "标签",
            "value": [],
            "valueType": "boolean",
            "description": "引用变量：{{labels}}"
          }
        ],
        "outputs": [
          {
            "key": "matchResult",
            "type": "source",
            "label": "分类结果",
            "targets": [],
            "valueType": "string",
            "description": "以JSON格式输出信息分类结果"
          },
          {
            "key": "finish",
            "type": "source",
            "label": "模块运行结束",
            "targets": [],
            "valueType": "boolean",
            "description": "运行完成后开关打开，下游链接组件开始运行。"
          }
        ]
    },
    "codeFragment": {
        "name": "代码块",
        "intro": "通过编写代码对输入数据进行精确的处理与加工",
        "category": "高阶能力",
        "disabled": False,
        "moduleType": "codeFragment",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "_language_",
                "type": "radio",
                "label": "语言",
                "value": "js",
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
                "valueType": "string",
                "description": "选择编程语言"
            },
            {
                "key": "_description_",
                "type": "textarea",
                "label": "代码描述",
                "connected": False,
                "valueType": "string",
                "description": "代码描述，非必填"
            },
            {
                "key": "_code_",
                "type": "textarea",
                "label": "代码内容",
                "value": "(\n      function userFunction(param) { \n        var input1 = param['input_key'];\n        var result = {};\n        result['output_key'] = input1 + \" append string\";\n        return result;\n      }\n )",
                "connected": False,
                "valueType": "string",
                "description": "用户编写的函数，Python函数名需指定为userFunction，输入输出为Key-Value数据类型，Key为String类型，Key和入参和岀参的设置对应"
            }
        ],
        "outputs": [
            {
                "key": "_runSuccess_",
                "type": "source",
                "label": "执行成功",
                "targets": [],
                "valueType": "boolean",
                "description": "代码执行成功"
            },
            {
                "key": "_runFailed_",
                "type": "source",
                "label": "执行异常",
                "targets": [],
                "valueType": "boolean",
                "description": "代码执行异常"
            },
            {
                "key": "_runResult_",
                "type": "source",
                "label": "执行结果",
                "targets": [],
                "valueType": "string",
                "description": "代码执行的全部结果"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "required": False,
                "valueType": "boolean",
                "description": "运行完成后开关打开,下游链接组件开始运行。"
            }
        ]
    },
    "forEach": {
        "name": "循环",
        "intro": "依次读取输入数组中的元素，执行循环流程",
        "category": "高阶能力",
        "disabled": False,
        "moduleType": "forEach",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "items",
                "type": "target",
                "label": "信息输入",
                "value": "",
                "connected": True,
                "valueType": "any",
                "description": "JSON数组或者目标对象"
            },
            {
                "key": "index",
                "type": "loopMemoryVar",
                "label": "元素序号",
                "connected": False,
                "valueType": "number",
                "description": "记录执行循环的次数"
            },
            {
                "key": "item",
                "type": "loopMemoryVar",
                "label": "元素值",
                "connected": False,
                "valueType": "string",
                "description": "记录执行数组的内容"
            },
            {
                "key": "length",
                "type": "loopMemoryVar",
                "label": "数组长度",
                "connected": False,
                "valueType": "number",
                "description": "执行数组的长度"
            },
            {
                "key": "loopEnd",
                "type": "target",
                "label": "循环单元终点",
                "connected": True,
                "valueType": "boolean",
                "description": "循环单元终点"
            }
        ],
        "outputs": [
            {
                "key": "loopStart",
                "type": "source",
                "label": "循环单元起点",
                "targets": [],
                "valueType": "boolean",
                "description": "循环单元起点"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后开关打开,下游链接组件开始运行。"
            }
        ],
    }
}