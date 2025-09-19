import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uuid

from src.autoagents_graph import Text2Workflow
from src.autoagents_graph.dify import DifyStartState, DifyLLMState, DifyEndState, START, END


def main():
    # 生成唯一ID
    llm_node_1_id = str(uuid.uuid4())  # GenerateCoT-1
    llm_node_2_id = str(uuid.uuid4())  # GenerateCoT-2  
    llm_node_3_id = str(uuid.uuid4())  # GenerateCoT-3
    llm_summary_id = str(uuid.uuid4())  # ScEnsemble集成

    # 创建Dify平台工作流
    workflow = Text2Workflow(
        platform="dify",
        app_name="Multi-CoT Ensemble工作流",
        app_description="基于aflow框架的多轮思维链集成工作流"
    )

    # 添加开始节点
    workflow.add_node(
        id=START,
        position={"x": 0, "y": 200},
        state=DifyStartState(title="开始"),
    )

    # 添加LLM节点 - GenerateCoT
    workflow.add_node(
        id=llm_node_1_id,
        state=DifyLLMState(
            title="GenerateCoT-1",
            prompt_template=[{"role": "system", "text": """使用思维链推理方法分析问题，逐步推理并给出结论。

用户输入：{{#start.sys_input#}}

请进行详细的思维链推理分析。"""}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4",
                "provider": ""
            }
        ),
        position={"x": 276, "y": 263}
    )

    # 添加LLM节点 - GenerateCoT
    workflow.add_node(
        id=llm_node_2_id,
        state=DifyLLMState(
            title="GenerateCoT-2",
            prompt_template=[{"role": "system", "text": """使用思维链推理方法分析问题，逐步推理并给出结论。

用户输入：{{#start.sys_input#}}

请进行详细的思维链推理分析。"""}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4",
                "provider": ""
            }
        ),
        position={"x": 276, "y": 82}
    )

    # 添加LLM节点 - GenerateCoT
    workflow.add_node(
        id=llm_node_3_id,
        state=DifyLLMState(
            title="GenerateCoT-3",
            prompt_template=[{"role": "system", "text": """使用思维链推理方法分析问题，逐步推理并给出结论。

用户输入：{{#start.sys_input#}}

请进行详细的思维链推理分析。"""}],
            model={
                "completion_params": {"temperature": 0.7},
                "mode": "chat",
                "name": "gpt-4",
                "provider": ""
            }
        ),
        position={"x": 276, "y": 459}
    )

    # 添加ScEnsemble集成节点
    workflow.add_node(
        id=llm_summary_id,
        state=DifyLLMState(
            title="ScEnsemble",
            prompt_template=[{"role": "system", "text": f"""
            使用Self-Consistency Ensemble方法，对多个思维链推理结果进行集成分析，选择最一致和可靠的答案。
            
            原始问题：{{{{#start.sys_input#}}}}
            
            方案A：{{{{#{llm_node_1_id}.text#}}}}
            
            方案B：{{{{#{llm_node_2_id}.text#}}}}
            
            方案C：{{{{#{llm_node_3_id}.text#}}}}
            
            请分析这三个方案的一致性，并选择最可靠的答案或进行合理的集成。
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
                        "selected_solution": {
                            "type": "string",
                            "description": "选择的最佳方案标识(A/B/C)"
                        },
                        "reasoning": {
                            "type": "string", 
                            "description": "选择该方案的推理过程"
                        },
                        "final_answer": {
                            "type": "string",
                            "description": "最终集成后的答案"
                        }
                    },
                    "required": ["selected_solution", "reasoning", "final_answer"],
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

    print(f"Multi-CoT Ensemble工作流生成完成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()