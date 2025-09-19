import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


from src.autoagents_graph import Text2Workflow
from src.autoagents_graph.dify import DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState, DifyEndState, START, END


def main():
    # 创建Dify平台工作流
    workflow = Text2Workflow(
        platform="dify",
        app_name="Dify测试工作流",
        app_description="基于Text2Workflow构建的Dify工作流"
    )

    # 添加开始节点
    workflow.add_node(
        id=START,
        position={"x": 50, "y": 200},
        state=DifyStartState(title="开始"),
    )

    # 添加LLM节点
    workflow.add_node(
        id="llm_analysis",
        state=DifyLLMState(
            title="智能分析",
            prompt_template=[{"role": "system", "text": "你是一个专业的AI助手，请分析用户的问题。"}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "doubao-deepseek-v3",
                "provider": ""
            }
        ),
        position={"x": 300, "y": 200}
    )

    # 添加知识检索节点
    workflow.add_node(
        id="knowledge",
        state=DifyKnowledgeRetrievalState(
            dataset_ids=["knowledge_base"],
            multiple_retrieval_config={"top_k": 5, "reranking_enable": True}
        ),
        position={"x": 550, "y": 200}
    )

    # 添加AI回复节点
    workflow.add_node(
        id="ai_reply",
        state=DifyLLMState(
            title="智能回复",
            prompt_template=[{"role": "system", "text": "基于检索结果，为用户提供详细回答。"}],
            model={
                "completion_params": {"temperature": 0.8},
                "mode": "chat",
                "name": "doubao-deepseek-v3",
                "provider": ""
            }
        ),
        position={"x": 800, "y": 200}
    )

    # 添加结束节点
    workflow.add_node(
        id=END,
        state=DifyEndState(title="处理完成"),
        position={"x": 1050, "y": 200}
    )

    # 添加连接边
    workflow.add_edge(START, "llm_analysis")
    workflow.add_edge("llm_analysis", "knowledge")
    workflow.add_edge("knowledge", "ai_reply")
    workflow.add_edge("ai_reply", END)

    # 编译并保存
    yaml_result = workflow.compile()
    workflow.save("playground/dify/dify_workflow_output.yaml")
    
    print(f"Dify工作流测试完成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()