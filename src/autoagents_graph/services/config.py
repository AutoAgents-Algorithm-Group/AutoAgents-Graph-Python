from typing import Optional
from pydantic import BaseModel, Field


class AgentifyConfig(BaseModel):
    """Agentify平台配置"""
    personal_auth_key: str = Field(..., description="AgentsPro平台的认证密钥")
    personal_auth_secret: str = Field(..., description="AgentsPro平台的认证密码")
    base_url: str = Field(default="https://uat.agentspro.cn", description="API基础URL")


class DifyConfig(BaseModel):
    """Dify平台配置"""
    app_name: str = Field(default="AutoAgents工作流", description="应用名称")
    app_description: str = Field(default="基于AutoAgents SDK构建的工作流", description="应用描述")
    app_icon: str = Field(default="🤖", description="应用图标")
    app_icon_background: str = Field(default="#FFEAD5", description="应用图标背景色")

