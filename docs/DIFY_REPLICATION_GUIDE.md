

## 📊 当前实现状态评估

### ✅ 已完成的模块

| 模块 | 文件路径 | 状态 | 功能描述 |
|------|----------|------|----------|
| 数据模型 | `dify_types.py` | ✅ 完成 | 定义了 4 种基础节点类型 |
| 图构建器 | `dify_graph.py` | ✅ 完成 | 可以构建工作流并导出 YAML |
| Parser | `dify_parser.py` | ✅ 完成 | 可以从 YAML 反向生成 SDK 代码 |
| 测试用例 | `test_dify_parser.py` | ✅ 完成 | 基础测试 |

### ⚠️ 需要补充的模块

| 模块 | 优先级 | 说明 |
|------|--------|------|
| 更多节点类型 | 🔴 高 | 只有 4 种节点，需扩展到 15+ |
| API 集成 | 🟡 中 | 如需自动部署到 Dify 平台 |
| 完整测试 | 🟡 中 | 需要覆盖所有节点类型 |
| 文档完善 | 🟢 低 | 使用文档和示例 |

---

## 🗺️ 完整复刻路线图

```
第一阶段: 扩展节点类型（核心功能）
    ├── 步骤1: 调研 Dify 所有节点类型
    ├── 步骤2: 定义节点 State 类
    ├── 步骤3: 更新 Parser 支持新节点
    └── 步骤4: 测试每种节点

第二阶段: 完善 SDK 功能
    ├── 步骤5: 增强 DifyGraph 功能
    ├── 步骤6: 支持条件分支和循环
    ├── 步骤7: 支持变量传递
    └── 步骤8: 支持高级配置

第三阶段: API 集成（可选）
    ├── 步骤9: 调研 Dify API
    ├── 步骤10: 实现 API 客户端
    ├── 步骤11: 实现自动部署
    └── 步骤12: 实现工作流管理

第四阶段: 文档和示例
    ├── 步骤13: 编写完整文档
    ├── 步骤14: 创建示例项目
    └── 步骤15: 制作教程视频
```

---

## 📝 详细步骤指南

## 第一阶段：扩展节点类型

### 步骤 1：调研 Dify 所有节点类型 ⏱️ 2小时

**目标：** 了解 Dify 平台支持的所有节点类型及其配置

**操作步骤：**

1. **访问 Dify 官方文档**
   ```
   https://docs.dify.ai/zh-hans/guides/workflow
   ```

2. **列出所有节点类型**
   
   创建文件 `docs/dify_node_types.md`，记录：

   | 节点类型 | 英文名 | 用途 | 重要参数 |
   |---------|--------|------|---------|
   | 开始 | start | 工作流入口 | variables |
   | LLM | llm | 调用大模型 | model, prompt_template |
   | 知识检索 | knowledge-retrieval | 查询知识库 | dataset_ids, query |
   | 结束 | end | 工作流出口 | outputs |
   | 代码执行 | code | 运行代码 | code, language |
   | HTTP 请求 | http-request | 调用 API | method, url, headers |
   | 模板转换 | template-transform | 转换文本 | template |
   | 问题分类 | question-classifier | 分类问题 | classes |
   | 条件分支 | if-else | 条件判断 | conditions |
   | 变量赋值 | variable-assigner | 设置变量 | variables |
   | 工具调用 | tool | 调用工具 | tool_name, parameters |
   | 参数提取 | parameter-extractor | 提取参数 | parameters |
   | 迭代 | iteration | 循环处理 | input_list |
   | ... | ... | ... | ... |

3. **导出示例 YAML**

   在 Dify 平台上创建包含各种节点的工作流，导出 YAML：
   ```bash
   mkdir -p playground/dify/samples
   # 保存导出的 YAML 文件到这个目录
   ```

---

### 步骤 2：定义节点 State 类 ⏱️ 4小时

**目标：** 为每种节点类型创建 Pydantic State 类

**操作步骤：**

1. **打开文件** `src/autoagents_graph/engine/dify/models/dify_types.py`

