import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph import NL2Workflow, AgentifyConfig
from src.autoagents_graph.engine.agentify import START
from src.autoagents_graph.engine.agentify.models import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,CodeFragmentState,InfoClassState,ForEachState,OfficeWordExportState,MarkdownToWordState,CodeExtractState,DatabaseQueryState

def main():
    workflow = NL2Workflow(
        platform="agentify",
        config=AgentifyConfig(
            # personal_auth_key="7217394b7d3e4becab017447adeac239",
            # personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
            jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiWkxsN21DVW0wWXRvUkxIT0JOM3VNMSttRzc5QWJGemdlc0hMc2dFWlJGNmtaeUszZTlSYUVBdFF0emo2Uy9hblVkelRpY1NVbGszQW11cnh3bHdQYk9Za3hwS1gzV2kvemlUbERHbExaNUNzcVpkUUtxM2s5WWlVY3Q4eEJkYm5TREJmc1EyaGhmUk96OXIzMVg1MnpoZ1ZoSzZNdmJiRzdGWktlaTIwd0VBR2RFeE50NTViRmlMSjNnNXhoOE5Kcm03bjlyM280dTZhS05BeXR4U2JHb0FteUxUVGZwZGxRbXMySnNoam9NVT0iLCJleHAiOjE3NjM2NTIzNTh9.xHyHrM2Vz1NauaPjvSdR8PEX0MM8rJdHVeujQ75qYrE",
            base_url="https://uat.agentspro.cn"
        )
    )

    # 添加节点
    # 用户提问节点
    workflow.add_node(
        id=START,
        position={'x': -2050.0187299418194, 'y': 168.1277274588137},
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            fileUpload=False,
            fileContrast=False,
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_3",
        position={'x': -873.0587219566071, 'y': 2123.791172048472},
        state=ConfirmReplyState(
            text="不同设备类型正在开发中，敬请期待！",
        )
    )

    # 智能对话节点
    workflow.add_node(
        id="ai_chat_2",
        position={'x': -861.8967916173706, 'y': 187.8637781812438},
        state=AiChatState(
            model="oneapi-siliconflow:deepseek-ai/DeepSeek-R1",
            quotePrompt="",
            isvisible=False,
            temperature=0,
            maxToken=4096,
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_5",
        position={'x': 1050.058092873814, 'y': 114.82823978954264},
        state=ConfirmReplyState(
            isvisible=False,
            text="""SELECT
  SBLX AS "设备类型",
  EQUIP_NAME AS "设备名称",
  SCCJ AS "生产厂家",
  TYRQ AS "投运日期"
FROM nusp_fac_equipment
WHERE xjdw LIKE {{geo}};""",
        )
    )

    # 代码块节点
    workflow.add_node(
        id="code_fragment_1",
        position={'x': -319.49586685447025, 'y': 155.25565264027563},
        state=CodeFragmentState(
            language="python",
            code="""import re

def userFunction(params):
    def extract_after_think(info):
        # 使用正则表达式匹配第一个</think>之后的所有内容
        match = re.search(r'</think>(.*)', info, re.DOTALL)
        if match:
            return match.group(1).strip()  # 返回匹配到的内容并去除首尾空白
        else:
            return info

    result = {}
    try:
        # 提取内容并保存到result中
         temp = extract_after_think(params['input_key'])
         temprp = temp.replace('\\n', '')
         result['output_key'] = "'%" + temprp +"%'"
    except Exception as e:
        # 捕获可能的异常并记录错误信息
        result['error'] = str(e)

    return result""",
            inputs={'input_key': {'key': 'input_key', 'type': 'parameter', 'valueType': 'string', 'description': '', 'connected': True}},
            outputs={'output_key': {'key': 'output_key', 'type': 'parameter', 'valueType': 'string', 'description': '', 'targets': [{'targetHandle': 'geo', 'target': 'memory_var_1'}, {'targetHandle': 'text', 'target': 'confirm_reply_6'}]}},
        )
    )

    # 添加记忆变量节点
    workflow.add_node(
        id="memory_var_1",
        position={'x': 187.41334017570892, 'y': 131.6960333509331},
        state=AddMemoryVariableState(
            variables={'geo': 'string'},
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_6",
        position={'x': 591.6882106464707, 'y': 135.4006165467965},
        state=ConfirmReplyState(
            isvisible=False,
            text="您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
        )
    )

    # 数据库查询节点
    workflow.add_node(
        id="database_query_1",
        position={'x': 2402.86927334456, 'y': 110.86520200031254},
        state=DatabaseQueryState(
            database={},
            showTable=True,
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_7",
        position={'x': 1543.7577279314946, 'y': 156.21737446259584},
        state=ConfirmReplyState(
            text="基本信息如下",
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_8",
        position={'x': 1067.1535700820075, 'y': 890.5267338164495},
        state=ConfirmReplyState(
            isvisible=False,
            text="""SELECT
CONTENT as '故障事件内容',
OCCUR_TIME as '故障发生时间',
BUSI_TYPE_NAME as '故障业务类型名称',
BUSI_TYPE_SUBCLASS as '故障业务子类名称'
FROM
    T_EVENT_ZNJS_DWXXJS t1
WHERE
    t1.EQUIP_ID in (select `EQUIP_ID` from nusp_fac_equipment 
where xjdw like {{geo}});""",
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_9",
        position={'x': 1574.6426907565042, 'y': 892.7600770675024},
        state=ConfirmReplyState(
            text="发生的历史故障如下",
        )
    )

    # 数据库查询节点
    workflow.add_node(
        id="database_query_2",
        position={'x': 2080.157377078698, 'y': 864.3978662788228},
        state=DatabaseQueryState(
            database={},
            showTable=True,
        )
    )

    # 信息分类节点
    info_class_labels = {'9f4da034-1f5c-44d4-9345-1cb53dfcbd61': '查询地区设备清单', '1c8384d9-2910-4ae5-bb36-7b2853be955a': '不同设备'}
    workflow.add_node(
        id="info_class",
        position={'x': -1479.7489037112273, 'y': 151.55533226592678},
        state=InfoClassState(
            historyText=0,
            model="qwen2.5-72b-instruct",
            quotePrompt="""你是电网行业问数智能体的二分类路由器。你的唯一任务：根据用户输入判定应走哪一个流程，并且只输出对应代号。

输出代号（严格二选一，且必须输出其一）：
查询地区设备清单
不同设备：指设备事件/缺陷/跳闸等记录或统计
决策优先级（从高到低，命中即停）：
事件/统计关键词命中 → 不同设备。 事件/统计关键词示例（包含但不限于）：跳闸、缺陷、故障、检修、告警、录波、重合、统计、次数、对比、比较、趋势、最近、近一周/上月/季度、原因、厂家、是否遗留、是否移交综合室、值班人、记录、日志、处理、事故。
清单/罗列关键词命中 → 查询地区设备清单。 清单关键词示例：清单、名单、有哪些、列出、罗列、一览、台账、盘点、汇总、分布、名录、列表。
地名/站名/区域线索命中（即使是冷门或不在词典中）→ 查询地区设备清单。 判定启发式（任一满足即可视为区域线索）：
后缀/词形：片区、区、市、县、旗、州、盟、镇、乡、村、园、园区、街、道、路、巷、岭、山、岛、湾、洲、滩、港、口、桥、湖、河、江、水库、矿、厂 等；
设施/站点：变电站、开闭所、运维站、开关站、枢纽、站、所、#×主变（如“#1主变”常与站点/设备清单相关）；
编码/别称：看似地名或站/所代号的短词/缩写/拼音/字母数字组合（如“GZ-01”“DF变”“临江新城”“洪泽洲”），即使很冷门也按区域线索处理；
含“kV + 站/所”（如“110kV××站”）。
模糊/极短输入的兜底：当未命中1)与2)，且输入很短或语义不明（如仅16个汉字或13个词），一律 → 查询地区设备清单。
若仍无法判断（几乎不可能出现），绝不空输出，强制 → 查询地区设备清单。
特殊歧义处理：
仅出现设备类别或设备名（如“主变”“断路器”“XX线路”）但无事件/统计词且无清单词：默认 → 查询地区设备清单（视为想看该类设备分布/清单）。
同时出现清单词与事件词时：以事件词优先 → 不同设备。
输出规范（务必遵守）：
严格只选择 查询地区设备清单 或 不同设备 之一。
不输出任何其他字符、标点、空格、换行、前后缀或解释。""",
            labels=info_class_labels,
        )
    )

    # 确定回复节点
    workflow.add_node(
        id="confirm_reply_10",
        position={'x': 1954.5790409016909, 'y': 156.83070120629836},
        state=ConfirmReplyState(
            isvisible=False,
            text="""SELECT
  SBLX AS "设备类型",
  EQUIP_NAME AS "设备名称",
  SCCJ AS "生产厂家",
  TYRQ AS "投运日期"
FROM nusp_fac_equipment
WHERE xjdw LIKE '%慈溪%';""",
        )
    )

    # 添加连接边
    workflow.add_edge("ai_chat_2", "code_fragment_1", "finish", "switchAny")
    workflow.add_edge("code_fragment_1", "memory_var_1", "output_key", "geo")
    workflow.add_edge("code_fragment_1", "confirm_reply_6", "finish", "switchAny")
    workflow.add_edge("code_fragment_1", "confirm_reply_6", "output_key", "text")
    workflow.add_edge("confirm_reply_6", "confirm_reply_5", "finish", "switchAny")
    workflow.add_edge("confirm_reply_5", "confirm_reply_7", "finish", "switchAny")
    workflow.add_edge("database_query_1", "confirm_reply_8", "finish", "switchAny")
    workflow.add_edge("confirm_reply_8", "confirm_reply_9", "finish", "switchAny")
    workflow.add_edge("confirm_reply_9", "database_query_2", "finish", "switchAny")
    workflow.add_edge("confirm_reply_8", "database_query_2", "text", "sql")
    workflow.add_edge("info_class", "ai_chat_2", list(info_class_labels.keys())[0], "switchAny")
    workflow.add_edge(START, "info_class", "userChatInput", "text")
    workflow.add_edge(START, "ai_chat_2", "userChatInput", "text")
    workflow.add_edge("info_class", "confirm_reply_3", list(info_class_labels.keys())[1], "switchAny")
    workflow.add_edge(START, "info_class", "finish", "switchAny")
    workflow.add_edge("confirm_reply_7", "confirm_reply_10", "finish", "switchAny")
    workflow.add_edge("confirm_reply_5", "database_query_1", "text", "sql")
    workflow.add_edge("confirm_reply_10", "database_query_1", "finish", "switchAny")
    workflow.add_edge("ai_chat_2", "code_fragment_1", "answerText", "input_key")

    # 编译
    workflow.compile(
        name="从json导出的工作流",
        intro="",
        category="自动生成",
        prologue="您好！我是从json导出的工作流"
    )

if __name__ == "__main__":
    main()