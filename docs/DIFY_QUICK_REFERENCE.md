# 🚀 Dify 复刻快速参考卡片

> 本文档是复刻 Dify 平台自动生成 Agent 的速查手册

---

## 📦 添加新节点类型的完整流程

### 1️⃣ 定义 State 类 (5分钟)

**文件:** `src/autoagents_graph/engine/dify/models/dify_types.py`

```python
class Dify新节点State(BaseModel):
    """节点描述"""
    # 必需字段
    type: str = "节点类型名"
    title: str = "显示名称"
    desc: str = ""
    selected: bool = False
    
    # 自定义字段
    your_field: str = ""
    your_config: Dict = Field(default_factory=dict)
```

### 2️⃣ 注册到工厂 (1分钟)

**文件:** `src/autoagents_graph/engine/dify/models/dify_types.py`

```python
DIFY_NODE_STATE_FACTORY = {
    # 已有节点...
    "新节点类型名": Dify新节点State,
}
```

### 3️⃣ 更新 Parser (3分钟)

**文件:** `src/autoagents_graph/engine/dify/services/dify_parser.py`

```python
# 在 _extract_node_params 方法中添加
elif node_type == "新节点类型名":
    if "title" in node_data:
        params["title"] = node_data["title"]
    if "your_field" in node_data:
        params["your_field"] = node_data["your_field"]

# 在 _get_state_class_name 方法中添加
type_mapping = {
    # 已有映射...
    "新节点类型名": "Dify新节点State",
}
```

### 4️⃣ 更新导入语句 (1分钟)

**文件:** `src/autoagents_graph/engine/dify/services/dify_parser.py`

```python
def _generate_header_code() -> List[str]:
    return [
        "from autoagents_graph import NL2Workflow, DifyConfig",
        "from autoagents_graph.engine.dify import (",
        "    DifyStartState, ..., Dify新节点State,",  # 添加这里
        "    START, END",
        ")",
    ]
```

### 5️⃣ 导出新类 (1分钟)

**文件:** `src/autoagents_graph/engine/dify/__init__.py`

```python
from .models.dify_types import (
    # 已有导出...
    Dify新节点State,
)

__all__ = [
    # 已有列表...
    "Dify新节点State",
]
```

### 6️⃣ 编写测试 (5分钟)

**文件:** `tests/test_新节点.py`

```python
def test_新节点():
    workflow = NL2Workflow(platform="dify", config=DifyConfig())
    
    workflow.add_node(
        id="test_node",
        state=Dify新节点State(your_field="value"),
        position={"x": 100, "y": 200}
    )
    
    yaml = workflow.compile()
    assert "新节点类型名" in yaml
```

### 7️⃣ 运行测试 (1分钟)

```bash
pytest tests/test_新节点.py -v
```

**总计时间: ~17分钟/节点**

---

## 📊 目前已实现 vs 需要实现

### ✅ 已实现 (4个)

| 节点类型 | State类 | Parser支持 | 测试 |
|---------|---------|-----------|------|
| start | DifyStartState | ✅ | ✅ |
| llm | DifyLLMState | ✅ | ✅ |
| knowledge-retrieval | DifyKnowledgeRetrievalState | ✅ | ✅ |
| end | DifyEndState | ✅ | ✅ |

### ❌ 需要实现 (15个)

| 优先级 | 节点类型 | 说明 | 预计时间 |
|-------|---------|------|---------|
| 🔴 P0 | code | 代码执行 | 20分钟 |
| 🔴 P0 | http-request | HTTP请求 | 20分钟 |
| 🔴 P0 | if-else | 条件分支 | 25分钟 |
| 🔴 P0 | template-transform | 模板转换 | 20分钟 |
| 🟡 P1 | question-classifier | 问题分类 | 25分钟 |
| 🟡 P1 | variable-assigner | 变量赋值 | 20分钟 |
| 🟡 P1 | parameter-extractor | 参数提取 | 25分钟 |
| 🟡 P1 | iteration | 迭代循环 | 30分钟 |
| 🟢 P2 | tool | 工具调用 | 25分钟 |
| 🟢 P2 | document-extractor | 文档提取 | 25分钟 |
| 🟢 P2 | list-filter | 列表过滤 | 20分钟 |
| 🟢 P2 | variable-aggregator | 变量聚合 | 25分钟 |
| 🟢 P2 | answer | 直接回复 | 20分钟 |
| 🟢 P2 | assigner | 分配器 | 20分钟 |
| 🟢 P2 | conversation-variable | 对话变量 | 20分钟 |

**总计:** P0需要 1.5小时，P1需要 1.7小时，P2需要 2.7小时，全部需要 **5.9小时**

---

## 🎯 最小可用版本 (MVP)

要实现基本可用的 Dify SDK，至少需要完成：

```
✅ start (已完成)
✅ llm (已完成)
✅ end (已完成)
❌ code (代码执行 - 必需)
❌ http-request (API调用 - 必需)
❌ if-else (条件判断 - 必需)
❌ template-transform (文本处理 - 必需)
```

**MVP 时间估算:** 1.5小时

---

## 📝 代码模板

### State 类模板

```python
class Dify{NodeName}State(BaseModel):
    """Dify {中文名} 节点状态"""
    # 基础字段（必需）
    desc: str = ""
    selected: bool = False
    title: str = "{默认标题}"
    type: str = "{node-type}"
    
    # 自定义字段
    field1: str = ""
    field2: int = 0
    field3: List = Field(default_factory=list)
    field4: Dict[str, Any] = Field(default_factory=dict)
    
    # 如果有子对象
    config: Dict[str, Any] = Field(default_factory=lambda: {
        "key1": "value1",
        "key2": "value2"
    })
```

