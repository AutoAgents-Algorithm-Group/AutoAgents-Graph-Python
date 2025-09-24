from copy import deepcopy
from typing import Dict, List, Any, Tuple, Optional, Union

import requests
from ..models import CreateAppParams

def create_app_api(data: CreateAppParams, personal_auth_key: str, personal_auth_secret: str, base_url: str) -> requests.Response:
    jwt_token = get_jwt_token_api(personal_auth_key, personal_auth_secret, base_url)

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    url=f"{base_url}/api/agent/create"
    response = requests.post(url, json=data.model_dump(), headers=headers)
    # 判断请求结果
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("code") == 1:
            # 成功，返回接口响应内容（包含知识库ID等信息）
            print(f"《{data.name}》智能体创建成功，请在灵搭平台查看")
            return response_data
        else:
            raise Exception(f"创建智能体失败: {response_data.get('msg', 'Unknown error')}")
    else:
        raise Exception(f"创建智能体失败: {response.status_code} - {response.text}")

def get_jwt_token_api(
    personal_auth_key: str,
    personal_auth_secret: str,
    base_url: str = "https://uat.agentspro.cn",
) -> str:
    """
    获取 AutoAgents AI 平台的 JWT 认证令牌，用户级认证，用于后续的 API 调用认证。
    JWT token 具有时效性，30天过期后需要重新获取。
    
    Args:
        agent_id (str): Agent 的唯一标识符，用于调用Agent对话
            - 获取方式：Agent详情页 - 分享 - API
            
        personal_auth_key (str): 认证密钥
            - 获取方式：右上角 - 个人密钥
            
        personal_auth_secret (str): 认证密钥
            - 获取方式：右上角 - 个人密钥

        base_url (str, optional): API 服务基础地址
            - 默认值: "https://uat.agentspro.cn"
            - 测试环境: "https://uat.agentspro.cn"  
            - 生产环境: "https://agentspro.cn"
            - 私有部署时可指定自定义地址
            
    Returns:
        str: JWT 认证令牌            
    """
    
    headers = {
        "Authorization": f"Bearer {personal_auth_key}.{personal_auth_secret}",
        "Content-Type": "application/json"
    }

    url = f"{base_url}/openapi/user/auth"
    response = requests.get(url, headers=headers)
    return response.json()["data"]["token"]