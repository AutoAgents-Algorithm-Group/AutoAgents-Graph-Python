from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models import (
    QuestionInputState,
    AiChatState,
    ForEachState,
    ConfirmReplyState,
    AddMemoryVariableState
)

def main():
    graph = FlowGraph(
        personal_auth_key="your_auth_key",
        personal_auth_secret="your_auth_secret",
        base_url="https://test.agentspro.cn"
    )

    # 用户输入节点
    graph.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            initialInput=True
        )
    )

    # 小说大纲生成AI
    graph.add_node(
        id="outline_gen",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是一个专业小说家，请根据用户提供的类型、角色和核心情节生成小说大纲。
包含5个章节标题和简要内容概述，用Markdown格式列出。""",
            temperature=0.7,
            stream=True
        )
    )

    # 保存大纲的记忆变量
    graph.add_node(
        id="save_outline",
        state=AddMemoryVariableState()
    )

    # 章节内容循环处理
    graph.add_node(
        id="chapter_loop",
        state=ForEachState()
    )

    # 章节内容生成AI
    graph.add_node(
        id="chapter_gen",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="根据小说大纲和当前章节标题，生成2000字详细内容，保持语言生动。",
            temperature=0.8,
            stream=True
        )
    )

    # 最终结果汇总
    graph.add_node(
        id="final_output",
        state=ConfirmReplyState(
            text="小说生成完成！以下是完整内容：\n",
            stream=True
        )
    )

    # 连接流程
    graph.add_edge(START, "outline_gen", "userChatInput", "text")
    graph.add_edge("outline_gen", "save_outline", "answerText", "feedback")

    graph.add_edge("save_outline", "chapter_loop", "finish", "switchAny")
    graph.add_edge("outline_gen", "chapter_loop", "answerText", "items")

    graph.add_edge("chapter_loop", "chapter_gen", "loopStart", "switchAny")
    graph.add_edge("chapter_gen", "chapter_loop", "finish", "loopEnd")

    graph.add_edge("chapter_loop", "final_output", "finish", "switchAny")
    graph.add_edge("chapter_gen", "final_output", "answerText", "text")

    graph.compile(
        name="智能小说生成系统",
        intro="根据用户输入自动生成完整小说内容",
        category="内容创作",
        prologue="请输入小说类型、主要角色和核心情节，我将为您生成完整小说。"
    )

if __name__ == "__main__":
    main()
