#!/usr/bin/env python3
"""
测试简化后的Text2Workflow API - 只使用add_node方法，通过BaseModel判断节点类型
"""

import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(project_root, 'src'))

from Text2Workflow import Text2Workflow
from agentify.types.GraphTypes import QuestionInputState, AiChatState, ConfirmReplyState, KnowledgeSearchState
from dify.DifyTypes import DifyStartNodeData, DifyLLMNodeData, DifyKnowledgeRetrievalNodeData, DifyEndNodeData


def test_text2workflow_dify_with_basemodel():
    """测试使用BaseModel的Dify平台工作流"""
    print("=== 测试Text2Workflow (Dify平台) - 使用BaseModel ===")
    
    # 创建Dify平台的Text2Workflow
    workflow = Text2Workflow(
        platform="dify",
        app_name="BaseModel测试工作流",
        app_description="使用BaseModel自动判断节点类型"
    )
    
    print(f"当前平台: {workflow.get_platform()}")
    
    # 方式1: 使用Dify原生的NodeData
    print("\n使用Dify原生NodeData添加节点:")
    
    # 添加开始节点
    start_data = DifyStartNodeData(title="开始")
    workflow.add_node("start_1", start_data, {"x": 50, "y": 200})
    print("✅ 添加开始节点 (DifyStartNodeData)")
    
    # 添加LLM节点
    llm_data = DifyLLMNodeData(
        title="智能分析",
        prompt_template=[{"role": "system", "text": "你是一个专业的AI助手，请分析用户的问题。"}],
        model={
            "completion_params": {"temperature": 0.7},
            "mode": "chat",
            "name": "doubao-deepseek-v3",
            "provider": ""
        }
    )
    workflow.add_node("llm_1", llm_data, {"x": 300, "y": 200})
    print("✅ 添加LLM节点 (DifyLLMNodeData)")
    
    # 添加知识检索节点
    knowledge_data = DifyKnowledgeRetrievalNodeData(
        dataset_ids=["kb_1", "kb_2"],
        multiple_retrieval_config={"top_k": 5, "reranking_enable": True}
    )
    workflow.add_node("knowledge_1", knowledge_data, {"x": 550, "y": 200})
    print("✅ 添加知识检索节点 (DifyKnowledgeRetrievalNodeData)")
    
    # 添加结束节点
    end_data = DifyEndNodeData(title="结束")
    workflow.add_node("end_1", end_data, {"x": 800, "y": 200})
    print("✅ 添加结束节点 (DifyEndNodeData)")
    
    # 方式2: 使用AgentsPro的State，自动转换为Dify格式
    print("\n使用AgentsPro State自动转换:")
    
    # 添加AI对话节点 (从AiChatState转换)
    ai_state = AiChatState(
        model="doubao-deepseek-v3",
        temperature=0.8,
        text="基于检索结果，给用户提供准确答案。"
    )
    workflow.add_node("llm_2", ai_state, {"x": 1050, "y": 200})
    print("✅ 添加AI对话节点 (从AiChatState转换)")
    
    # 添加连接
    workflow.add_edge("start_1", "llm_1")
    workflow.add_edge("llm_1", "knowledge_1") 
    workflow.add_edge("knowledge_1", "llm_2")
    workflow.add_edge("llm_2", "end_1")
    print("✅ 添加连接边")
    
    # 编译和保存
    yaml_result = workflow.compile()
    workflow.save("basemodel_dify_workflow.yaml")
    
    print(f"\n编译完成，YAML长度: {len(yaml_result)} 字符")
    print("已保存到: basemodel_dify_workflow.yaml")
    
    return workflow


