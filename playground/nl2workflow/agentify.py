import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph import NL2Workflow
from src.autoagents_graph.engine.agentify import START
from src.autoagents_graph.engine.agentify.models import (
    QuestionInputState, 
    AiChatState, 
    ConfirmReplyState,
    KnowledgeSearchState,
    AddMemoryVariableState
)


def main():
    # 创建知识库问答助手
    workflow = NL2Workflow(
        platform="agentify",
        personal_auth_key="7217394b7d3e4becab017447adeac239",
        personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    # 1. 用户提问节点
    workflow.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            initialInput=True
        )
    )

    # 2. 知识库搜索节点
    workflow.add_node(
        id="knowledge_search",
        state=KnowledgeSearchState(
            datasets=["kb_001"],  # 知识库ID
            similarity=0.2,
            topK=20,
            enableRerank=False
        )
    )

    # 3. 确认回复节点（显示知识库搜索状态）
    workflow.add_node(
        id="search_status",
        state=ConfirmReplyState(
            text="正在为您检索相关知识...",
            isvisible=True
        )
    )

    # 4. AI回答节点
    workflow.add_node(
        id="ai_answer",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""<角色>
你是一个智能问答助手，基于检索到的知识库内容为用户提供准确的回答。
</角色>

<知识库内容>
{{@knowledge_search_quoteQA}}
</知识库内容>

<用户问题>
{{@question1_userChatInput}}
</用户问题>

<要求>
1. 根据知识库内容准确回答用户问题
2. 如果知识库中没有相关信息，请如实告知
3. 回答要简洁明了，重点突出
</要求>""",
            temperature=0.3,
            maxToken=3000,
            isvisible=True,
            historyText=3
        )
    )

    # 5. 记忆变量节点（保存对话内容）
    workflow.add_node(
        id="memory_save",
        state=AddMemoryVariableState(
            variables={
                "question1_userChatInput": "string",
                "knowledge_search_quoteQA": "search",
                "ai_answer_answerText": "string"
            }
        )
    )

    # 添加连接边
    # 用户提问 -> 知识库搜索
    workflow.add_edge(START, "knowledge_search", "finish", "switchAny")
    workflow.add_edge(START, "knowledge_search", "userChatInput", "text")
    
    # 知识库搜索 -> 确认回复
    workflow.add_edge("knowledge_search", "search_status", "unEmpty", "switchAny")
    
    # 确认回复 -> AI回答
    workflow.add_edge("search_status", "ai_answer", "finish", "switchAny")
    workflow.add_edge(START, "ai_answer", "userChatInput", "text")
    workflow.add_edge("knowledge_search", "ai_answer", "quoteQA", "knSearch")
    
    # AI回答 -> 记忆变量
    workflow.add_edge(START, "memory_save", "userChatInput", "question1_userChatInput")
    workflow.add_edge("knowledge_search", "memory_save", "quoteQA", "knowledge_search_quoteQA")
    workflow.add_edge("ai_answer", "memory_save", "answerText", "ai_answer_answerText")

    # 编译工作流
    workflow.compile(
        name="知识库问答助手",
        intro="基于知识库的智能问答系统，支持知识检索和AI回答",
        category="智能助手",
        prologue="你好！我是知识库问答助手，请问有什么可以帮助您的？"
    )


if __name__ == "__main__":
    main()

