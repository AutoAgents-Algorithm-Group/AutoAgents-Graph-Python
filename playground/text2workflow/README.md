# Text2Workflow 测试

这个目录包含Text2Workflow跨平台转换器的测试示例。

## 文件说明

- `test_text2workflow.py` - 简洁的Text2Workflow测试脚本
- `test_dify_output.yaml` - Dify平台生成的工作流配置
- `test_agentify_output.json` - Agentify平台生成的工作流配置

## 运行测试

```bash
cd playground/text2workflow
python test_text2workflow.py
```

测试会同时演示：
- Dify平台工作流构建和YAML生成
- Agentify平台工作流构建和JSON生成
