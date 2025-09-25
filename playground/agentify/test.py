import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models import QuestionInputState, KnowledgeSearchState, AiChatState, ConfirmReplyState, ForEachState

def main():
    graph = FlowGraph(
        personal_auth_key="7217394b7d3e4becab017447adeac239",
        personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    graph.add_node(
        id=START,  # 或者使用 "simpleInputId"
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            fileContrast=False,
            initialInput=True
        )
    )

    # 循环处理模块
    graph.add_node(
        id="batchProcessor",
        state=ForEachState()
    )

    # 循环内：AI分析每个项目
    graph.add_node(
        id="analyzeItem",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="你是数据分析专家，请对以下内容进行简要分析和总结。",
            temperature=0.3
        )
    )
    
    # 循环完成后的总结
    graph.add_node(
        id="finalSummary",
        state=ConfirmReplyState(
            text="批量分析完成！已成功处理所有项目。",
            isvisible=True
        )
    )

    # 添加连接边
    graph.add_edge(START, "batchProcessor", "finish", "switchAny")
    graph.add_edge(START, "batchProcessor", "userChatInput", "items")
    
    # 循环结构连接
    graph.add_edge("batchProcessor", "analyzeItem", "loopStart", "switchAny")
    graph.add_edge("analyzeItem", "batchProcessor", "finish", "loopEnd")
    
    # 循环完成后触发总结
    graph.add_edge("batchProcessor", "finalSummary", "finish", "switchAny")

    # 编译
    graph.compile(
        name="循环批量处理助手",
        intro="这是一个批量处理系统，可以对您的数据列表进行逐项分析",
        category="批量处理",
        prologue="请输入需要分析的数据列表（JSON数组格式），例如：[\"项目1\", \"项目2\", \"项目3\"]"
    )

if __name__ == "__main__":
    main()
