import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.autoagents_graph.engine.dify.services.dify_graph import DifyGraph


def main():
    """使用DifyGraph直接加载和保存YAML"""
    # 从源YAML文件加载
    source_file = "playground/dify/inputs/智票通 - 批量发票智能解析 (1)_副本.yml"
    
    # 加载DifyGraph
    dify_graph = DifyGraph.from_yaml_file(source_file)
    
    # 保存到输出文件
    output_file = "playground/dify/outputs/dify_workflow_output.yaml"
    dify_graph.save_yaml(output_file)
    
    print(f"工作流已生成，输出文件: {output_file}")
    
    # 获取YAML内容长度
    yaml_result = dify_graph.to_yaml()
    print(f"YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()
