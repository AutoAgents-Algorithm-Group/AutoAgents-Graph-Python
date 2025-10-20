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
        print("测试完成!")
        print("=" * 60)
      
        
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()