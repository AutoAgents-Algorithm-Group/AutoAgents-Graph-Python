import os
import sys
import uuid

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.Text2Workflow import Text2Workflow
# 只使用DifyTypes，不再混用agentify.types
from src.dify import DifyStartState, DifyLLMState, DifyEndState, START, END


def main():
    # 生成唯一ID
    llm_node_1_id = str(uuid.uuid4())  # 苹果吃法id
    llm_node_2_id = str(uuid.uuid4())  # 苹果特点
    llm_node_3_id = str(uuid.uuid4())  # 苹果坏处
    llm_summary_id = str(uuid.uuid4())  # 总结苹果

    # 创建Dify平台工作流
    workflow = Text2Workflow(
        platform="dify",
        app_name="苹果的介绍-代码生成",
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
        id=llm_node_1_id,
        state=DifyLLMState(
            title="苹果吃法",
            prompt_template=[{"role": "system", "text": "说一下苹果的吃法，100字左右。"}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4",
                "provider": ""
            }
        ),
        position={"x": 276, "y": 263}
    )

    # 添加LLM节点
    workflow.add_node(
        id=llm_node_2_id,
        state=DifyLLMState(
            title="苹果特点",
            prompt_template=[{"role": "system", "text": "说一下苹果的特点，100字左右。"}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4",
                "provider": ""
            }
        ),
        position={"x": 276, "y": 82}
    )

    # 添加LLM节点
    workflow.add_node(
        id=llm_node_3_id,
        state=DifyLLMState(
            title="苹果坏处",
            prompt_template=[{"role": "system", "text": "说一下苹果的坏处，100字左右。"}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4",
                "provider": ""
            }
        ),
        position={"x": 276, "y": 459}
    )

    # 添加LLM总结节点
    workflow.add_node(
        id=llm_summary_id,
        state=DifyLLMState(
            title="总结苹果",
            prompt_template=[{"role": "system", "text": f"""
            合并总结上游LLM输出内容，最后进行输出。最多200字。
            LLM_Output_1：{{#{llm_node_1_id}.text#}}

            LLM_Output_2：{{#{llm_node_2_id}.text#}}

            LLM_Output_3：{{#{llm_node_3_id}.text#}}
            """}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4o",
                "provider": "langgenius/openai/openai"
            },
            structured_output={
                "schema": {
                    "additionalProperties": False,
                    "properties": {
                        "output": {
                            "type": "string",
                            "description": "总结结果的输出"
                        }
                    },
                    "required": ["output"],
                    "type": "object"
                }
            },
            structured_output_enabled=True
        ),
        position={"x": 572, "y": 254}
    )

    # 添加结束节点
    workflow.add_node(
        id=END,
        state=DifyEndState(title="处理完成"),
        position={"x": 852, "y": 254}
    )

    # 添加连接边
    workflow.add_edge(START, llm_node_1_id)
    workflow.add_edge(START, llm_node_2_id)
    workflow.add_edge(START, llm_node_3_id)
    workflow.add_edge(llm_node_1_id, llm_summary_id)
    workflow.add_edge(llm_node_2_id, llm_summary_id)
    workflow.add_edge(llm_node_3_id, llm_summary_id)
    workflow.add_edge(llm_summary_id, END)

    # 编译并保存
    yaml_result = workflow.compile()
    workflow.save("playground/dify/dify_workflow_output-Parallel.yaml")

    print(f"Dify工作流测试完成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()