2. **添加新的节点 State 类**

   **示例：添加 Code 节点**

   ```python
   class DifyCodeState(BaseModel):
       """Dify代码执行节点状态"""
       code: str = ""  # 代码内容
       code_language: str = "python"  # 编程语言：python, javascript
       desc: str = ""
       outputs: Dict[str, Any] = Field(default_factory=dict)  # 输出变量
       selected: bool = False
       title: str = "代码执行"
       type: str = "code"
       variables: List = Field(default_factory=list)  # 输入变量
   ```

   **示例：添加 HTTP Request 节点**

   ```python
   class DifyHttpRequestState(BaseModel):
       """Dify HTTP请求节点状态"""
       api_base: str = ""  # 可选的API基础URL
       authorization: Dict[str, Any] = Field(default_factory=lambda: {
           "type": "no-auth"
       })
       body: Dict[str, Any] = Field(default_factory=dict)
       desc: str = ""
       headers: str = ""
       method: str = "get"  # get, post, put, delete, patch
       params: str = ""
       selected: bool = False
       timeout: int = 30
       title: str = "HTTP请求"
       type: str = "http-request"
       url: str = ""
   ```

   **示例：添加 If-Else 节点**

   ```python
   class DifyIfElseState(BaseModel):
       """Dify条件分支节点状态"""
       conditions: List[Dict[str, Any]] = Field(default_factory=list)
       desc: str = ""
       logical_operator: str = "and"  # and, or
       selected: bool = False
       title: str = "条件分支"
       type: str = "if-else"
   ```

3. **更新工厂字典**

   ```python
   DIFY_NODE_STATE_FACTORY = {
       "start": DifyStartState,
       "llm": DifyLLMState,
       "knowledge-retrieval": DifyKnowledgeRetrievalState,
       "end": DifyEndState,
       # 新增
       "code": DifyCodeState,
       "http-request": DifyHttpRequestState,
       "if-else": DifyIfElseState,
       "template-transform": DifyTemplateTransformState,
       "question-classifier": DifyQuestionClassifierState,
       "variable-assigner": DifyVariableAssignerState,
       "tool": DifyToolState,
       "parameter-extractor": DifyParameterExtractorState,
       "iteration": DifyIterationState,
   }
   ```

4. **验证数据结构**

   创建测试文件 `tests/test_dify_types.py`：
   
   ```python
   from autoagents_graph.engine.dify.models import DifyCodeState
   
   def test_code_state():
       state = DifyCodeState(
           code="print('hello')",
           code_language="python"
       )
       assert state.type == "code"
       assert state.code == "print('hello')"
   ```

---

### 步骤 3：更新 Parser 支持新节点 ⏱️ 3小时

**目标：** 让 DifyParser 能够识别和转换新节点类型

**操作步骤：**

1. **打开文件** `src/autoagents_graph/engine/dify/services/dify_parser.py`

2. **更新 `_extract_node_params` 方法**

   ```python
   @staticmethod
   def _extract_node_params(node_data: Dict[str, Any]) -> Dict[str, Any]:
       params = {}
       node_type = node_data.get("type", "")
       
       # 根据不同节点类型提取参数
       if node_type == "start":
           if "title" in node_data:
               params["title"] = node_data["title"]
           if "variables" in node_data:
               params["variables"] = node_data["variables"]
       
       elif node_type == "llm":
           # ... 现有代码 ...
       
       # 新增：code 节点
       elif node_type == "code":
           if "title" in node_data:
               params["title"] = node_data["title"]
           if "code" in node_data:
               params["code"] = node_data["code"]
           if "code_language" in node_data:
               params["code_language"] = node_data["code_language"]
           if "variables" in node_data:
               params["variables"] = node_data["variables"]
           if "outputs" in node_data:
               params["outputs"] = node_data["outputs"]
       
       # 新增：http-request 节点
       elif node_type == "http-request":
           if "title" in node_data:
               params["title"] = node_data["title"]
           if "method" in node_data:
               params["method"] = node_data["method"]
           if "url" in node_data:
               params["url"] = node_data["url"]
           if "headers" in node_data:
               params["headers"] = node_data["headers"]
           if "body" in node_data:
               params["body"] = node_data["body"]
       
       # 新增：if-else 节点
       elif node_type == "if-else":
           if "title" in node_data:
               params["title"] = node_data["title"]
           if "conditions" in node_data:
               params["conditions"] = node_data["conditions"]
           if "logical_operator" in node_data:
               params["logical_operator"] = node_data["logical_operator"]
       
       return params
   ```

