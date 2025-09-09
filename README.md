<div align="center">

# Hades - AI工作流构建引擎
*以冥界之王的名义，掌控你的AI工作流*

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0+-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![AI](https://img.shields.io/badge/AI-Workflow-FF6B6B?style=for-the-badge&logo=robot&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

![Dify](https://img.shields.io/badge/Platform-Dify-4285F4?style=flat-square&logo=google&logoColor=white)
![Agentify](https://img.shields.io/badge/Platform-Agentify-FF4081?style=flat-square&logo=android&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)

---

</div>

**Hades** 是一个强大的AI工作流构建引擎，提供统一的API来创建和管理智能体工作流。支持多个主流AI平台，包括Dify和Agentify，让你可以用同一套代码在不同平台间无缝切换。

## ✨ 核心特性

- 🎯 **统一API** - 一套代码，多平台部署
- 🔒 **类型安全** - 基于Pydantic的完整类型验证
- 🌉 **平台兼容** - 支持Dify、Agentify等主流平台
- 🤖 **智能转换** - 节点类型自动识别和转换
- 📦 **模块化设计** - 清晰的架构，易于扩展

## 📁 项目结构

```
Hades/
├── src/                        # 核心源代码
│   ├── agentify/              # AI工作流引擎核心
│   │   ├── api/               # API接口层
│   │   ├── types/             # 类型定义
│   │   ├── AutoWorkFlow.py    # 自动工作流生成
│   │   ├── FlowGraph.py       # 工作流图构建器
│   │   ├── FlowInterpreter.py # 工作流解释器
│   │   ├── NodeRegistry.py    # 节点注册表
│   │   └── Utils.py           # 工具函数
│   ├── dify/                  # Dify平台适配器
│   │   ├── DifyGraph.py       # Dify工作流构建器
│   │   └── DifyTypes.py       # Dify数据类型
│   └── Text2Workflow.py       # 跨平台工作流转换器
├── playground/                 # 示例和测试
│   ├── agentify/              # Agentify平台示例
│   └── dify/                  # Dify平台示例
├── requirements.txt           # 依赖管理
├── pyproject.toml            # 项目配置
└── README.md                 # 项目文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd Hades
pip install -r requirements.txt
```

### 2. 基本使用

Hades提供三种主要使用方式：

#### Text2Workflow - 跨平台转换器
统一的API接口，支持Dify和Agentify平台的工作流构建和转换。

#### FlowGraph - Agentify原生构建器  
专为Agentify平台设计的原生工作流构建器，提供完整的节点和连接管理。

#### AutoWorkFlow - 自动工作流生成
基于自然语言描述自动生成工作流结构。

### 3. 运行示例

```bash
# 测试Agentify平台功能
cd playground/agentify
python test_autoworkflow.py
python test_text2workflow.py

# 测试Dify平台集成
cd playground/dify
python test_dify.py
```

## 🎯 支持的节点类型

### Agentify平台节点
- **QuestionInputState** - 用户输入节点
- **AiChatState** - AI对话节点
- **ConfirmReplyState** - 确认回复节点
- **KnowledgeSearchState** - 知识库搜索节点
- **Pdf2MdState** - PDF文档解析节点
- **InfoClassState** - 信息分类节点
- **CodeFragmentState** - 代码执行节点
- **ForEachState** - 循环执行节点
- **AddMemoryVariableState** - 内存变量节点

### Dify平台节点
- **DifyStartNodeData** - 开始节点
- **DifyLLMNodeData** - LLM节点
- **DifyKnowledgeRetrievalNodeData** - 知识检索节点
- **DifyEndNodeData** - 结束节点

### 自动转换支持
Hades支持Agentify节点自动转换为Dify格式：
- `AiChatState` → `DifyLLMNodeData`
- `KnowledgeSearchState` → `DifyKnowledgeRetrievalNodeData`
- `ConfirmReplyState` → `DifyEndNodeData`

## 🔧 核心功能

### Text2Workflow API
跨平台工作流转换器，提供统一的节点添加、连接和编译接口。支持Dify和Agentify平台的无缝切换。

### FlowGraph API
Agentify平台原生工作流构建器，提供完整的节点状态管理和工作流编译功能。

### 自动工作流生成
使用自然语言描述生成工作流结构，简化工作流创建过程。

### 工作流解释器
从JSON配置生成可执行的SDK代码，支持工作流的逆向工程。

## 📖 API参考

### 主要模块

- **Text2Workflow** - 跨平台工作流转换器
- **FlowGraph** - Agentify平台工作流构建器
- **AutoWorkFlow** - 自动工作流生成器
- **FlowInterpreter** - 工作流解释器

### 平台支持

- **Dify平台**: 生成标准YAML配置文件
- **Agentify平台**: 直接发布到平台或生成JSON配置

### 节点管理

- 统一的节点添加接口
- 自动类型识别和转换
- 智能连接验证
- 位置坐标管理

## 🛠️ 开发环境

### 系统要求
- **Python**: 3.8+
- **操作系统**: Windows/macOS/Linux

### 核心依赖
- **pydantic**: 数据验证和类型定义
- **requests**: HTTP请求和API调用
- **PyYAML**: YAML文件处理和生成

### 开发工具
- 支持类型提示的IDE (推荐VSCode、PyCharm)
- Git版本控制
- Python虚拟环境

## 📋 配置说明

### Agentify平台配置
需要提供认证凭据：
- `personal_auth_key`: 个人认证密钥
- `personal_auth_secret`: 个人认证密钥
- `base_url`: 平台地址 (默认: https://uat.agentspro.cn)

### Dify平台配置
需要提供应用信息：
- `app_name`: 应用名称
- `app_description`: 应用描述
- `app_icon`: 应用图标

### 模型配置
默认使用 `doubao-deepseek-v3` 模型，可根据平台支持情况调整：
- 温度参数: 0.1-1.0
- 最大令牌数: 100-4000
- 流式输出: 支持

## 🎨 最佳实践

### 工作流设计
- 合理规划节点位置坐标
- 使用描述性的节点ID
- 设置适当的模型参数
- 考虑用户交互体验

### 平台选择
- **Dify**: 适合复杂的企业级应用
- **Agentify**: 适合快速原型和轻量级应用

### 性能优化
- 合理设置AI模型参数
- 优化知识库检索配置
- 控制工作流复杂度
- 监控API调用频率

## 🧪 测试

### 单元测试
```bash
cd playground/agentify
python test_autoworkflow.py      # 测试自动工作流生成
python test_text2workflow.py     # 测试跨平台转换
python test_flowinterpreter.py   # 测试工作流解释
```

### 集成测试
```bash
cd playground/dify
python test_dify.py              # 测试Dify平台集成
```

### 功能测试
```bash
cd playground/agentify
python test_codeFragment.py      # 测试代码执行节点
python test_forEach.py           # 测试循环执行节点
python test_new_infoclass.py     # 测试信息分类节点
```

## 📚 学习资源

### 文档
- API参考文档
- 节点类型说明
- 平台集成指南
- 最佳实践指南

### 示例
- 基础工作流示例
- 复杂场景示例
- 平台迁移示例
- 自定义节点示例

## 🚀 路线图

### 当前版本 (v1.0)
- ✅ 核心工作流引擎
- ✅ Dify和Agentify平台支持
- ✅ 跨平台转换器
- ✅ 基础节点类型

### 下一版本 (v1.1)
- 🔄 更多平台支持
- 🔄 高级节点类型
- 🔄 可视化工作流编辑器
- 🔄 性能优化

### 未来计划
- 📅 云端工作流管理
- 📅 协作式工作流开发
- 📅 AI驱动的工作流优化
- 📅 企业级安全特性

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下步骤：

1. Fork项目仓库
2. 创建功能分支
3. 提交代码更改
4. 创建Pull Request
5. 等待代码审查

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发
- 📝 文档改进
- 🧪 测试用例
- 🎨 UI/UX改进

## 📞 支持

### 问题反馈
- GitHub Issues
- 邮件支持
- 社区论坛

### 商业支持
- 企业级技术支持
- 定制化开发服务
- 培训和咨询

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

---

<div align="center">

⚡ **Hades** ⚡

*让AI工作流构建变得简单而强大*

![Hades](https://img.shields.io/badge/⚡-Hades-000000?style=for-the-badge&logo=crown&logoColor=gold)

</div>