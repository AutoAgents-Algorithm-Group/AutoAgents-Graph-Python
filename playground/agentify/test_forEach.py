import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph import NL2Workflow
from src.autoagents_graph.engine.agentify import START
from src.autoagents_graph.engine.agentify.models import QuestionInputState, ForEachState, ConfirmReplyState


def main():
    # 初始化工作流
    workflow = NL2Workflow(
        platform="agentify",
        personal_auth_key="833c6771a8ae4ee88e6f4d5f7f2a62e5",
        personal_auth_secret="XceT7Cf86SfX2LNhl5I0QuOYomt1NvqZ",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    workflow.add_node(
        id=START,
        state=QuestionInputState()
    )

    workflow.add_node(
        id="forEach1",
        state=ForEachState()
    )

    workflow.add_node(
        id="confirmreply1",
        state=ConfirmReplyState(
            stream=True,
            text="1"
        )
    )

    # 添加连接边
    workflow.add_edge(START, "forEach1", "userChatInput", "items")
    workflow.add_edge(START, "forEach1", "finish", "switchAny")

    workflow.add_edge("forEach1", "confirmreply1", "loopStart", "switchAny")
    
    workflow.add_edge("confirmreply1", "forEach1", "finish", "loopEnd")

    # 编译工作流
    workflow.compile(
        name="循环执行",
        intro="这是一个专业的循环执行系统",
        category="循环执行",
        prologue="你好！我是你的循环执行系统。"
    )


if __name__ == "__main__":
    main()