3. **更新 `_get_state_class_name` 方法**

   ```python
   @staticmethod
   def _get_state_class_name(node_type: str) -> str:
       type_mapping = {
           "start": "DifyStartState",
           "llm": "DifyLLMState",
           "knowledge-retrieval": "DifyKnowledgeRetrievalState",
           "end": "DifyEndState",
           # 新增
           "code": "DifyCodeState",
           "http-request": "DifyHttpRequestState",
           "if-else": "DifyIfElseState",
           "template-transform": "DifyTemplateTransformState",
           "question-classifier": "DifyQuestionClassifierState",
           "variable-assigner": "DifyVariableAssignerState",
           "tool": "DifyToolState",
       }
       return type_mapping.get(node_type, None)
   ```

4. **更新生成的导入语句**

   在 `_generate_header_code` 方法中：

   ```python
   @staticmethod
   def _generate_header_code() -> List[str]:
       return [
           "from autoagents_graph import NL2Workflow, DifyConfig",
           "from autoagents_graph.engine.dify import (",
           "    DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState,",
           "    DifyEndState, DifyCodeState, DifyHttpRequestState,",
           "    DifyIfElseState, DifyTemplateTransformState,",
           "    DifyQuestionClassifierState, START, END",
           ")",
           "",
           # ...
       ]
   ```

---

### 步骤 4：测试每种节点 ⏱️ 2小时

**目标：** 确保每种节点都能正确转换

**操作步骤：**

1. **创建测试文件** `tests/test_all_dify_nodes.py`

   ```python
   import pytest
   from autoagents_graph import NL2Workflow, DifyConfig
   from autoagents_graph.engine.dify import (
       DifyStartState, DifyLLMState, DifyCodeState,
       DifyHttpRequestState, DifyIfElseState, START, END
   )
   
   
   def test_code_node():
       """测试代码执行节点"""
       workflow = NL2Workflow(
           platform="dify",
           config=DifyConfig(app_name="测试代码节点")
       )
       
       workflow.add_node(id=START, position={"x": 100, "y": 200}, state=DifyStartState())
       workflow.add_node(
           id="code_1",
           position={"x": 400, "y": 200},
           state=DifyCodeState(
               code="result = input_var * 2",
               code_language="python"
           )
       )
       workflow.add_node(id=END, position={"x": 700, "y": 200}, state=DifyEndState())
       
       workflow.add_edge(START, "code_1")
       workflow.add_edge("code_1", END)
       
       yaml_content = workflow.compile()
       assert "code" in yaml_content
       assert "python" in yaml_content
   
   
   def test_http_request_node():
       """测试HTTP请求节点"""
       workflow = NL2Workflow(
           platform="dify",
           config=DifyConfig(app_name="测试HTTP节点")
       )
       
       workflow.add_node(id=START, position={"x": 100, "y": 200}, state=DifyStartState())
       workflow.add_node(
           id="http_1",
           position={"x": 400, "y": 200},
           state=DifyHttpRequestState(
               method="post",
               url="https://api.example.com/data",
               headers='{"Content-Type": "application/json"}'
           )
       )
       workflow.add_node(id=END, position={"x": 700, "y": 200}, state=DifyEndState())
       
       workflow.add_edge(START, "http_1")
       workflow.add_edge("http_1", END)
       
       yaml_content = workflow.compile()
       assert "http-request" in yaml_content
       assert "https://api.example.com/data" in yaml_content
   
   
   def test_if_else_node():
       """测试条件分支节点"""
       workflow = NL2Workflow(
           platform="dify",
           config=DifyConfig(app_name="测试条件节点")
       )
       
       workflow.add_node(id=START, position={"x": 100, "y": 200}, state=DifyStartState())
       workflow.add_node(
           id="if_1",
           position={"x": 400, "y": 200},
           state=DifyIfElseState(
               conditions=[
                   {
                       "variable_selector": ["start", "sys_input"],
                       "comparison_operator": "contains",
                       "value": "hello"
                   }
               ],
               logical_operator="and"
           )
       )
       workflow.add_node(id=END, position={"x": 700, "y": 200}, state=DifyEndState())
       
       workflow.add_edge(START, "if_1")
       workflow.add_edge("if_1", END)
       
       yaml_content = workflow.compile()
       assert "if-else" in yaml_content
   ```

