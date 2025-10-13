# 📅 Dify 复刻执行计划表

> 这是一个详细的执行计划，包含时间安排、优先级和检查点

---

## 🗓️ 时间线总览

```
Week 1: 核心节点类型 (必须完成)
  Day 1-2: P0节点 (code, http-request)
  Day 3-4: P0节点 (if-else, template-transform)
  Day 5: 测试和修复

Week 2: 增强功能 (建议完成)
  Day 1-2: P1节点 (question-classifier, variable-assigner)
  Day 3: P1节点 (parameter-extractor, iteration)
  Day 4-5: 图功能增强

Week 3: API集成 (可选)
  Day 1-2: 调研Dify API
  Day 3-4: 实现API客户端
  Day 5: 自动部署功能

Week 4: 文档和示例
  Day 1-2: 编写文档
  Day 3-4: 创建示例
  Day 5: 整理和发布
```

---

## 📋 第一天详细计划

### 🌅 上午 (9:00 - 12:00)

#### 任务 1: 添加 Code 节点 ⏱️ 1.5小时

**9:00 - 9:30 | 调研和设计**
- [ ] 在 Dify 平台创建包含 Code 节点的工作流
- [ ] 导出 YAML，分析字段结构
- [ ] 设计 DifyCodeState 类

**9:30 - 10:00 | 实现 State 类**
```python
# 文件: src/autoagents_graph/engine/dify/models/dify_types.py

class DifyCodeState(BaseModel):
    """Dify代码执行节点状态"""
    code: str = ""
    code_language: str = "python"
    desc: str = ""
    outputs: Dict[str, Any] = Field(default_factory=dict)
    selected: bool = False
    title: str = "代码执行"
    type: str = "code"
    variables: List = Field(default_factory=list)

# 更新工厂
DIFY_NODE_STATE_FACTORY["code"] = DifyCodeState
```

**10:00 - 10:30 | 更新 Parser**
```python
# 文件: src/autoagents_graph/engine/dify/services/dify_parser.py

# 在 _extract_node_params 中添加
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

# 在 _get_state_class_name 中添加
"code": "DifyCodeState",
```

**10:30 - 11:00 | 更新导入和导出**
```python
# 文件: src/autoagents_graph/engine/dify/__init__.py
from .models.dify_types import DifyCodeState

__all__ = [..., "DifyCodeState"]

# 文件: src/autoagents_graph/engine/dify/services/dify_parser.py
# 在 _generate_header_code 中添加
"    DifyCodeState,"
```

**11:00 - 11:30 | 编写测试**
```python
# 文件: tests/test_dify_code_node.py

def test_code_node_creation():
    """测试代码节点创建"""
    workflow = NL2Workflow(platform="dify", config=DifyConfig())
    
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

def test_code_node_parser():
    """测试Parser能正确解析Code节点"""
    # ... 测试代码
```

**11:30 - 12:00 | 运行测试和修复**
```bash
pytest tests/test_dify_code_node.py -v
```
- [ ] 所有测试通过
- [ ] 提交代码

---

### 🌆 下午 (14:00 - 18:00)

#### 任务 2: 添加 HTTP Request 节点 ⏱️ 1.5小时

**14:00 - 14:30 | 调研和设计**
- [ ] 在 Dify 平台测试 HTTP Request 节点
- [ ] 导出 YAML，分析字段
- [ ] 设计 DifyHttpRequestState 类

**14:30 - 15:00 | 实现 State 类**
```python
class DifyHttpRequestState(BaseModel):
    """Dify HTTP请求节点状态"""
    authorization: Dict[str, Any] = Field(default_factory=lambda: {"type": "no-auth"})
    body: Dict[str, Any] = Field(default_factory=dict)
    desc: str = ""
    headers: str = ""
    method: str = "get"
    params: str = ""
    selected: bool = False
    timeout: int = 30
    title: str = "HTTP请求"
    type: str = "http-request"
    url: str = ""
```

**15:00 - 15:30 | 更新 Parser**
- [ ] 添加参数提取逻辑
- [ ] 添加类型映射
- [ ] 更新导入语句

**15:30 - 16:00 | 编写测试**
- [ ] 测试节点创建
- [ ] 测试不同HTTP方法
- [ ] 测试Parser反向生成

**16:00 - 16:30 | 运行测试**
- [ ] 测试通过
- [ ] 提交代码

**16:30 - 18:00 | 文档和示例**
- [ ] 更新 README
- [ ] 编写使用示例
- [ ] 创建完整示例工作流

---

### 🌙 晚上 (可选，19:00 - 21:00)

#### 任务 3: 回顾和总结

**19:00 - 20:00 | 代码审查**
- [ ] 检查代码风格
- [ ] 运行所有测试
- [ ] 检查测试覆盖率

**20:00 - 21:00 | 文档更新**
- [ ] 更新进度
- [ ] 记录遇到的问题
- [ ] 准备明天的任务

---

## 📊 进度跟踪表

### Week 1: 核心节点类型

