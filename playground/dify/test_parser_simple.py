import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph.engine.dify import DifyParser


def main():
    """简单测试"""
    print("测试 DifyParser 基本功能\n")
    
    parser = DifyParser()
    
    # 测试YAML字符串生成代码
    yaml_content = """
app:
  name: 简单测试
  description: 测试工作流
  icon: 🤖
  icon_background: '#FFEAD5'
  mode: workflow
  use_icon_as_answer_icon: false
kind: app
version: 0.3.1
workflow:
  conversation_variables: []
  environment_variables: []
  features: {}
  graph:
    edges:
    - id: start-source-end-target
      source: start
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
        variables: []
    - id: end
      type: custom
      position:
        x: 300
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
    
    print("正在生成代码...")
    try:
        code = parser.from_yaml_to_code(yaml_content)
        print("\n生成的代码:")
        print("=" * 60)
        print(code)
        print("=" * 60)
        print("\n✅ 测试成功！")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