2. **运行测试**

   ```bash
   pytest tests/test_all_dify_nodes.py -v
   ```

---

## 第二阶段：完善 SDK 功能

### 步骤 5：增强 DifyGraph 功能 ⏱️ 3小时

**目标：** 添加更多实用方法

**操作步骤：**

1. **打开文件** `src/autoagents_graph/engine/dify/services/dify_graph.py`

2. **添加节点查找方法**

   ```python
   def find_node(self, node_id: str) -> Optional[DifyNode]:
       """根据ID查找节点"""
       return next((n for n in self.nodes if n.id == node_id), None)
   
   def find_nodes_by_type(self, node_type: str) -> List[DifyNode]:
       """根据类型查找所有节点"""
       return [n for n in self.nodes if n.data.get("type") == node_type]
   ```

3. **添加边查找方法**

   ```python
   def find_edges_from_node(self, node_id: str) -> List[DifyEdge]:
       """查找从指定节点出发的所有边"""
       return [e for e in self.edges if e.source == node_id]
   
   def find_edges_to_node(self, node_id: str) -> List[DifyEdge]:
       """查找指向指定节点的所有边"""
       return [e for e in self.edges if e.target == node_id]
   ```

4. **添加批量操作方法**

   ```python
   def add_nodes_batch(self, nodes_config: List[Dict]) -> List[DifyNode]:
       """批量添加节点"""
       created_nodes = []
       for config in nodes_config:
           node = self.add_node(**config)
           created_nodes.append(node)
       return created_nodes
   
   def add_edges_batch(self, edges_config: List[Dict]) -> List[DifyEdge]:
       """批量添加边"""
       created_edges = []
       for config in edges_config:
           edge = self.add_edge(**config)
           created_edges.append(edge)
       return created_edges
   ```

5. **添加验证方法**

   ```python
   def validate(self) -> Dict[str, Any]:
       """验证工作流的有效性"""
       errors = []
       warnings = []
       
       # 检查是否有START节点
       start_nodes = [n for n in self.nodes if n.data.get("type") == "start"]
       if not start_nodes:
           errors.append("工作流缺少START节点")
       elif len(start_nodes) > 1:
           errors.append(f"工作流有多个START节点: {len(start_nodes)}")
       
       # 检查是否有END节点
       end_nodes = [n for n in self.nodes if n.data.get("type") == "end"]
       if not end_nodes:
           warnings.append("工作流缺少END节点")
       
       # 检查孤立节点
       node_ids = {n.id for n in self.nodes}
       connected_nodes = set()
       for edge in self.edges:
           connected_nodes.add(edge.source)
           connected_nodes.add(edge.target)
       
       isolated_nodes = node_ids - connected_nodes
       if isolated_nodes:
           warnings.append(f"发现孤立节点: {isolated_nodes}")
       
       # 检查无效边
       for edge in self.edges:
           if edge.source not in node_ids:
               errors.append(f"边引用了不存在的源节点: {edge.source}")
           if edge.target not in node_ids:
               errors.append(f"边引用了不存在的目标节点: {edge.target}")
       
       return {
           "valid": len(errors) == 0,
           "errors": errors,
           "warnings": warnings
       }
   ```

---

### 步骤 6：支持条件分支和循环 ⏱️ 4小时

**目标：** 实现复杂的控制流

**操作步骤：**

1. **添加条件分支辅助方法**

   在 `dify_graph.py` 中：

   ```python
   def add_if_else_branch(self,
                          id: str,
                          position: Dict[str, float],
                          condition: Dict[str, Any],
                          true_branch_node: str,
                          false_branch_node: str) -> DifyNode:
       """
       添加条件分支
       
       Args:
           id: 节点ID
           position: 位置
           condition: 条件配置
           true_branch_node: 条件为真时的目标节点
           false_branch_node: 条件为假时的目标节点
       """
       # 创建if-else节点
       if_node = self.add_node(
           id=id,
           type="if-else",
           position=position,
           conditions=[condition]
       )
       
       # 添加true分支
       self.add_edge(id, true_branch_node, source_handle="true")
       
       # 添加false分支
       self.add_edge(id, false_branch_node, source_handle="false")
       
       return if_node
   ```