### Parser 提取参数模板

```python
elif node_type == "{node-type}":
    # 提取title
    if "title" in node_data:
        params["title"] = node_data["title"]
    
    # 提取自定义字段
    for field in ["field1", "field2", "field3", "field4"]:
        if field in node_data:
            params[field] = node_data[field]
    
    # 提取嵌套配置
    if "config" in node_data:
        params["config"] = node_data["config"]
```

### 测试用例模板

```python
def test_{node_type}_node():
    """测试 {中文名} 节点"""
    workflow = NL2Workflow(
        platform="dify",
        config=DifyConfig(app_name="测试{中文名}节点")
    )
    
    # 添加节点
    workflow.add_node(id=START, position={"x": 100, "y": 200}, state=DifyStartState())
    workflow.add_node(
        id="{node_id}",
        position={"x": 400, "y": 200},
        state=Dify{NodeName}State(
            field1="value1",
            field2=123
        )
    )
    workflow.add_node(id=END, position={"x": 700, "y": 200}, state=DifyEndState())
    
    # 添加连线
    workflow.add_edge(START, "{node_id}")
    workflow.add_edge("{node_id}", END)
    
    # 生成YAML
    yaml_content = workflow.compile()
    
    # 断言
    assert "{node-type}" in yaml_content
    assert "value1" in yaml_content
    
    # 测试Parser
    parser = DifyParser()
    code = parser.from_yaml_to_code(yaml_content)
    assert "Dify{NodeName}State" in code
```

---

## 🔧 常见问题

### Q1: 如何找到节点的所有字段？

**A:** 三种方法：
1. 在 Dify 平台创建节点，导出 YAML 查看
2. 查看 Dify 官方文档
3. 参考 Dify 源码 (GitHub)

### Q2: 字段的默认值怎么设置？

**A:** 参考 Dify 导出的 YAML：
```yaml
nodes:
  - data:
      type: code
      code: ""  # 空字符串
      timeout: 30  # 数字
      enabled: false  # 布尔值
      config: {}  # 空字典
      items: []  # 空列表
```

### Q3: 如何处理复杂的嵌套配置？

**A:** 使用 `Field(default_factory=lambda: {...})`：
```python
complex_config: Dict[str, Any] = Field(default_factory=lambda: {
    "level1": {
        "level2": {
            "level3": "value"
        }
    }
})
```

### Q4: Parser 提取参数时要注意什么？

**A:** 三个原则：
1. 只提取 **用户配置** 的字段，不提取系统字段
2. 跳过 **默认值**（减少代码冗余）
3. 保持与 State 类字段名 **一致**

### Q5: 如何验证实现是否正确？

**A:** 完整测试流程：
```python
# 1. SDK → YAML
workflow = NL2Workflow(...)
yaml1 = workflow.compile()

# 2. YAML → SDK
parser = DifyParser()
code = parser.from_yaml_to_code(yaml1)

# 3. 执行生成的SDK代码 → YAML
exec(code)  # 这会创建新的workflow
yaml2 = workflow.compile()

# 4. 对比两个YAML（应该基本一致）
assert yaml1 == yaml2  # 或使用 diff 工具
```

---

## 📦 文件结构

```
src/autoagents_graph/engine/dify/
├── __init__.py              # 导出所有公开类
├── models/
│   ├── __init__.py
│   └── dify_types.py        # ← 在这里定义 State 类
├── services/
│   ├── __init__.py
│   ├── dify_graph.py        # DifyGraph 构建器
│   └── dify_parser.py       # ← 在这里更新 Parser
└── api/
    └── dify_api.py          # API 客户端（可选）

tests/
└── test_dify_nodes.py       # ← 在这里编写测试

playground/dify/
├── examples/
│   └── step_by_step_example.py  # 示例代码
└── outputs/
    └── *.yaml               # 生成的文件
```

---

## ✅ 每日检查清单

开始工作前：
- [ ] 拉取最新代码 `git pull`
- [ ] 激活虚拟环境
- [ ] 运行现有测试确保通过

添加新节点：
- [ ] 在 Dify 平台测试节点功能
- [ ] 导出包含该节点的 YAML
- [ ] 定义 State 类
- [ ] 注册到工厂
- [ ] 更新 Parser
- [ ] 更新导入
- [ ] 编写测试
- [ ] 运行测试通过
- [ ] 提交代码

结束工作：
- [ ] 运行所有测试
- [ ] 更新文档
- [ ] 提交代码 `git commit`
- [ ] 推送代码 `git push`

---

## 🎓 学习资源

1. **Dify 官方文档**
   - 英文: https://docs.dify.ai/
   - 中文: https://docs.dify.ai/zh-hans/

2. **Dify GitHub**
   - https://github.com/langgenius/dify

3. **Pydantic 文档**
   - https://docs.pydantic.dev/

4. **本项目文档**
   - 详细指南: `docs/DIFY_REPLICATION_GUIDE.md`
   - 快速参考: `docs/DIFY_QUICK_REFERENCE.md` (本文档)

---

## 💬 获取帮助

1. 查看示例代码: `playground/dify/examples/`
2. 参考现有实现: `src/autoagents_graph/engine/agentify/`
3. 运行测试查看用法: `tests/`
4. 查看完整指南: `docs/DIFY_REPLICATION_GUIDE.md`

---

**最后更新:** 2025-01-XX
**作者:** AutoAgents Team
**版本:** v1.0

