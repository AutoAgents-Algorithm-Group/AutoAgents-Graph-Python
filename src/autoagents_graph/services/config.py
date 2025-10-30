from typing import Optional
from pydantic import BaseModel, Field


class AgentifyConfig(BaseModel):
    """Agentify平台配置"""
    personal_auth_key: Optional[str] = Field(default=None, description="AgentsPro平台的认证密钥（如果提供了jwt_token则可选）")
    personal_auth_secret: Optional[str] = Field(default=None, description="AgentsPro平台的认证密码（如果提供了jwt_token则可选）")
    jwt_token: Optional[str] = Field(default=None, description="JWT认证令牌（可选，如果提供则直接使用，不再调用获取token接口）")
    base_url: str = Field(default="https://uat.agentspro.cn", description="API基础URL")
    
    def model_post_init(self, __context):
        """验证至少提供一种认证方式"""
        if self.jwt_token is None and (self.personal_auth_key is None or self.personal_auth_secret is None):
            raise ValueError("必须提供 jwt_token 或者同时提供 personal_auth_key 和 personal_auth_secret")


class DifyConfig(BaseModel):
    """Dify平台配置"""
    app_name: str = Field(default="AutoAgents工作流", description="应用名称")
    app_description: str = Field(default="基于AutoAgents SDK构建的工作流", description="应用描述")
    app_icon: str = Field(default="🤖", description="应用图标")
    app_icon_background: str = Field(default="#FFEAD5", description="应用图标背景色")
    api_key: Optional[str] = Field(default=None, description="Dify API密钥（用于自动部署）")
    base_url: str = Field(default="https://api.dify.ai", description="Dify API基础URL")

