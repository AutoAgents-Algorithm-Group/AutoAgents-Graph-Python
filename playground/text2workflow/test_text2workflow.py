import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph import Text2Agent
from src.autoagents_graph.dify import DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState, DifyEndState, START, END


def main():
    # 创建智能问答助手
    workflow = Text2Agent(
        platform="dify",
        app_name="智能问答助手",
        app_description="基于知识库的智能问答系统"
    )

    # 添加节点
    workflow.add_node(
        id=START,
        position={"x": 50, "y": 200},
        state=DifyStartState(
            title="开始",
            variables=[]
        ),
    )

    workflow.add_node(
        id="knowledge_search",
        position={"x": 300, "y": 200},
        state=DifyKnowledgeRetrievalState(
            title="知识检索",
            dataset_ids=["knowledge_base"],
            multiple_retrieval_config={
                "reranking_enable": True,
                "top_k": 5
            }
        ),
    )

    workflow.add_node(
        id="ai_answer",
        state=DifyLLMState(
            title="智能回答",
            model={
                "completion_params": {"temperature": 0.3},
                "mode": "chat",
                "name": "doubao-deepseek-v3",
                "provider": ""
            },
            prompt_template=[{
                "role": "system", 
                "text": """基于检索到的知识内容，为用户提供准确、详细的回答。

知识内容：{{@knowledge_search_text}}
用户问题：{{@start_userChatInput}}

请根据知识内容回答用户问题，如果知识内容无法回答问题，请如实告知。"""
            }]
        ),
        position={"x": 550, "y": 200},
    )

    workflow.add_node(
        id=END,
        position={"x": 800, "y": 200},
        state=DifyEndState(
            title="结束",
            outputs=[]
        ),
    )

    # 添加连接边
    workflow.add_edge(START, "knowledge_search")
    workflow.add_edge("knowledge_search", "ai_answer")
    workflow.add_edge("ai_answer", END)

    # 编译工作流
    workflow.compile()
    workflow.save("playground/text2workflow/dify_workflow_output.yaml")


if __name__ == "__main__":
    main()