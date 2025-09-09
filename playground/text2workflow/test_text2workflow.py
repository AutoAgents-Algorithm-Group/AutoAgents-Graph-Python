import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.Text2Workflow import Text2Workflow
from src.agentify.types import QuestionInputState, AiChatState, ConfirmReplyState
from src.dify import DifyStartNodeData, DifyLLMNodeData, DifyEndNodeData


def main():
    # Dify平台测试
    workflow = Text2Workflow(
        platform="dify",
        app_name="简单测试助手"
    )

    workflow.add_node("start", DifyStartNodeData(title="开始"), {"x": 50, "y": 200})
    workflow.add_node("ai", AiChatState(model="doubao-deepseek-v3", text="你好！"), {"x": 300, "y": 200})
    workflow.add_node("end", DifyEndNodeData(title="结束"), {"x": 550, "y": 200})

    workflow.add_edge("start", "ai")
    workflow.add_edge("ai", "end")

    yaml_output = workflow.compile()
    workflow.save("test_dify_output.yaml")
    print(f"Dify测试完成，YAML长度: {len(yaml_output)}")

    # Agentify平台测试  
    workflow2 = Text2Workflow(
        platform="agentify",
        personal_auth_key="test_key",
        personal_auth_secret="test_secret"
    )

    workflow2.add_node("input", QuestionInputState(inputText=True), {"x": 50, "y": 200})
    workflow2.add_node("ai", AiChatState(model="doubao-deepseek-v3", text="请问有什么可以帮助您的？"), {"x": 300, "y": 200})
    workflow2.add_node("reply", ConfirmReplyState(text="感谢使用！"), {"x": 550, "y": 200})

    workflow2.add_edge("input", "ai", "finish", "switchAny")
    workflow2.add_edge("ai", "reply", "finish", "switchAny")

    workflow2.save("test_agentify_output.json")
    print("Agentify测试完成")


if __name__ == "__main__":
    main()
