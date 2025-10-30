from autoagents_graph.engine.agentify.services.agentify_graph import AgentifyGraph
from autoagents_graph.engine.agentify.models.graph_types import QuestionInputState, AiChatState, ConfirmReplyState

# 初始化
graph = AgentifyGraph(
    personal_auth_key="1558352c152b484ead33187a3a0ab035",
    personal_auth_secret="ZBlCbwYjcoBYmJTPGKiUgXM2XRUvf3s1",
    base_url="https://test.agentspro.cn"
)

# 添加节点
graph.add_node("input", state=QuestionInputState())
graph.add_node("ai", state=AiChatState())
graph.add_edge("input", "ai")
graph.add_node("confirm_reply_3", state=ConfirmReplyState())
graph.add_edge("ai", "confirm_reply_3")
# 测试 update 方法
try:
    graph.update(
        agent_id=2266,  # 替换成真实的智能体ID
        name="更新后的智能体名称",
        intro="这是更新后的介绍"
    )
    print("✅ update 方法调用成功！")
except Exception as e:
    print(f"❌ 出错了: {e}")