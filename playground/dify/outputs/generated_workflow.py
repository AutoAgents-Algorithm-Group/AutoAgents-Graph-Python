import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.autoagents_graph import NL2Workflow, DifyConfig
from src.autoagents_graph.engine.dify import (
    DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState,
    DifyEndState, START, END
)


def main():
    # 创建Dify工作流
    workflow = NL2Workflow(
        platform="dify",
        config=DifyConfig(
            app_name="从Dify导出的工作流",
            app_description="通过DifyParser自动生成",
            app_icon="🤖",
            app_icon_background="#FFEAD5"
        )
    )

    # 添加节点
    # 添加开始节点
    workflow.add_node(
        id=START,
        position={'x': 50.0, 'y': 200.0},
        state=DifyStartState(
            title="开始",
            variables=[{'label': '系统输入', 'max_length': 48000, 'options': [], 'required': True, 'type': 'text-input', 'variable': 'sys_input'}],
        )
    )

    # 添加AI处理节点
    workflow.add_node(
        id="ai",
        position={'x': 300.0, 'y': 200.0},
        state=DifyLLMState(
            title="AI处理",
            model={'completion_params': {'temperature': 0.8}, 'mode': 'chat', 'name': 'gpt-4', 'provider': 'openai'},
            prompt_template=[{'role': 'system', 'text': '你是一个智能助手'}],
            context={'enabled': False, 'variable_selector': []},
            variables=[],
        )
    )

    # 添加结束节点
    workflow.add_node(
        id=END,
        position={'x': 550.0, 'y': 200.0},
        state=DifyEndState(
            title="结束",
            outputs=[],
        )
    )

    # 添加连接边
    workflow.add_edge(START, "ai")
    workflow.add_edge("ai", END)

    # 编译并保存
    yaml_result = workflow.compile()
    workflow.save("playground/dify/outputs/dify_workflow_output.yaml")
    print(f"工作流已生成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()