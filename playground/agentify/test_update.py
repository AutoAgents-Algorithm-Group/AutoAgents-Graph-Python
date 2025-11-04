import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import uuid
from src.autoagents_graph import NL2Workflow, AgentifyConfig
from src.autoagents_graph.engine.agentify import START
from src.autoagents_graph.engine.agentify.models import (
    QuestionInputState, InfoClassState, AiChatState, KnowledgeSearchState
)


def main():
    """
    测试增强版 update 方法的完整功能：
    1. 创建/使用现有智能体
    2. 演示三种更新模式：合并、替换、信息更新
    3. 展示智能节点连接和工作流管理
    4. 验证更新结果
    """
    
    # 初始化工作流
    workflow = NL2Workflow(
        platform="agentify",
        config=AgentifyConfig(
            personal_auth_key="1558352c152b484ead33187a3a0ab035",
            personal_auth_secret="ZBlCbwYjcoBYmJTPGKiUgXM2XRUvf3s1",
            base_url="https://test.agentspro.cn"
        )
    )

    print("=== 增强版 update 方法测试 ===")
    print("支持功能：")
    print("✅ 获取现有工作流配置")
    print("✅ 合并模式 - 在现有基础上添加功能")
    print("✅ 替换模式 - 完全替换工作流")
    print("✅ 信息更新 - 只更新智能体信息")
    print("✅ 智能节点连接处理")

    # 选择测试模式
    print("\n请选择测试方式：")
    print("1. 创建新智能体并测试更新")
    print("2. 使用现有智能体测试更新")
    
    choice = input("输入选择 (1/2): ").strip()
    
    if choice == "1":
        agent_id = create_new_agent(workflow)
        if not agent_id:
            return
    else:
        agent_id = input("请输入现有智能体ID: ").strip()
        try:
            agent_id = int(agent_id)
        except ValueError:
            print("❌ 无效的智能体ID")
            return
        
        # 验证智能体是否存在
        try:
            current_config = workflow.get_json(agent_id)
            current_nodes = len(current_config.get('nodes', []))
            current_edges = len(current_config.get('edges', []))
            print(f"✅ 智能体 {agent_id} 存在")
            print(f"当前工作流: {current_nodes} 个节点, {current_edges} 个连接")
        except Exception as e:
            print(f"❌ 智能体 {agent_id} 不存在或无法访问: {e}")
            return

    # 开始测试更新功能
    test_update_modes(workflow, agent_id)


def create_new_agent(workflow):
    """创建新的智能体用于测试"""
    
    print("\n=== 创建新智能体 ===")
    
    # 构建简单的初始工作流
    workflow.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=False,
            uploadPicture=False,
            initialInput=True
        )
    )

    workflow.add_node(
        id="basic_chat",
        position={'x': 300, 'y': 100},
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="你是一个基础的智能助手，可以回答用户的各种问题。",
            temperature=0.5,
            maxToken=1500,
            isvisible=True,
            historyText=3
        )
    )

    # 连接节点
    workflow.add_edge(START, "basic_chat", "finish", "switchAny")
    workflow.add_edge(START, "basic_chat", "userChatInput", "text")

    print("📝 构建基础工作流完成")
    
    try:
        agent_id = workflow.compile(
            name="测试智能体（基础版）",
            intro="用于测试更新功能的基础智能体",
            category="测试",
            prologue="您好！我是基础版智能助手，即将进行功能升级测试。"
        )
        
        print(f"✅ 智能体创建成功，ID: {agent_id}")
        return agent_id
        
    except Exception as e:
        print(f"❌ 智能体创建失败: {e}")
        return None


def test_update_modes(workflow, agent_id):
    """测试三种更新模式"""
    
    print(f"\n=== 开始测试智能体 {agent_id} 的更新功能 ===")
    
    # 模式1：合并模式测试
    test_merge_mode(workflow, agent_id)
    
    if input("\n继续测试替换模式？(y/n): ").lower() == 'y':
        test_replace_mode(workflow, agent_id)
    
    if input("\n继续测试信息更新模式？(y/n): ").lower() == 'y':
        test_info_update_mode(workflow, agent_id)
    
    # 最终验证
    verify_final_result(workflow, agent_id)