| 日期 | 节点类型 | 状态 | 完成时间 | 备注 |
|------|---------|------|---------|------|
| Day 1 上午 | code | ⬜ | - | |
| Day 1 下午 | http-request | ⬜ | - | |
| Day 2 上午 | if-else | ⬜ | - | |
| Day 2 下午 | template-transform | ⬜ | - | |
| Day 3 上午 | question-classifier | ⬜ | - | |
| Day 3 下午 | variable-assigner | ⬜ | - | |
| Day 4 上午 | parameter-extractor | ⬜ | - | |
| Day 4 下午 | iteration | ⬜ | - | |
| Day 5 | 测试和修复 | ⬜ | - | |

**图例:**
- ⬜ 未开始
- 🟡 进行中
- ✅ 已完成
- ❌ 有问题

---

## 🎯 每日目标

### Day 1
- ✅ 完成 Code 节点
- ✅ 完成 HTTP Request 节点
- ✅ 所有测试通过

### Day 2
- ✅ 完成 If-Else 节点
- ✅ 完成 Template Transform 节点
- ✅ 所有测试通过

### Day 3
- ✅ 完成 Question Classifier 节点
- ✅ 完成 Variable Assigner 节点
- ✅ 所有测试通过

### Day 4
- ✅ 完成 Parameter Extractor 节点
- ✅ 完成 Iteration 节点
- ✅ 所有测试通过

### Day 5
- ✅ 运行完整测试套件
- ✅ 修复所有发现的问题
- ✅ 代码审查
- ✅ 文档更新

---

## 🔍 质量检查点

### 每个节点完成后

- [ ] State 类定义正确
- [ ] 所有字段都有合适的类型注解
- [ ] 默认值设置合理
- [ ] 注册到工厂字典
- [ ] Parser 能正确提取参数
- [ ] Parser 能生成正确的导入语句
- [ ] 编写了完整的测试
- [ ] 测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 代码符合风格规范
- [ ] 有文档注释

### 每天结束前

- [ ] 所有当天的测试通过
- [ ] 代码已提交到 Git
- [ ] 更新了进度表
- [ ] 记录了遇到的问题
- [ ] 准备了明天的任务清单

### 每周结束前

- [ ] 所有测试通过
- [ ] 代码审查完成
- [ ] 文档更新
- [ ] 性能测试
- [ ] 创建了示例
- [ ] 准备了周报

---

## 📝 问题追踪

### 遇到问题时的处理流程

1. **记录问题**
   ```markdown
   ## 问题 #1: 标题
   
   **日期:** 2025-01-XX
   **节点:** code
   **描述:** 详细描述问题
   **复现步骤:**
   1. 步骤1
   2. 步骤2
   
   **解决方案:** 如何解决的
   **状态:** ⬜ 未解决 / ✅ 已解决
   ```

2. **查找类似问题**
   - 搜索现有的 Issue
   - 查看 agentify 的实现
   - 查看 Dify 文档

3. **尝试解决**
   - 编写最小复现代码
   - 逐步调试
   - 添加日志输出

4. **寻求帮助**
   - 提问前整理好问题
   - 提供完整的上下文
   - 附上错误信息

---

## 🎓 学习计划

### 第一周学习目标

- [ ] 理解 Pydantic 的 Field 用法
- [ ] 掌握 YAML 格式
- [ ] 熟悉 Dify 节点结构
- [ ] 学会编写单元测试

### 推荐学习资源

1. **Pydantic 快速入门** (1小时)
   - https://docs.pydantic.dev/latest/concepts/models/

2. **YAML 语法** (30分钟)
   - https://yaml.org/spec/1.2/spec.html

3. **pytest 教程** (1小时)
   - https://docs.pytest.org/en/stable/

---

## 🚀 快速开始命令

### 环境设置
```bash
# 克隆项目
git clone https://github.com/your-repo/AutoAgents-Graph-Python.git
cd AutoAgents-Graph-Python

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/ -v
```

### 开始开发
```bash
# 创建新分支
git checkout -b feature/dify-code-node

# 编辑文件
code src/autoagents_graph/engine/dify/models/dify_types.py

# 运行测试
pytest tests/test_dify_code_node.py -v

# 提交代码
git add .
git commit -m "feat: add Dify Code node support"
git push origin feature/dify-code-node
```

### 常用命令
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_dify_nodes.py::test_code_node -v

# 查看测试覆盖率
pytest --cov=src/autoagents_graph/engine/dify tests/

# 格式化代码
black src/
isort src/

# 类型检查
mypy src/autoagents_graph/engine/dify/
```

---

## 📞 联系方式

如果遇到问题，可以通过以下方式获取帮助：

1. **查看文档**
   - 完整指南: `docs/DIFY_REPLICATION_GUIDE.md`
   - 快速参考: `docs/DIFY_QUICK_REFERENCE.md`
   - 执行计划: `docs/DIFY_EXECUTION_PLAN.md` (本文档)

2. **查看示例**
   - `playground/dify/examples/`
   - `tests/`

3. **参考实现**
   - Agentify 的实现: `src/autoagents_graph/engine/agentify/`

---

**祝你复刻成功！🎉**

记住：**一次只做一个节点，做好一个再做下一个。**

慢慢来，比较快！💪

