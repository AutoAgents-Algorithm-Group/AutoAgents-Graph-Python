from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models.GraphTypes import (
    QuestionInputState, AiChatState, ConfirmReplyState,
    KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState,
    InfoClassState, CodeFragmentState, ForEachState, HttpInvokeState
)

def main():
    graph = FlowGraph(
            personal_auth_key="7217394b7d3e4becab017447adeac239",
            personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
            base_url="https://uat.agentspro.cn"
        )

    # 添加节点
    # 添加questionInput节点
    graph.add_node(
        id="simpleInputId",
        position={'x': 0, 'y': 300},
        state=QuestionInputState
    )

    # 添加pdf2md节点
    graph.add_node(
        id="doc_parser",
        position={'x': 497.2741652021091, 'y': 340.8875219683656},
        state=Pdf2MdState
    )

    # 添加knowledgesSearch节点
    graph.add_node(
        id="kb_search",
        position={'x': 1000, 'y': 300},
        state=KnowledgeSearchState
    )

    # 添加aiChat节点
    graph.add_node(
        id="ai_chat",
        position={'x': 1505.4516695957818, 'y': 294.54833040421795},
        state=AiChatState
    )

    # 添加confirmreply节点
    graph.add_node(
        id="confirm_reply",
        position={'x': 2002.7258347978911, 'y': 291.8224956063269},
        state=ConfirmReplyState
    )

    # 添加addMemoryVariable节点
    graph.add_node(
        id="save_memory",
        position={'x': 2500, 'y': 300},
        state=AddMemoryVariableState
    )

    # 添加连接边
    graph.add_edge("simpleInputId", "doc_parser", "finish", "switchAny")
    graph.add_edge("simpleInputId", "doc_parser", "files", "files")
    graph.add_edge("simpleInputId", "kb_search", "userChatInput", "text")
    graph.add_edge("doc_parser", "ai_chat", "pdf2mdResult", "text")
    graph.add_edge("kb_search", "ai_chat", "quoteQA", "knSearch")
    graph.add_edge("ai_chat", "confirm_reply", "finish", "switchAny")
    graph.add_edge("ai_chat", "confirm_reply", "answerText", "text")
    graph.add_edge("confirm_reply", "save_memory", "finish", "")
    graph.add_edge("ai_chat", "save_memory", "answerText", "feedback")

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