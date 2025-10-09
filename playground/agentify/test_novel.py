import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph import NL2Workflow, AgentifyConfig
from src.autoagents_graph.engine.agentify import START
from src.autoagents_graph.engine.agentify.models import QuestionInputState, KnowledgeSearchState, AiChatState, ConfirmReplyState, ForEachState,AddMemoryVariableState


def main():
    workflow = NL2Workflow(
        platform="agentify",
        config=AgentifyConfig(
            personal_auth_key="7217394b7d3e4becab017447adeac239",
            personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
            base_url="https://uat.agentspro.cn"
        )
    )

    # 用户输入节点
    workflow.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            initialInput=True
        )
    )

    # 小说大纲生成AI
    workflow.add_node(
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
    workflow.add_node(
        id="save_outline",
        state=AddMemoryVariableState()
    )

    # 章节内容循环处理
    workflow.add_node(
        id="chapter_loop",
        state=ForEachState()
    )

    # 章节内容生成AI
    workflow.add_node(
        id="chapter_gen",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="根据小说大纲和当前章节标题，生成2000字详细内容，保持语言生动。",
            temperature=0.8,
            stream=True
        )
    )

    # 最终结果汇总
    workflow.add_node(
        id="final_output",
        state=ConfirmReplyState(
            text="小说生成完成！以下是完整内容：\n",
            stream=True
        )
    )

    # 连接流程
    workflow.add_edge(START, "outline_gen", "userChatInput", "text")
    workflow.add_edge("outline_gen", "save_outline", "answerText", "feedback")

    workflow.add_edge("save_outline", "chapter_loop", "finish", "switchAny")
    workflow.add_edge("outline_gen", "chapter_loop", "answerText", "items")

    workflow.add_edge("chapter_loop", "chapter_gen", "loopStart", "switchAny")
    workflow.add_edge("chapter_gen", "chapter_loop", "finish", "loopEnd")

    workflow.add_edge("chapter_loop", "final_output", "finish", "switchAny")
    workflow.add_edge("chapter_gen", "final_output", "answerText", "text")

    workflow.compile(
        name="智能小说生成系统",
        intro="根据用户输入自动生成完整小说内容",
        category="内容创作",
        prologue="请输入小说类型、主要角色和核心情节，我将为您生成完整小说。"
    )

if __name__ == "__main__":
    main()