2. **添加循环辅助方法**

   ```python
   def add_iteration(self,
                     id: str,
                     position: Dict[str, float],
                     input_list_selector: List,
                     iteration_node: str) -> DifyNode:
       """
       添加迭代循环
       
       Args:
           id: 节点ID
           position: 位置
           input_list_selector: 输入列表选择器
           iteration_node: 循环体节点
       """
       # 创建iteration节点
       iter_node = self.add_node(
           id=id,
           type="iteration",
           position=position,
           input_list_selector=input_list_selector
       )
       
       # 连接到循环体
       self.add_edge(id, iteration_node, source_handle="iteration")
       
       return iter_node
   ```

---

### 步骤 7：支持变量传递 ⏱️ 2小时

**目标：** 正确处理节点间的变量引用

**操作步骤：**

1. **添加变量选择器辅助函数**

   创建文件 `src/autoagents_graph/engine/dify/utils/variable_helper.py`：

   ```python
   def create_variable_selector(node_id: str, variable_name: str) -> List:
       """
       创建变量选择器
       
       Args:
           node_id: 节点ID
           variable_name: 变量名
           
       Returns:
           变量选择器列表 [node_id, variable_name]
       """
       return [node_id, variable_name]
   
   
   def create_context_variable(variable_selectors: List[List]) -> Dict:
       """
       创建上下文变量配置
       
       Args:
           variable_selectors: 变量选择器列表
           
       Returns:
           上下文配置字典
       """
       return {
           "enabled": True,
           "variable_selector": variable_selectors
       }
   ```

2. **在节点中使用变量引用**

   ```python
   from autoagents_graph.engine.dify.utils import create_variable_selector
   
   # LLM节点引用start节点的输入
   workflow.add_node(
       id="llm_1",
       position={"x": 400, "y": 200},
       state=DifyLLMState(
           prompt_template=[{
               "role": "user",
               "text": "{{#start.sys_input#}}"  # 引用start节点的sys_input变量
           }]
       )
   )
   ```

---

### 步骤 8：支持高级配置 ⏱️ 2小时

**目标：** 支持环境变量、对话变量等高级功能

**操作步骤：**

1. **添加环境变量配置**

   在 `dify_graph.py` 中：

   ```python
   def add_environment_variable(self, name: str, value: Any, value_type: str = "string"):
       """添加环境变量"""
       env_var = {
           "id": str(uuid.uuid4()),
           "name": name,
           "value": value,
           "value_type": value_type
       }
       self.workflow.environment_variables.append(env_var)
   
   def add_conversation_variable(self, name: str, value_type: str = "string", 
                                 description: str = ""):
       """添加对话变量"""
       conv_var = {
           "id": str(uuid.uuid4()),
           "name": name,
           "value_type": value_type,
           "description": description
       }
       self.workflow.conversation_variables.append(conv_var)
   ```

2. **配置工作流特性**

   ```python
   def enable_file_upload(self, allowed_types: List[str] = ["image"]):
       """启用文件上传"""
       self.workflow.features["file_upload"]["enabled"] = True
       self.workflow.features["file_upload"]["allowed_file_types"] = allowed_types
   
   def set_opening_statement(self, statement: str):
       """设置开场白"""
       self.workflow.features["opening_statement"] = statement
   
   def add_suggested_question(self, question: str):
       """添加建议问题"""
       self.workflow.features["suggested_questions"].append(question)
   ```

---

## 第三阶段：API 集成（可选）

### 步骤 9：调研 Dify API ⏱️ 3小时

**目标：** 了解 Dify 的 API 接口

**操作步骤：**

1. **查阅 Dify API 文档**

   ```
   https://docs.dify.ai/zh-hans/guides/application-publishing/developing-with-apis
   ```

2. **测试 API 接口**

   使用 Postman 或 curl 测试：

   ```bash
   # 创建应用
   curl -X POST 'https://api.dify.ai/v1/apps' \
     -H 'Authorization: Bearer YOUR_API_KEY' \
     -H 'Content-Type: application/json' \
     -d '{
       "name": "测试应用",
       "mode": "workflow",
       "icon": "🤖"
     }'
   
   # 更新工作流
   curl -X PUT 'https://api.dify.ai/v1/apps/{app_id}/workflow' \
     -H 'Authorization: Bearer YOUR_API_KEY' \
     -H 'Content-Type: application/yaml' \
     --data-binary @workflow.yaml
   ```

