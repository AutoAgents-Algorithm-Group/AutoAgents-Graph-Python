from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState, Pdf2MdState, AddMemoryVariableState

def main():
    graph = FlowGraph(
        personal_auth_key="7217394b7d3e4becab017447adeac239",
        personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 用户提问节点
    graph.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=True
        )
    )

    # 文档解析节点
    graph.add_node(
        id="doc_parser",
        state=Pdf2MdState()
    )

    # 知识库搜索节点
    graph.add_node(
        id="kb_search",
        state=KnowledgeSearchState(
            datasets=["kb_001"],
            similarity=0.3,
            topK=5
        )
    )

    # AI对话节点
    graph.add_node(
        id="ai_chat",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="你是一个专业的问答助手，请根据知识库内容回答用户问题",
            temperature=0.2,
            stream=True
        )
    )

    # 确认回复节点
    graph.add_node(
        id="confirm_reply",
        state=ConfirmReplyState(
            stream=True
        )
    )

    # 记忆变量节点
    graph.add_node(
        id="save_memory",
        state=AddMemoryVariableState()
    )

    # 连接边
    graph.add_edge(START, "doc_parser", "finish", "switchAny")
    graph.add_edge(START, "doc_parser", "files", "files")
    
    graph.add_edge(START, "kb_search", "userChatInput", "text")
    
    graph.add_edge("doc_parser", "ai_chat", "pdf2mdResult", "text")
    graph.add_edge("kb_search", "ai_chat", "quoteQA", "knSearch")
    
    graph.add_edge("ai_chat", "confirm_reply", "finish", "switchAny")
    graph.add_edge("ai_chat", "confirm_reply", "answerText", "text")
    
    graph.add_edge("confirm_reply", "save_memory", "finish", "switchAny")
    graph.add_edge("ai_chat", "save_memory", "answerText", "feedback")

    # 编译
    graph.compile(
        name="知识库问答助手",
        intro="基于知识库的智能问答系统",
        category="问答助手",
        prologue="您好！我是知识库问答助手，请提出您的问题。"
    )

if __name__ == "__main__":
    main()