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
    # 添加questionInput节点
    graph.add_node(
        id="simpleInputId",
        position={'x': -443.54089012517386, 'y': 512.8525730180806},
        state=QuestionInputState
    )

    # 添加aiChat节点
    graph.add_node(
        id="simpleAichatId",
        position={'x': 685, 'y': 364},
        state=AiChatState
    )

    # 添加confirmreply节点
    graph.add_node(
        id="confirm_reply",
        position={'x': 176.76119610570254, 'y': 550.6982614742699},
        state=ConfirmReplyState
    )

    # 添加confirmreply节点
    graph.add_node(
        id="confirm_reply_1",
        position={'x': 1303.5857213907286, 'y': 915.5886004018828},
        state=ConfirmReplyState
    )

    # 添加连接边
    graph.add_edge("confirm_reply", "simpleAichatId", "finish", "switch")
    graph.add_edge("simpleInputId", "confirm_reply", "finish", "switch")
    graph.add_edge("simpleInputId", "simpleAichatId", "userChatInput", "text")
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