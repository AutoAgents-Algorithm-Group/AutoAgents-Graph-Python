"""
演示SDK代码如何与Agentify平台通信的机制
"""
import json
import requests


def demo_sdk_mechanism():
    """演示SDK与平台通信的完整流程"""
    
    print("=" * 60)
    print("SDK 与 Agentify 平台通信机制演示")
    print("=" * 60)
    
    # ========== 步骤1: 准备认证信息 ==========
    print("\n【步骤1】准备认证信息")
    print("-" * 60)
    
    personal_auth_key = "your_key_here"
    personal_auth_secret = "your_secret_here"
    base_url = "https://uat.agentspro.cn"
    
    print(f"Key: {personal_auth_key[:10]}...")
    print(f"Secret: {personal_auth_secret[:10]}...")
    print(f"平台地址: {base_url}")
    
    # ========== 步骤2: 构建工作流数据 ==========
    print("\n【步骤2】构建工作流数据")
    print("-" * 60)
    
    workflow_data = {
        "nodes": [
            {
                "id": "simpleInputId",
                "type": "custom",
                "position": {"x": 100, "y": 200},
                "data": {
                    "moduleType": "questionInput",
                    "name": "用户提问",
                    "inputs": [],
                    "outputs": [
                        {
                            "key": "userChatInput",
                            "type": "source",
                            "valueType": "string",
                            "label": "文本信息"
                        }
                    ]
                }
            },
            {
                "id": "ai_chat",
                "type": "custom",
                "position": {"x": 400, "y": 200},
                "data": {
                    "moduleType": "aiChat",
                    "name": "智能对话",
                    "inputs": [
                        {
                            "key": "model",
                            "value": "gpt-4",
                            "type": "selectChatModel"
                        }
                    ],
                    "outputs": []
                }
            }
        ],
        "edges": [
            {
                "id": "edge-1",
                "source": "simpleInputId",
                "target": "ai_chat",
                "sourceHandle": "finish",
                "targetHandle": "switchAny"
            }
        ]
    }
    
    print(f"节点数量: {len(workflow_data['nodes'])}")
    print(f"连线数量: {len(workflow_data['edges'])}")
    print("\n工作流JSON数据（部分）:")
    print(json.dumps(workflow_data, indent=2, ensure_ascii=False)[:300] + "...")
    
    # ========== 步骤3: 准备API请求数据 ==========
    print("\n【步骤3】准备API请求数据")
    print("-" * 60)
    
    api_request_data = {
        "name": "SDK测试智能体",
        "intro": "通过SDK创建的智能体",
        "prologue": "您好！我是SDK创建的智能体",
        "avatar": "https://uat.agentspro.cn/assets/agent/avatar.png",
        "appModel": json.dumps(workflow_data, ensure_ascii=False),  # 核心！
        "category": "测试",
        "shareAble": True,
        "allowVoiceInput": False
    }
    
    print(f"智能体名称: {api_request_data['name']}")
    print(f"智能体介绍: {api_request_data['intro']}")
    print(f"appModel长度: {len(api_request_data['appModel'])} 字符")
    
    # ========== 步骤4: 模拟认证过程 ==========
    print("\n【步骤4】模拟认证过程")
    print("-" * 60)
    
    print("第一次请求: 获取JWT Token")
    print(f"  GET {base_url}/openapi/user/auth")
    print(f"  Headers:")
    print(f"    Authorization: Bearer {personal_auth_key}.{personal_auth_secret}")
    print(f"    Content-Type: application/json")
    print(f"\n  响应 (模拟):")
    print(f"    {{")
    print(f"      \"code\": 1,")
    print(f"      \"data\": {{")
    print(f"        \"token\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\"")
    print(f"      }}")
    print(f"    }}")
    
    jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.mock_token"
    
    # ========== 步骤5: 模拟创建智能体请求 ==========
    print("\n【步骤5】模拟创建智能体请求")
    print("-" * 60)
    
    print("第二次请求: 创建智能体")
    print(f"  POST {base_url}/api/agent/create")
    print(f"  Headers:")
    print(f"    Authorization: Bearer {jwt_token[:30]}...")
    print(f"    Content-Type: application/json")
    print(f"\n  Body (JSON):")
    print(f"    name: {api_request_data['name']}")
    print(f"    intro: {api_request_data['intro']}")
    print(f"    appModel: <工作流JSON数据>")
    print(f"    ... (其他字段)")
    
    print(f"\n  响应 (模拟):")
    print(f"    {{")
    print(f"      \"code\": 1,")
    print(f"      \"msg\": \"success\",")
    print(f"      \"data\": {{")
    print(f"        \"agentId\": \"agent_123456\",")
    print(f"        \"name\": \"{api_request_data['name']}\"")
    print(f"      }}")
    print(f"    }}")
    
    # ========== 步骤6: 总结 ==========
    print("\n【步骤6】总结")
    print("-" * 60)
    print("✅ SDK代码在平台生成组件需要:")
    print("   1. 认证信息 (personal_auth_key, personal_auth_secret)")
    print("   2. 平台地址 (base_url)")
    print("   3. 工作流数据 (nodes, edges)")
    print("   4. 网络连接 (HTTP请求)")
    print("   5. API接口 (/openapi/user/auth, /api/agent/create)")
    print("\n✅ 核心原理:")
    print("   SDK → 构建JSON → 获取Token → 发送HTTP请求 → 平台创建")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


