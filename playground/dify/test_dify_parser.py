import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph import NL2Workflow, DifyConfig
from src.autoagents_graph.engine.dify import DifyParser
from src.autoagents_graph.engine.dify import (
    DifyStartState, DifyLLMState, DifyEndState, START, END
)


def test_from_yaml_file():
    """测试从YAML文件生成代码"""
    print("=" * 60)
    print("测试1: 从YAML文件生成代码")
    print("=" * 60)
    
    parser = DifyParser()
    
    # 假设你有一个从Dify平台导出的YAML文件
    yaml_file = "playground/dify/outputs/dify_workflow_output.yaml"
    
    if os.path.exists(yaml_file):
        # 生成代码
        generated_code = parser.from_yaml_file(
            yaml_file_path=yaml_file,
            output_path="playground/dify/outputs/generated_from_yaml.py"
        )
        
        print("生成的代码预览:")
        print("-" * 60)
        print(generated_code[:500] + "...")
        print("-" * 60)
        print("✅ 代码已生成并保存")
    else:
        print(f"⚠️  文件不存在: {yaml_file}")
        print("请先运行 test_dify.py 生成示例YAML文件")


def test_from_yaml_string():
    """测试从YAML字符串生成代码"""
    print("\n" + "=" * 60)
    print("测试2: 从YAML字符串生成代码")
    print("=" * 60)
    
    parser = DifyParser()
    
    # 示例YAML内容 (简化版)
    yaml_content = """
app:
  description: 测试工作流
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: workflow
  name: Dify测试工作流
  use_icon_as_answer_icon: false
kind: app
version: 0.3.1
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    edges:
    - id: start-source-llm_analysis-target
      source: start
      target: llm_analysis
      sourceHandle: source
      targetHandle: target
      type: custom
      data: {}
      zIndex: 0
    - id: llm_analysis-source-end-target
      source: llm_analysis
      target: end
      sourceHandle: source
      targetHandle: target
      type: custom
      data: {}
      zIndex: 0
    nodes:
    - id: start
      type: custom
      position:
        x: 50
        y: 200
      data:
        desc: ''
        selected: false
        title: 开始
        type: start
        variables:
        - label: 系统输入
          max_length: 48000
          options: []
          required: true
          type: text-input
          variable: sys_input
    - id: llm_analysis
      type: custom
      position:
        x: 300
        y: 200
      data:
        desc: ''
        model:
          completion_params:
            temperature: 0.7
          mode: chat
          name: doubao-deepseek-v3
          provider: ''
        prompt_template:
        - role: system
          text: 你是一个专业的AI助手
        selected: false
        title: 智能分析
        type: llm
    - id: end
      type: custom
      position:
        x: 550
        y: 200
      data:
        desc: ''
        outputs: []
        selected: false
        title: 结束
        type: end
    viewport:
      x: 0
      y: 0
      zoom: 1.0
"""
    
    # 生成代码
    generated_code = parser.from_yaml_to_code(
        yaml_content=yaml_content,
        output_path="playground/dify/outputs/generated_from_string.py"
    )
    
    print("生成的代码:")
    print("-" * 60)
    print(generated_code)
    print("-" * 60)
    print("✅ 代码已生成并保存")


def test_workflow_import_export():
    """测试完整的工作流导入导出流程"""
    print("\n" + "=" * 60)
    print("测试3: 完整的工作流导入导出流程")
    print("=" * 60)
    
    # 步骤1: 手动创建工作流
    print("步骤1: 创建工作流...")
    workflow = NL2Workflow(
        platform="dify",
        config=DifyConfig(
            app_name="测试工作流",
            app_description="用于测试DifyParser",
            app_icon="🚀",
            app_icon_background="#FFE5E5"
        )
    )
    
    workflow.add_node(
        id=START,
        position={"x": 50, "y": 200},
        state=DifyStartState(title="开始"),
    )
    
    workflow.add_node(
        id="ai",
        state=DifyLLMState(
            title="AI处理",
            prompt_template=[{"role": "system", "text": "你是一个智能助手"}],
            model={
                "completion_params": {"temperature": 0.8},
                "mode": "chat",
                "name": "gpt-4",
                "provider": "openai"
            }
        ),
        position={"x": 300, "y": 200}
    )
    
    workflow.add_node(
        id=END,
        state=DifyEndState(title="结束"),
        position={"x": 550, "y": 200}
    )
    
    workflow.add_edge(START, "ai")
    workflow.add_edge("ai", END)
    
    # 步骤2: 保存为YAML
    print("步骤2: 保存为YAML...")
    yaml_path = "playground/dify/outputs/test_workflow.yaml"
    workflow.save(yaml_path)
    print(f"✅ YAML已保存到: {yaml_path}")
    
    # 步骤3: 从YAML生成代码
    print("步骤3: 从YAML生成Python代码...")
    parser = DifyParser()
    generated_code = parser.from_yaml_file(
        yaml_file_path=yaml_path,
        output_path="playground/dify/outputs/generated_workflow.py"
    )
    print("✅ Python代码已生成")
    
    # 步骤4: 显示生成的代码
    print("\n生成的代码预览:")
    print("-" * 60)
    lines = generated_code.split('\n')
    for i, line in enumerate(lines[:30], 1):  # 显示前30行
        print(f"{i:3d} | {line}")
    if len(lines) > 30:
        print("    ...")
        print(f"    (共 {len(lines)} 行)")
    print("-" * 60)
    
    print("\n✅ 完整流程测试成功！")


def main():
    """主函数"""
    print("\n" + "🚀 " * 20)
    print("DifyParser 测试程序")
    print("🚀 " * 20 + "\n")
    
    # 创建输出目录
    os.makedirs("playground/dify/outputs", exist_ok=True)
    
    # 运行测试
    try:
        # test_from_yaml_file()
        test_from_yaml_string()
        test_workflow_import_export()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        
        print("\n使用说明:")
        print("1. 从Dify平台导出工作流YAML文件")
        print("2. 使用DifyParser将YAML转换为Python SDK代码")
        print("3. 运行生成的Python代码来重建工作流")
        
        print("\n示例代码:")
        print("-" * 60)
        print("""
from autoagents_graph.engine.dify import DifyParser

parser = DifyParser()

# 方法1: 从YAML文件生成代码
code = parser.from_yaml_file(
    yaml_file_path="dify_workflow.yaml",
    output_path="generated_workflow.py"
)

# 方法2: 从YAML字符串生成代码  
code = parser.from_yaml_to_code(
    yaml_content=yaml_string,
    output_path="generated_workflow.py"
)

# 方法3: 从JSON文件生成代码
code = parser.from_json_file(
    json_file_path="dify_workflow.json",
    output_path="generated_workflow.py"
)
        """)
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