def test_merge_mode(workflow, agent_id):
    """测试合并模式 - 在现有基础上添加功能"""
    
    print("\n🔀 === 模式1：合并模式测试 ===")
    print("功能：在现有工作流基础上添加知识库搜索和智能分类")
    
    # 获取现有工作流信息，智能选择连接点
    print("🔍 分析现有工作流...")
    existing_nodes = []
    input_node_id = None
    
    try:
        existing_workflow = workflow.get_json(agent_id)
        existing_nodes = existing_workflow.get('nodes', [])
        
        # 寻找合适的连接节点
        for node in existing_nodes:
            module_type = node.get('data', {}).get('moduleType', '')
            node_id = node.get('id', '')
            if module_type == 'questionInput' or node_id == START:
                input_node_id = node_id
                print(f"  📍 找到输入节点: {input_node_id}")
                break
        
        if not input_node_id and existing_nodes:
            input_node_id = existing_nodes[0].get('id', '')
            print(f"  📍 使用第一个节点: {input_node_id}")
            
        print(f"  📊 现有: {len(existing_nodes)} 节点")
        
    except Exception as e:
        print(f"  ⚠️ 获取现有配置失败: {e}")
    
    # 构建新功能节点
    tech_label_id = str(uuid.uuid1())
    general_label_id = str(uuid.uuid1())
    
    # 智能分类器
    workflow.add_node(
        id="smart_classifier",
        position={'x': 200, 'y': 150},
        state=InfoClassState(
            model="doubao-deepseek-v3",
            quotePrompt="""请判断用户问题的类型：

技术问题包括：
- 编程和开发
- 软件使用
- 系统配置
- 故障排查

请严格按JSON格式返回。""",
            labels={
                tech_label_id: "技术问题",
                general_label_id: "一般问题"
            }
        )
    )
    
    # 知识库搜索
    workflow.add_node(
        id="kb_search",
        position={'x': 450, 'y': 100},
        state=KnowledgeSearchState(
            datasets=["tech_docs"],
            similarity=0.3,
            topK=12,
            enableRerank=True
        )
    )
    
    # 技术专家AI
    workflow.add_node(
        id="tech_expert",
        position={'x': 700, 'y': 100},
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是技术专家，请基于知识库内容提供专业技术支持：

1. 优先使用知识库准确信息
2. 提供详细解决方案
3. 包含具体操作步骤
4. 保持专业严谨的态度""",
            temperature=0.2,
            maxToken=3000,
            isvisible=True,
            historyText=6
        )
    )
    
    # 一般助手AI
    workflow.add_node(
        id="general_assistant",
        position={'x': 450, 'y': 300},
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是友好的通用助手，可以：

1. 回答日常问题
2. 提供生活建议
3. 进行轻松对话
4. 保持温暖友善的语调""",
            temperature=0.6,
            maxToken=2000,
            isvisible=True,
            historyText=4
        )
    )
    
    # 构建新节点之间的连接关系
    # 注意：不要尝试连接到现有节点，因为它们不在当前工作流实例中
    # 合并更新时，服务端会自动处理现有节点和新节点的整合
    
    print("🔗 构建新功能模块的内部连接")
    print(f"📝 现有节点({input_node_id})将在合并更新时自动连接到新的分类器")
    
    # 技术分支：分类器 → 知识库搜索 → 技术专家
    workflow.add_edge("smart_classifier", "kb_search", tech_label_id, "switchAny")
    workflow.add_edge("kb_search", "tech_expert", "finish", "switchAny")
    workflow.add_edge("kb_search", "tech_expert", "quoteQA", "knSearch")
    
    # 一般分支：分类器 → 一般助手
    workflow.add_edge("smart_classifier", "general_assistant", general_label_id, "switchAny")
    
    print("✅ 新功能模块连接完成:")
    print("   📊 智能分类器 → 技术问题分支 → 知识库搜索 → 技术专家")  
    print("   📊 智能分类器 → 一般问题分支 → 通用助手")
    print("⚠️  现有工作流的连接将在合并更新时由服务端自动处理")
    
    # 执行合并更新
    try:
        print("🔀 执行合并更新...")
        updated_id = workflow.update(
            agent_id=agent_id,
            load_existing_workflow=True,   # 加载现有工作流
            merge_workflow=True,           # 合并模式
            name="智能助手Pro（技术增强版）",
            intro="具备智能分类、知识库搜索和专业技术支持能力的升级版助手",
            prologue="您好！我已升级为Pro版本，现在可以智能识别您的问题类型并提供专业的技术支持或友好的日常对话。",
            category="智能助手Pro"
        )
        
        print(f"✅ 合并更新成功！ID: {updated_id}")
        print("🎉 新增功能：智能分类 + 知识库搜索 + 专业技术支持")
        
    except Exception as e:
        print(f"❌ 合并更新失败: {e}")


