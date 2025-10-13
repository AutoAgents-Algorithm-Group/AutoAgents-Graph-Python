import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.autoagents_graph.engine.dify import DifyParser


def test_from_yaml_file():
    """测试从YAML文件生成代码"""
    print("=" * 60)
    print("DifyParser - 从YAML文件生成代码")
    print("=" * 60)
    
    parser = DifyParser()
    
    # 测试文件列表
    test_files = [
        "playground/dify/inputs/example.yml"
    ]
    
    for yaml_file in test_files:
        print(f"\n📁 处理文件: {yaml_file}")
        
        if os.path.exists(yaml_file):
            try:
                # 生成输出文件名
                base_name = os.path.splitext(os.path.basename(yaml_file))[0]
                output_file = f"playground/dify/outputs/generated_{base_name}.py"
                
                # 生成代码
                generated_code = parser.from_yaml_file(
                    yaml_file_path=yaml_file,
                    output_path=output_file
                )
                
                print(f"✅ 代码已生成并保存到: {output_file}")
                
                # 显示生成代码的前几行
                lines = generated_code.split('\n')
                print(f"📊 生成代码统计: 共 {len(lines)} 行")
                
                # 显示代码预览
                print("\n代码预览 (前15行):")
                print("-" * 40)
                for i, line in enumerate(lines[:15], 1):
                    print(f"{i:2d} | {line}")
                if len(lines) > 15:
                    print(f"    ... (还有 {len(lines) - 15} 行)")
                print("-" * 40)
                
            except Exception as e:
                print(f"❌ 处理失败: {str(e)}")
                import traceback
                traceback.print_exc()
        else:
            print(f"⚠️  文件不存在: {yaml_file}")
    
    print(f"\n🎉 测试完成!")


def main():
    """主函数"""
    print("\n" + "🧪 " * 20)
    print("DifyParser 测试程序")
    print("🧪 " * 20 + "\n")
    
    # 创建输出目录
    os.makedirs("playground/dify/outputs", exist_ok=True)
    
    # 运行测试
    try:
        test_from_yaml_file()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成!")
        print("=" * 60)
        
        print("\n📖 使用说明:")
        print("1. 从Dify平台导出工作流YAML文件")
        print("2. 将文件放在 playground/dify/inputs/ 目录下")
        print("3. 运行此程序生成对应的Python SDK代码")
        print("4. 生成的代码保存在 playground/dify/outputs/ 目录下")
        
        print("\n💡 支持的节点类型:")
        print("- start (开始节点)")
        print("- llm (LLM节点)")
        print("- knowledge-retrieval (知识检索节点)")
        print("- end (结束节点)")
        print("- answer (直接回复节点)")
        print("- code (代码执行节点)")
        print("- tool (工具调用节点)")
        print("- if-else (条件分支节点)")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()