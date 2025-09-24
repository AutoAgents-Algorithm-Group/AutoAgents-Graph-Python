from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models.GraphTypes import (
    QuestionInputState, AiChatState, ConfirmReplyState,
    KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,
    InfoClassState, CodeFragmentState, ForEachState, HttpInvokeState
)

def main():
    graph = FlowGraph(
            personal_auth_key="1558352c152b484ead33187a3a0ab035",
            personal_auth_secret="ZBlCbwYjcoBYmJTPGKiUgXM2XRUvf3s1",
            base_url="https://test.agentspro.cn"
        )

    # 添加节点
    # 创建questionInput状态对象
    simpleInputId_state = QuestionInputState(
        inputText=True,
        uploadFile=False,
        uploadPicture=False,
        fileUpload=False,
        fileContrast=False,
        initialInput=True,
        fileInfo=[],
    )

    graph.add_node(
        id="simpleInputId",
        position={'x': -360.36620305980534, 'y': 478.60417246175246},
        state=simpleInputId_state
    )

    # 创建aiChat状态对象
    simpleAichatId_state = AiChatState(
        text="",
        images=[],
        knSearch="",
        historyText=3,
        model="gpt-4",
        quotePrompt="",
        temperature=0,
        maxToken=3000,
        isvisible=True,
    )

    graph.add_node(
        id="simpleAichatId",
        position={'x': 616.5031988873434, 'y': 334.64422809457585},
        state=simpleAichatId_state
    )

    # 创建confirmreply状态对象
    confirm_reply_state = ConfirmReplyState(
        text="您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
        isvisible=True,
    )

    graph.add_node(
        id="confirm_reply",
        position={'x': 103.37176634214188, 'y': 469.9698887343536},
        state=confirm_reply_state
    )

    # 创建databaseQuery状态对象
    kb_search_state = KnowledgeSearchState(
    )

    graph.add_node(
        id="kb_search",
        position={'x': 1483.3988351877615, 'y': 359.88574408901263},
        state=kb_search_state
    )

    # 创建confirmreply状态对象
    confirm_reply_1_state = ConfirmReplyState(
        text="您可以输入希望用户看到的内容，当触发条件判定成立，将显示您输入的内容。",
        isvisible=True,
    )

    graph.add_node(
        id="confirm_reply_1",
        position={'x': 1123.4848400556325, 'y': 924.9843532684284},
        state=confirm_reply_1_state
    )

    # 添加连接边
    graph.add_edge("simpleInputId", "confirm_reply", "userChatInput", "text")
    graph.add_edge("confirm_reply", "simpleAichatId", "text", "text")
    graph.add_edge("confirm_reply", "simpleAichatId", "finish", "switch")
    graph.add_edge("simpleAichatId", "confirm_reply_1", "answerText", "text")
    graph.add_edge("simpleAichatId", "confirm_reply_1", "finish", "switch")

    # 编译, 导入配置，点击确定
    graph.compile(
            name="从JSON生成的工作流",
            intro="这是从JSON数据反向生成的工作流",
            category="自动生成",
            prologue="你好！这是自动生成的工作流。",
            shareAble=True,
            allowVoiceInput=False,
            autoSendVoice=False
        )

if __name__ == "__main__":
    main()