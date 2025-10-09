import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uuid
from src.autoagents_graph import NL2Workflow, AgentifyConfig
from src.autoagents_graph.engine.agentify import START
from src.autoagents_graph.engine.agentify.models import QuestionInputState, InfoClassState, AiChatState, ConfirmReplyState, KnowledgeSearchState


def main():
    workflow = NL2Workflow(
        platform="agentify",
        config=AgentifyConfig(
            personal_auth_key="7217394b7d3e4becab017447adeac239",
            personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
            base_url="https://uat.agentspro.cn"
        )
    )

    # 用户输入节点
    workflow.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            initialInput=True
        )
    )

    # 信息分类节点
    ad_label_id = str(uuid.uuid1())
    other_label_id = str(uuid.uuid1())
    
    workflow.add_node(
        id="classifier",
        state=InfoClassState(
            model="doubao-deepseek-v3",
            quotePrompt="""请判断用户输入是否与广告相关。

广告相关包括：
- 广告创意、文案、策划
- 广告投放、渠道、效果
- 营销推广、品牌宣传
- 广告设计、制作
- 广告法规、合规问题
- 其他广告行业相关问题

请严格按照JSON格式返回分类结果。""",
            labels={
                ad_label_id: "广告相关",
                other_label_id: "其他问题"
            }
        )
    )

    # 知识库搜索节点
    workflow.add_node(
        id="kb_search",
        state=KnowledgeSearchState(
            datasets=["ad_knowledge_base"],
            similarity=0.2,
            topK=20,
            enableRerank=False
        )
    )

    # 广告问题AI回答节点
    workflow.add_node(
        id="ad_answer",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是一个专业的广告助手，请根据知识库内容回答用户的广告相关问题。

要求：
1. 基于知识库内容提供准确、专业的回答
2. 如果知识库内容不足，请结合广告行业常识补充
3. 回答要具体、实用，有助于解决用户问题
4. 保持专业、友好的语调""",
            temperature=0.1,
            maxToken=3000,
            isvisible=True,
            historyText=3
        )
    )

    # 非广告问题回复节点
    workflow.add_node(
        id="other_reply",
        state=ConfirmReplyState(
            text="抱歉，我只能处理广告相关的问题。如果您有广告创意、投放策略、文案撰写等方面的需求，我很乐意为您提供帮助！",
            isvisible=True
        )
    )

    # 添加连接边
    # 用户输入到分类器
    workflow.add_edge(START, "classifier", "finish", "switchAny")
    workflow.add_edge(START, "classifier", "userChatInput", "text")

    # 广告相关分支：分类器 -> 知识库搜索 -> AI回答
    workflow.add_edge("classifier", "kb_search", ad_label_id, "switchAny")
    workflow.add_edge(START, "kb_search", "userChatInput", "text")
    
    workflow.add_edge("kb_search", "ad_answer", "finish", "switchAny")
    workflow.add_edge(START, "ad_answer", "userChatInput", "text")
    workflow.add_edge("kb_search", "ad_answer", "quoteQA", "knSearch")

    # 其他问题分支：分类器 -> 确定回复
    workflow.add_edge("classifier", "other_reply", other_label_id, "switchAny")

    # 编译工作流
    workflow.compile(
        name="智能广告处理助手",
        intro="专业的广告助手，能够根据用户输入智能分类处理，为广告相关问题提供专业解答",
        category="营销助手",
        prologue="您好！我是您的专业广告助手，可以帮您解答广告创意、投放策略、文案撰写等各类广告相关问题。请告诉我您想了解什么？"
    )

if __name__ == "__main__":
    main()