def demo_data_flow():
    """演示数据流转过程"""
    
    print("\n\n" + "=" * 60)
    print("数据流转过程演示")
    print("=" * 60)
    
    print("""
    【本地 - Python代码】
        ↓
        workflow.add_node(id="user_input", state=QuestionInputState())
        ↓
    【内存 - Python对象】
        ↓
        AgentifyNode(
            id="simpleInputId",
            data={"moduleType": "questionInput", ...}
        )
        ↓
    【序列化 - JSON字符串】
        ↓
        '{"nodes":[{"id":"simpleInputId","data":{...}}]}'
        ↓
    【网络传输 - HTTP请求】
        ↓
        POST /api/agent/create
        Body: {"name":"...", "appModel":"..."}
        ↓
    【平台服务器 - 接收处理】
        ↓
        1. 验证JWT Token
        2. 解析JSON数据
        3. 存储到数据库
        4. 返回成功响应
        ↓
    【平台界面 - 显示结果】
        ↓
        用户在网页上看到新创建的智能体
        包含所有节点和连线
    """)


def demo_comparison():
    """对比Agentify和Dify的不同机制"""
    
    print("\n\n" + "=" * 60)
    print("Agentify vs Dify 机制对比")
    print("=" * 60)
    
    print("\n【Agentify - 在线平台模式】")
    print("-" * 60)
    print("流程:")
    print("  1. SDK代码 → 构建数据")
    print("  2. compile() → 调用API")
    print("  3. 上传到云端 → 立即可用")
    print("  4. 在网页打开 → 看到智能体")
    print("\n特点:")
    print("  ✓ 需要网络连接")
    print("  ✓ 需要认证信息")
    print("  ✓ 直接在云端创建")
    print("  ✓ 团队协作友好")
    
    print("\n【Dify - 配置文件模式】")
    print("-" * 60)
    print("流程:")
    print("  1. SDK代码 → 构建数据")
    print("  2. compile() → 生成YAML")
    print("  3. 保存到文件 → 本地文件")
    print("  4. 手动导入 → 在Dify平台使用")
    print("\n特点:")
    print("  ✓ 可离线使用")
    print("  ✓ 不需要认证信息（生成YAML时）")
    print("  ✓ 生成配置文件")
    print("  ✓ 可本地部署")
    
    print("\n【使用场景对比】")
    print("-" * 60)
    print("Agentify适合:")
    print("  • SaaS云服务")
    print("  • 需要快速部署")
    print("  • 团队协作开发")
    print("\nDify适合:")
    print("  • 开源自部署")
    print("  • 需要版本控制")
    print("  • 灵活定制化")


if __name__ == "__main__":
    demo_sdk_mechanism()
    demo_data_flow()
    demo_comparison()

