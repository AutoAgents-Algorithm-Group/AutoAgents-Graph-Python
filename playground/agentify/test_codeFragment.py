import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uuid

from src.autoagents_graph.agentify import FlowGraph, START
from src.autoagents_graph.agentify.types import QuestionInputState, CodeFragmentState, ConfirmReplyState


def main():
    # 初始化工作流
    graph = FlowGraph(
        personal_auth_key="833c6771a8ae4ee88e6f4d5f7f2a62e5",
        personal_auth_secret="XceT7Cf86SfX2LNhl5I0QuOYomt1NvqZ",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    graph.add_node(
        id=START,
        state=QuestionInputState()
    )

    # 定义输入输出标签
    input_labels = [
        {
            str(uuid.uuid1()): {
                "label": "input啊",
                "valueType": "string"
            }
        }
    ]
    output_labels = [
        {
            str(uuid.uuid1()): {
                "label": "output啊",
                "valueType": "string"
            }
        }
    ]
    input_label_keys = [list(input_label.keys())[0] for input_label in input_labels]
    output_labels_keys = [list(output_label.keys())[0] for output_label in output_labels]

    graph.add_node(
        id="codeFragment1",
        state=CodeFragmentState(
            model="doubao-deepseek-v3",
            language="python",
            code="def userFunction(params):\n    result = {}\n    result['"
                 + output_labels_keys[0] + "'] = \"代码块处理后的用户输入\"\n    result['input'] = params['"
                 + input_label_keys[0] + "']\n    return result",
            input_labels=input_labels,
            output_labels=output_labels
        )
    )

    graph.add_node(
        id="confirmreply1",
        state=ConfirmReplyState(
            stream=True
        )
    )

    # 添加连接边
    graph.add_edge(START, "codeFragment1", "finish", "switchAny")
    graph.add_edge(START, "codeFragment1", "userChatInput", input_label_keys[0])
    
    graph.add_edge("codeFragment1", "confirmreply1", output_labels_keys[0], "text")
    

    # 编译工作流
    graph.compile(
        name="代码块执行",
        intro="这是一个专业的代码块执行系统",
        category="代码块执行",
        prologue="你好！我是你的代码块执行系统。"
    )


if __name__ == "__main__":
    main()