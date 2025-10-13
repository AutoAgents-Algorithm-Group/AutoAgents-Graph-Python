import requests
from typing import Dict, Any, Optional
import json


class DifyAPIClient:
    """
    Dify API 客户端
    
    用于与 Dify 平台进行交互，支持创建应用、更新工作流等操作
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.dify.ai"):
        """
        初始化 Dify API 客户端
        
        Args:
            api_key: Dify API 密钥
            base_url: Dify API 基础URL，默认为官方API地址
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_app(self, name: str, mode: str = "workflow", 
                   icon: str = "🤖", description: str = "") -> Dict[str, Any]:
        """
        创建 Dify 应用
        
        Args:
            name: 应用名称
            mode: 应用模式，默认为 "workflow"
            icon: 应用图标，默认为 "🤖"
            description: 应用描述
            
        Returns:
            创建结果，包含应用ID等信息
            
        Raises:
            Exception: 当API调用失败时
        """
        url = f"{self.base_url}/v1/apps"
        data = {
            "name": name,
            "mode": mode,
            "icon": icon,
            "description": description
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Dify应用《{name}》创建成功")
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"创建Dify应用失败: {str(e)}")
    
    def update_workflow(self, app_id: str, yaml_content: str) -> Dict[str, Any]:
        """
        更新应用的工作流配置
        
        Args:
            app_id: 应用ID
            yaml_content: YAML格式的工作流配置
            
        Returns:
            更新结果
            
        Raises:
            Exception: 当API调用失败时
        """
        url = f"{self.base_url}/v1/apps/{app_id}/workflow"
        headers = self.headers.copy()
        headers["Content-Type"] = "application/yaml"
        
        try:
            response = requests.put(url, data=yaml_content, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ 工作流配置更新成功")
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"更新工作流失败: {str(e)}")
    
    def get_app(self, app_id: str) -> Dict[str, Any]:
        """
        获取应用信息
        
        Args:
            app_id: 应用ID
            
        Returns:
            应用信息
            
        Raises:
            Exception: 当API调用失败时
        """
        url = f"{self.base_url}/v1/apps/{app_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取应用信息失败: {str(e)}")
    
    def delete_app(self, app_id: str) -> Dict[str, Any]:
        """
        删除应用
        
        Args:
            app_id: 应用ID
            
        Returns:
            删除结果
            
        Raises:
            Exception: 当API调用失败时
        """
        url = f"{self.base_url}/v1/apps/{app_id}"
        
        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ 应用删除成功")
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"删除应用失败: {str(e)}")
    
    def list_apps(self, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """
        获取应用列表
        
        Args:
            page: 页码，默认为1
            limit: 每页数量，默认为20
            
        Returns:
            应用列表
            
        Raises:
            Exception: 当API调用失败时
        """
        url = f"{self.base_url}/v1/apps"
        params = {
            "page": page,
            "limit": limit
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"获取应用列表失败: {str(e)}")
    
    def validate_workflow(self, yaml_content: str) -> Dict[str, Any]:
        """
        验证工作流配置
        
        Args:
            yaml_content: YAML格式的工作流配置
            
        Returns:
            验证结果
            
        Raises:
            Exception: 当API调用失败时
        """
        url = f"{self.base_url}/v1/workflows/validate"
        headers = self.headers.copy()
        headers["Content-Type"] = "application/yaml"
        
        try:
            response = requests.post(url, data=yaml_content, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"验证工作流失败: {str(e)}")
