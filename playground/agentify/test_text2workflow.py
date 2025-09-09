import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.Text2Workflow import Text2Workflow
from src.agentify.types import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState
from src.dify import DifyStartNodeData, DifyLLMNodeData, DifyEndNodeData


def test_agentify_platform():
    """测试AgentsPro平台的Text2Workflow"""
    print("=== 测试AgentsPro平台 ===")
    
    # 创建AgentsPro平台工作流
    workflow = Text2Workflow(
        platform="agentify",
        personal_auth_key="7217394b7d3e4becab017447adeac239",
        personal_auth_secret="f4Ziua6B0NexIMBGj1tQEVpe62EhkCWB",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点 - 使用AgentsPro原生State
    workflow.add_node(
        "question_input",
        QuestionInputState(
            inputText=True,
            uploadFile=False,
            initialInput=True
        ),
        {"x": 50, "y": 200}
    )

    workflow.add_node(
        "ai_chat",
        AiChatState(
            model="doubao-deepseek-v3",
            text="你是一个专业的AI助手，请根据用户的问题提供帮助。",
            temperature=0.7,
            maxToken=2000,
            stream=True
        ),
        {"x": 300, "y": 200}
    )

    workflow.add_node(
        "knowledge_search",
        KnowledgeSearchState(
            datasets=["general_kb"],
            topK=5,
            similarity=0.7,
            enableRerank=True
        ),
        {"x": 550, "y": 200}
    )

    workflow.add_node(
        "confirm_reply",
        ConfirmReplyState(
            text="希望我的回答对您有帮助！如有其他问题，请随时询问。",
            stream=True
        ),
        {"x": 800, "y": 200}
    )

    # 添加连接边
    workflow.add_edge("question_input", "ai_chat", "finish", "switchAny")
    workflow.add_edge("ai_chat", "knowledge_search", "finish", "switchAny")
    workflow.add_edge("knowledge_search", "confirm_reply", "finish", "switchAny")

    # 编译工作流
    workflow.compile(
        name="Text2Workflow测试助手",
        intro="基于Text2Workflow构建的智能助手",
        category="测试",
        prologue="你好！我是Text2Workflow测试助手，请告诉我如何帮助您。",
        shareAble=True,
        allowVoiceInput=False
    )
    
    print("✅ AgentsPro平台测试完成")


def test_dify_platform():
    """测试Dify平台的Text2Workflow"""
    print("\n=== 测试Dify平台 ===")
    
    # 创建Dify平台工作流
    workflow = Text2Workflow(
        platform="dify",
        app_name="Text2Workflow Dify测试",
        app_description="使用Text2Workflow创建的Dify工作流测试",
        app_icon="🧪"
    )

    # 添加节点 - 使用Dify原生NodeData
    workflow.add_node(
        "start",
        DifyStartNodeData(
            title="开始处理",
            desc="用户问题输入入口"
        ),
        {"x": 50, "y": 200}
    )

    workflow.add_node(
        "llm_analysis",
        DifyLLMNodeData(
            title="问题分析",
            desc="分析用户问题的类型和意图",
            prompt_template=[{
                "role": "system",
                "text": "你是一个专业的问题分析师。请分析用户的问题，判断问题类型并提供初步建议。"
            }],
            model={
                "completion_params": {"temperature": 0.5},
                "mode": "chat",
                "name": "doubao-deepseek-v3",
                "provider": ""
            }
        ),
        {"x": 300, "y": 200}
    )

    # 添加节点 - 使用AgentsPro State（自动转换）
    ai_state = AiChatState(
        model="doubao-deepseek-v3",
        text="基于分析结果，为用户提供详细的解答和建议。",
        temperature=0.8,
        maxToken=1500
    )
    workflow.add_node("final_answer", ai_state, {"x": 550, "y": 200})

    workflow.add_node(
        "end",
        DifyEndNodeData(
            title="处理完成",
            desc="问题处理结束"
        ),
        {"x": 800, "y": 200}
    )

    # 添加连接边
    workflow.add_edge("start", "llm_analysis")
    workflow.add_edge("llm_analysis", "final_answer")
    workflow.add_edge("final_answer", "end")

    # 编译并保存
    yaml_output = workflow.compile()
    workflow.save("text2workflow_dify_test.yaml")
    
    print(f"✅ Dify平台测试完成，生成YAML长度: {len(yaml_output)} 字符")
    print("📁 已保存到: text2workflow_dify_test.yaml")


def test_mixed_usage():
    """测试混合使用两种平台的BaseModel"""
    print("\n=== 测试混合使用BaseModel ===")
    
    workflow = Text2Workflow(
        platform="dify",
        app_name="混合测试工作流"
    )

    # 混合使用Dify原生数据和AgentsPro State
    
    # 1. Dify原生开始节点
    start_data = DifyStartNodeData(title="混合测试开始")
    workflow.add_node("start", start_data, {"x": 50, "y": 200})
    
    # 2. AgentsPro AI状态（自动转换为Dify LLM）
    ai_state = AiChatState(
        model="doubao-deepseek-v3",
        text="这是一个混合测试，展示AgentsPro State自动转换为Dify格式。",
        temperature=0.6
    )
    workflow.add_node("ai_converted", ai_state, {"x": 300, "y": 200})
    
    # 3. AgentsPro确认状态（自动转换为Dify end）
    confirm_state = ConfirmReplyState(text="混合测试完成")
    workflow.add_node("end", confirm_state, {"x": 550, "y": 200})
    
    # 连接
    workflow.add_edge("start", "ai_converted")
    workflow.add_edge("ai_converted", "end")
    
    # 保存
    workflow.save("mixed_test_workflow.yaml")
    print("✅ 混合使用测试完成")
    print("📁 已保存到: mixed_test_workflow.yaml")


def main():
    """主测试函数"""
    print("🧪 Text2Workflow 功能测试")
    print("=" * 50)
    
    try:
        # 测试1: AgentsPro平台
        test_agentify_platform()
        
        # 测试2: Dify平台
        test_dify_platform()
        
        # 测试3: 混合使用
        test_mixed_usage()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试完成！")
        
        print("\n✨ 测试特点:")
        print("  1. 统一的add_node API")
        print("  2. BaseModel自动类型判断")
        print("  3. 平台自动适配")
        print("  4. 支持原生数据和自动转换")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        print("💡 提示: AgentsPro平台测试需要有效的认证凭据")


if __name__ == "__main__":
    main()