3. **记录 API 端点**

   创建文件 `docs/dify_api_endpoints.md`

---

### 步骤 10：实现 API 客户端 ⏱️ 4小时

**目标：** 封装 Dify API 调用

**操作步骤：**

1. **创建 API 客户端文件**

   `src/autoagents_graph/engine/dify/api/dify_api.py`：

   ```python
   import requests
   from typing import Dict, Any, Optional
   
   
   class DifyAPIClient:
       """Dify API 客户端"""
       
       def __init__(self, api_key: str, base_url: str = "https://api.dify.ai"):
           self.api_key = api_key
           self.base_url = base_url
           self.headers = {
               "Authorization": f"Bearer {api_key}",
               "Content-Type": "application/json"
           }
       
       def create_app(self, name: str, mode: str = "workflow", 
                      icon: str = "🤖") -> Dict[str, Any]:
           """创建应用"""
           url = f"{self.base_url}/v1/apps"
           data = {
               "name": name,
               "mode": mode,
               "icon": icon
           }
           response = requests.post(url, json=data, headers=self.headers)
           response.raise_for_status()
           return response.json()
       
       def update_workflow(self, app_id: str, yaml_content: str) -> Dict[str, Any]:
           """更新工作流"""
           url = f"{self.base_url}/v1/apps/{app_id}/workflow"
           headers = self.headers.copy()
           headers["Content-Type"] = "application/yaml"
           
           response = requests.put(url, data=yaml_content, headers=headers)
           response.raise_for_status()
           return response.json()
       
       def get_app(self, app_id: str) -> Dict[str, Any]:
           """获取应用信息"""
           url = f"{self.base_url}/v1/apps/{app_id}"
           response = requests.get(url, headers=self.headers)
           response.raise_for_status()
           return response.json()
       
       def delete_app(self, app_id: str) -> Dict[str, Any]:
           """删除应用"""
           url = f"{self.base_url}/v1/apps/{app_id}"
           response = requests.delete(url, headers=self.headers)
           response.raise_for_status()
           return response.json()
   ```

---

### 步骤 11：实现自动部署 ⏱️ 3小时

**目标：** 实现一键部署到 Dify 平台

**操作步骤：**

1. **在 DifyGraph 中添加 deploy 方法**

   ```python
   def deploy(self, api_key: str, app_name: Optional[str] = None) -> Dict[str, Any]:
       """
       部署工作流到 Dify 平台
       
       Args:
           api_key: Dify API密钥
           app_name: 应用名称（可选）
           
       Returns:
           部署结果
       """
       from ..api.dify_api import DifyAPIClient
       
       # 验证工作流
       validation = self.validate()
       if not validation["valid"]:
           raise ValueError(f"工作流验证失败: {validation['errors']}")
       
       # 创建API客户端
       client = DifyAPIClient(api_key)
       
       # 创建应用
       app_result = client.create_app(
           name=app_name or self.app.name,
           mode="workflow",
           icon=self.app.icon
       )
       app_id = app_result["id"]
       
       # 上传工作流
       yaml_content = self.to_yaml()
       workflow_result = client.update_workflow(app_id, yaml_content)
       
       return {
           "app_id": app_id,
           "app_name": app_name or self.app.name,
           "workflow_result": workflow_result,
           "status": "success"
       }
   ```

2. **在 NL2Workflow 中支持部署**

   在 `nl2workflow.py` 中：

   ```python
   def deploy(self, **kwargs):
       """部署工作流"""
       if self.platform == "dify":
           return self.graph.deploy(**kwargs)
       else:
           raise NotImplementedError(f"{self.platform} 平台暂不支持直接部署")
   ```

---

### 步骤 12：实现工作流管理 ⏱️ 2小时

**目标：** 提供工作流的CRUD操作

**操作步骤：**