def test_text2workflow_agentify_with_basemodel():
    """测试使用BaseModel的AgentsPro平台工作流"""
    print("\n=== 测试Text2Workflow (AgentsPro平台) - 使用BaseModel ===")
    
    try:
        # 创建AgentsPro平台的Text2Workflow
        workflow = Text2Workflow(
            platform="agentify",
            personal_auth_key="test_key",
            personal_auth_secret="test_secret"
        )
        
        print(f"当前平台: {workflow.get_platform()}")
        
        # 使用AgentsPro原生State
        print("\n使用AgentsPro原生State添加节点:")
        
        # 添加用户输入节点
        question_state = QuestionInputState(
            inputText=True,
            uploadFile=False,
            initialInput=True
        )
        workflow.add_node("input_1", question_state, {"x": 50, "y": 200})
        print("✅ 添加用户输入节点 (QuestionInputState)")
        
        # 添加AI对话节点
        ai_state = AiChatState(
            model="doubao-deepseek-v3",
            temperature=0.7,
            text="请帮助用户解决问题。",
            maxToken=2000
        )
        workflow.add_node("ai_1", ai_state, {"x": 300, "y": 200})
        print("✅ 添加AI对话节点 (AiChatState)")
        
        # 添加知识搜索节点
        knowledge_state = KnowledgeSearchState(
            datasets=["knowledge_base_1"],
            topK=5,
            similarity=0.8,
            enableRerank=True
        )
        workflow.add_node("search_1", knowledge_state, {"x": 550, "y": 200})
        print("✅ 添加知识搜索节点 (KnowledgeSearchState)")
        
        # 添加确认回复节点
        reply_state = ConfirmReplyState(
            text="感谢使用我们的服务！",
            stream=True
        )
        workflow.add_node("reply_1", reply_state, {"x": 800, "y": 200})
        print("✅ 添加确认回复节点 (ConfirmReplyState)")
        
        # 添加连接
        workflow.add_edge("input_1", "ai_1")
        workflow.add_edge("ai_1", "search_1")
        workflow.add_edge("search_1", "reply_1")
        print("✅ 添加连接边")
        
        # 保存配置
        workflow.save("basemodel_agentify_workflow.json")
        print("已保存到: basemodel_agentify_workflow.json")
        
        return workflow
        
    except Exception as e:
        print(f"⚠️ AgentsPro平台测试需要真实凭据: {e}")
        return None


def test_mixed_approach():
    """测试混合使用不同类型的BaseModel"""
    print("\n=== 测试混合使用不同BaseModel ===")
    
    workflow = Text2Workflow(
        platform="dify", 
        app_name="混合BaseModel工作流"
    )
    
    # 混合使用Dify原生数据和AgentsPro State
    
    # 1. 使用Dify原生开始节点
    start_data = DifyStartNodeData(title="开始处理")
    workflow.add_node("start", start_data, {"x": 50, "y": 200})
    
    # 2. 使用AgentsPro的AI对话状态（自动转换）
    ai_state = AiChatState(
        model="doubao-deepseek-v3",
        text="请分析用户的问题类型",
        temperature=0.5
    )
    workflow.add_node("analyzer", ai_state, {"x": 300, "y": 200})
    
    # 3. 使用Dify原生知识检索节点
    knowledge_data = DifyKnowledgeRetrievalNodeData(
        title="专业知识库",
        dataset_ids=["professional_kb"],
        multiple_retrieval_config={"top_k": 3}
    )
    workflow.add_node("knowledge", knowledge_data, {"x": 550, "y": 200})
    
    # 4. 使用AgentsPro的确认回复状态（自动转换为end节点）
    reply_state = ConfirmReplyState(text="处理完成")
    workflow.add_node("end", reply_state, {"x": 800, "y": 200})
    
    # 连接节点
    workflow.add_edge("start", "analyzer")
    workflow.add_edge("analyzer", "knowledge")
    workflow.add_edge("knowledge", "end")
    
    # 保存
    workflow.save("mixed_basemodel_workflow.yaml")
    
    print("✅ 混合使用测试完成")
    print("节点类型:")
    print("  - start: DifyStartNodeData")
    print("  - analyzer: AiChatState -> llm")
    print("  - knowledge: DifyKnowledgeRetrievalNodeData")
    print("  - end: ConfirmReplyState -> end")
    print("已保存到: mixed_basemodel_workflow.yaml")
    
    return workflow


def main():
    """主测试函数"""
    print("🚀 测试简化的Text2Workflow API")
    print("=" * 60)
    
    # 测试1: Dify平台使用BaseModel
    dify_workflow = test_text2workflow_dify_with_basemodel()
    
    # 测试2: AgentsPro平台使用BaseModel
    agentify_workflow = test_text2workflow_agentify_with_basemodel()
    
    # 测试3: 混合使用不同BaseModel
    mixed_workflow = test_mixed_approach()
    
    print("\n" + "=" * 60)
    print("🎉 简化API测试完成！")
    
    print("\n生成的文件:")
    generated_files = [
        "basemodel_dify_workflow.yaml",
        "basemodel_agentify_workflow.json", 
        "mixed_basemodel_workflow.yaml"
    ]
    
    for file in generated_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (未生成)")
    
    print("\n✨ 新的API特点:")
    print("  1. 只需要一个add_node方法")
    print("  2. 通过BaseModel自动判断节点类型")
    print("  3. 支持Dify原生数据和AgentsPro State混用")
    print("  4. 平台间自动转换")


if __name__ == "__main__":
    main()
