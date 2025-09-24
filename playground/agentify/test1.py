from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models import QuestionInputState, Pdf2MdState, KnowledgeSearchState, AiChatState, ConfirmReplyState


def main():
    graph = FlowGraph(
        personal_auth_key="1558352c152b484ead33187a3a0ab035",
        personal_auth_secret="ZBlCbwYjcoBYmJTPGKiUgXM2XRUvf3s1",
        base_url="https://test.agentspro.cn"
    )

    # 用户输入节点（支持文本和文档上传）
    graph.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=True,
            uploadPicture=False,
            fileUpload=True,
            initialInput=True
        )
    )

    # 文档解析节点
    graph.add_node(
        id="doc_parser",
        state=Pdf2MdState(
            pdf2mdType="deep_pdf2md"
        )
    )

    # 知识库搜索节点
    graph.add_node(
        id="kb_search",
        state=KnowledgeSearchState(
            datasets=["shortplay_kb"],
            similarity=0.25,
            topK=15
        )
    )

    # AI剧本生成节点
    graph.add_node(
        id="script_generator",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是一位专业编剧助理，根据以下要素生成微短剧剧本：
1. 用户需求：{user_input}
2. 参考文档：{doc_content}
3. 相关知识：{kb_content}

要求：
- 包含完整的三幕结构
- 每个场景标注镜头语言
- 包含主要角色对话
- 保持节奏紧凑""",
            temperature=0.3,
            maxToken=3000,
            stream=True
        )
    )

    # 结果确认节点
    graph.add_node(
        id="final_output",
        state=ConfirmReplyState(
            stream=True
        )
    )

    # 连接工作流
    graph.add_edge(START, "doc_parser", "files", "files")
    graph.add_edge(START, "kb_search", "userChatInput", "text")
    graph.add_edge("doc_parser", "kb_search", "pdf2mdResult", "text")
    graph.add_edge(START, "script_generator", "userChatInput", "text")
    graph.add_edge("doc_parser", "script_generator", "pdf2mdResult", "text")
    graph.add_edge("kb_search", "script_generator", "quoteQA", "knSearch")
    graph.add_edge("script_generator", "final_output", "answerText", "text")

    # 错误处理分支
    graph.add_node(
        id="error_handler",
        state=ConfirmReplyState(
            text="剧本生成失败，请检查输入格式或重新上传参考文档",
            stream=True
        )
    )
    graph.add_edge("doc_parser", "error_handler", "failed", "switchAny")
    graph.add_edge("kb_search", "error_handler", "isEmpty", "switchAny")

    # 编译智能体
    graph.compile(
        name="微短剧剧本生成器",
        intro="专业生成符合短视频平台要求的微短剧剧本",
        category="内容创作",
        prologue="欢迎使用剧本生成助手！请描述您的剧本需求并上传参考文档（可选）"
    )


if __name__ == "__main__":
    main()