1. **创建工作流管理器**

   `src/autoagents_graph/engine/dify/api/workflow_manager.py`：

   ```python
   from typing import List, Dict, Any
   from .dify_api import DifyAPIClient
   from ..services.dify_graph import DifyGraph
   
   
   class DifyWorkflowManager:
       """Dify 工作流管理器"""
       
       def __init__(self, api_key: str):
           self.client = DifyAPIClient(api_key)
       
       def list_apps(self) -> List[Dict[str, Any]]:
           """列出所有应用"""
           return self.client.list_apps()
       
       def export_workflow(self, app_id: str, output_path: str):
           """导出工作流到文件"""
           app = self.client.get_app(app_id)
           yaml_content = app["workflow"]
           
           with open(output_path, 'w', encoding='utf-8') as f:
               f.write(yaml_content)
       
       def import_workflow(self, yaml_path: str, app_name: str) -> Dict[str, Any]:
           """从文件导入工作流"""
           with open(yaml_path, 'r', encoding='utf-8') as f:
               yaml_content = f.read()
           
           # 创建应用
           app_result = self.client.create_app(name=app_name)
           app_id = app_result["id"]
           
           # 上传工作流
           self.client.update_workflow(app_id, yaml_content)
           
           return {"app_id": app_id, "app_name": app_name}
       
       def clone_workflow(self, source_app_id: str, new_app_name: str) -> Dict[str, Any]:
           """克隆工作流"""
           # 获取源工作流
           source_app = self.client.get_app(source_app_id)
           yaml_content = source_app["workflow"]
           
           # 创建新应用
           return self.import_workflow(yaml_content, new_app_name)
   ```

---

## 第四阶段：文档和示例

### 步骤 13：编写完整文档 ⏱️ 4小时

**目标：** 提供详细的使用文档

**操作步骤：**

1. **创建快速开始文档**

   `docs/dify_quick_start.md`

2. **创建API参考文档**

   `docs/dify_api_reference.md`

3. **创建最佳实践文档**

   `docs/dify_best_practices.md`

---

### 步骤 14：创建示例项目 ⏱️ 3小时

**目标：** 提供实际可用的示例

**操作步骤：**

1. **创建基础示例**

   `examples/dify/01_basic_workflow.py`

2. **创建复杂示例**

   `examples/dify/02_advanced_workflow.py`

3. **创建实战项目**

   `examples/dify/03_customer_service_bot.py`

---

### 步骤 15：制作教程视频 ⏱️ 6小时

**目标：** 录制视频教程

**操作步骤：**

1. 录制入门教程
2. 录制进阶教程
3. 录制实战案例

---

## ⏰ 时间估算

| 阶段 | 总时长 | 说明 |
|------|--------|------|
| 第一阶段 | 11小时 | 核心功能，必须完成 |
| 第二阶段 | 11小时 | 增强功能，建议完成 |
| 第三阶段 | 12小时 | API集成，可选 |
| 第四阶段 | 13小时 | 文档示例，重要 |
| **总计** | **47小时** | 约 1 周工作量 |

---

## 🎯 优先级建议

### 🔴 高优先级（必须完成）

- ✅ 步骤 1-4: 扩展节点类型
- ✅ 步骤 5: 增强 DifyGraph 功能
- ✅ 步骤 13-14: 基础文档和示例

### 🟡 中优先级（建议完成）

- ⚠️ 步骤 6-7: 支持复杂控制流
- ⚠️ 步骤 8: 高级配置

### 🟢 低优先级（可选）

- 💡 步骤 9-12: API 集成（如果 Dify 提供了公开 API）
- 💡 步骤 15: 视频教程

---

## 📋 检查清单

完成每一步后，在这里打勾：

- [ ] 步骤 1: 调研节点类型
- [ ] 步骤 2: 定义 State 类
- [ ] 步骤 3: 更新 Parser
- [ ] 步骤 4: 测试所有节点
- [ ] 步骤 5: 增强图功能
- [ ] 步骤 6: 条件分支
- [ ] 步骤 7: 变量传递
- [ ] 步骤 8: 高级配置
- [ ] 步骤 9: 调研 API
- [ ] 步骤 10: API 客户端
- [ ] 步骤 11: 自动部署
- [ ] 步骤 12: 工作流管理
- [ ] 步骤 13: 编写文档
- [ ] 步骤 14: 创建示例
- [ ] 步骤 15: 制作视频

---

## 🚀 开始行动

建议按照以下顺序执行：

1. **Week 1 (第一阶段)**: 扩展所有节点类型
2. **Week 2 (第二阶段)**: 完善 SDK 功能
3. **Week 3 (第三阶段)**: API 集成（可选）
4. **Week 4 (第四阶段)**: 文档和示例

祝你复刻成功！🎉