def test_replace_mode(workflow, agent_id):
    """测试替换模式 - 完全替换工作流"""
    
    print("\n🔄 === 模式2：替换模式测试 ===")
    print("功能：完全替换为全新的简洁工作流")
    
    # 重新初始化workflow实例（清空当前构建的节点）
    workflow = NL2Workflow(
        platform="agentify",
        config=AgentifyConfig(
            personal_auth_key="1558352c152b484ead33187a3a0ab035",
            personal_auth_secret="ZBlCbwYjcoBYmJTPGKiUgXM2XRUvf3s1",
            base_url="https://test.agentspro.cn"
        )
    )
    
    # 构建全新的简洁工作流
    workflow.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=True,  # 新增文件上传功能
            uploadPicture=True,  # 新增图片上传功能
            initialInput=True
        )
    )
    
    workflow.add_node(
        id="streamlined_ai",
        position={'x': 400, 'y': 150},
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""你是高效简洁的AI助手：

特点：
- 直接回答，不绕弯子
- 重点突出，条理清晰  
- 支持文件和图片分析
- 快速准确地解决问题

始终保持高效专业的服务风格。""",
            temperature=0.4,
            maxToken=2500,
            isvisible=True,
            historyText=5
        )
    )
    
    # 简单直连
    workflow.add_edge(START, "streamlined_ai", "finish", "switchAny")
    workflow.add_edge(START, "streamlined_ai", "userChatInput", "text")
    
    # 执行替换更新
    try:
        print("🔄 执行完全替换...")
        updated_id = workflow.update(
            agent_id=agent_id,
            load_existing_workflow=True,   # 获取现有信息
            merge_workflow=False,          # 替换模式
            name="高效简洁AI助手",
            intro="专注于快速高效解决问题的简洁型AI助手，支持多媒体输入",
            prologue="您好！我是高效简洁的AI助手，专注于快速准确地解决您的问题。支持文本、文件和图片输入。",
            category="效率工具"
        )
        
        print(f"✅ 完全替换成功！ID: {updated_id}")
        print("🎉 新工作流：多媒体输入 → 高效AI助手")
        
    except Exception as e:
        print(f"❌ 完全替换失败: {e}")


def test_info_update_mode(workflow, agent_id):
    """测试信息更新模式 - 只更新智能体信息"""
    
    print("\n📝 === 模式3：信息更新测试 ===")
    print("功能：仅更新智能体基本信息，工作流结构保持不变")
    
    try:
        print("📝 执行信息更新...")
        updated_id = workflow.update(
            agent_id=agent_id,
            load_existing_workflow=False,  # 不处理工作流结构
            name="AI智能助手Ultimate",
            intro="经过全面优化和调试的终极版AI智能助手",
            prologue="欢迎使用AI智能助手Ultimate！我经过了全面的优化升级，将为您提供最佳的智能服务体验。",
            category="旗舰产品",
            allowVoiceInput=True,  # 开启语音输入
            autoSendVoice=False
        )
        
        print(f"✅ 信息更新成功！ID: {updated_id}")
        print("🎉 仅更新了智能体信息，工作流结构保持不变")
        
    except Exception as e:
        print(f"❌ 信息更新失败: {e}")


def verify_final_result(workflow, agent_id):
    """验证最终更新结果"""
    
    print("\n🔍 === 验证最终结果 ===")
    
    try:
        final_config = workflow.get_json(agent_id)
        final_nodes = len(final_config.get('nodes', []))
        final_edges = len(final_config.get('edges', []))
        
        print("✅ 最终工作流结构:")
        print(f"   📊 节点数量: {final_nodes}")
        print(f"   🔗 连接数量: {final_edges}")
        
        # 显示节点详情
        if final_nodes > 0:
            print("\n📋 节点列表:")
            nodes = final_config.get('nodes', [])
            for i, node in enumerate(nodes[:10]):  # 最多显示10个
                node_id = node.get('id', 'N/A')
                module_type = node.get('data', {}).get('moduleType', 'N/A')
                print(f"   {i+1:2d}. {node_id:<20} ({module_type})")
            
            if final_nodes > 10:
                print(f"   ... 还有 {final_nodes-10} 个节点")
        
        print("\n🎉 所有测试完成！")
        print(f"您可以访问灵搭平台查看智能体 {agent_id} 的最新状态。")
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")


if __name__ == "__main__":
    main()
