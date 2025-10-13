import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from src.autoagents_graph import NL2Workflow, DifyConfig
from src.autoagents_graph.engine.dify import (
    DifyStartState, DifyLLMState, DifyKnowledgeRetrievalState,
    DifyEndState, DifyAnswerState, DifyCodeState, DifyToolState,
    DifyIfElseState, START, END
)


def main():
    # 创建Dify工作流
    workflow = NL2Workflow(
        platform="dify",
        config=DifyConfig(
            app_name="从Dify导出的工作流",
            app_description="通过DifyParser自动生成",
            app_icon="🤖",
            app_icon_background="#FFEAD5"
        )
    )

    # 添加节点
    # 添加开始节点
    workflow.add_node(
        id=START,
        position={'x': 401.90026926950384, 'y': 486.7408933479527},
        state=DifyStartState(
            title="开始",
            variables=[{'label': '文章主题', 'required': True, 'type': 'text-input', 'variable': 'topic'}, {'label': '目标字数', 'max_length': 48, 'required': True, 'type': 'text-input', 'variable': 'target_length'}, {'label': '文章风格', 'options': ['学术严谨', '科技创新', '商业分析', '生活随笔', '新闻报道'], 'required': False, 'type': 'select', 'variable': 'style'}, {'label': '目标读者', 'max_length': 250, 'options': [], 'required': True, 'type': 'text-input', 'variable': 'target_audience'}],
        )
    )

    # 添加大纲生成器节点
    workflow.add_node(
        id="outline_generator",
        position={'x': 665.4736898687406, 'y': 486.7408933479527},
        state=DifyLLMState(
            title="大纲生成器",
            model={'completion_params': {}, 'mode': 'chat', 'name': 'qwen3:latest', 'provider': 'langgenius/ollama/ollama'},
            prompt_template=[{'id': 'system-prompt', 'role': 'system', 'text': '你是一位资深的内容策略师，擅长制定清晰的内容框架和写作大纲。你的任务是为一篇长文制定详细的写作大纲。\n\n要求：\n1. 分析主题的关键维度和核心要点\n2. 设计逻辑严密的章节结构\n3. 每个章节都要有明确的写作方向和重点\n4. 考虑内容的连贯性和递进关系\n5. 根据目标字数合理分配各章节的篇幅\n6. 输出格式要规范，便于后续处理\n\n输出格式示例：\n{\n  "title": "文章标题",\n  "sections": [\n    {\n      "section_number": 1,\n      "title": "章节标题",\n      "key_points": ["要点1", "要点2"],\n      "target_length": 500\n    }\n  ],\n  "total_sections": 5\n}\n'}, {'id': 'user-prompt', 'role': 'user', 'text': '请为以下主题制定写作大纲：\n- 文章的核心主题：{{#start.topic#}}\n- 目标读者：{{#start.target_audience#}}\n- 预期的总字数：{{#start.target_length#}}\n- 文案的风格和语调：{{#start.style#}}\n'}],
            context={'enabled': False, 'variable_selector': []},
            variables=[],
        )
    )

    # 未知节点类型: iteration

    # 添加总编辑节点
    workflow.add_node(
        id="final_editor",
        position={'x': 1385.656212163108, 'y': 833.4731210545426},
        state=DifyLLMState(
            title="总编辑",
            model={'completion_params': {}, 'mode': 'chat', 'name': 'qwen3:latest', 'provider': 'langgenius/ollama/ollama'},
            prompt_template=[{'id': 'system-prompt', 'role': 'system', 'text': "你将扮演一位资深的中文总编辑。你的任务是，根据我提供的分散的章节草稿和总体要求，将它们整合成一篇逻辑连贯、行文流畅、结构完整的最终文章。\n\n### 原始材料\n\n- 文章的核心主题：{{#start.topic#}}\n- 目标读者：{{#start.target_audience#}}\n- 预期的总字数：{{#start.target_length#}}\n- 文案的风格和语调：{{#start.style#}}\n3.  **原始大纲 (供参考)**:{{#outline_generator.text#}}\n4.  **各章节独立撰写的内容 (已拼接)**:\n{{{#section_iterator.output#}} | join('\\n\\n---\\n\\n')}}\n\n### 你的任务与执行步骤\n\n1.  **撰写引言**: 根据总主题和目标受众，写一个大约200字的、吸引人的引言，概括全文核心价值。\n2.  **整合主体**: 将上面提供的“各章节独立撰写的内容”自然地衔接起来。注意章节之间的过渡要平滑，而不是生硬地罗列。\n3.  **撰写结论**: 根据全文内容，进行有力的总结，并可以提出号召性用语（Call to Action）或深刻的见解。\n4.  **通篇润色**: 检查并统一全文的语气、风格，修正任何不通顺或逻辑不清晰的地方。\n5.  **添加标题**: 在文章最前面，加上一个与主题和风格相符的、吸引人的总标题。\n\n### 输出要求\n\n请直接输出最终完成的、完整的文章正文，从总标题开始。不要包含任何额外的解释或元信息。"}],
            context={'enabled': False, 'variable_selector': []},
            variables=[],
        )
    )

    # 未知节点类型: iteration-start

    # 添加LLM 4节点
    workflow.add_node(
        id="node_1749443261566",
        position={'x': 139, 'y': 67.07269804075315},
        state=DifyLLMState(
            title="LLM 4",
            model={'completion_params': {}, 'mode': 'chat', 'name': 'qwen3:latest', 'provider': 'langgenius/ollama/ollama'},
            prompt_template=[{'id': '8bfb0906-76e8-46f3-858f-4132cecf9454', 'role': 'system', 'text': '# 角色\n你是一位专业的文案撰稿人，擅长将一个具体的主题要点，扩展成内容丰富、逻辑清晰、引人入胜的段落。\n\n# 任务\n你的核心任务是，根据下面提供的“当前章节信息”，专注于撰写**这一个章节**的详细内容。\n\n# 文章总体信息（供你参考风格和背景）\n- 文章的核心主题：{{#start.topic#}}\n- 目标读者：{{#start.target_audience#}}\n- 预期的总字数：{{#start.target_length#}}\n- 文案的风格和语调：{{#start.style#}}\n\n# 当前章节信息（本次写作的唯一依据）\n- 章节标题: {{#section_iterator.item#}}\n\n# 写作要求\n1.  **紧扣主题**：严格围绕“当前章节信息”给出的标题和要点展开，不要跑题或引入无关内容。\n2.  **内容详实**：对核心要点进行充分的阐述、解释或举例。\n3.  **独立成篇**：仅撰写本章节的正文，**不要**包含如“在本章中，我们将讨论...”或“总结一下，本章...”这类承上启下的句子。这些工作将由后续的“总编辑”完成。\n4.  **直接输出**：请直接输出撰写好的正文内容，不要添加任何额外的标题或说明。'}],
            context={'enabled': False, 'variable_selector': []},
            variables=[],
        )
    )

    # 添加结束节点
    workflow.add_node(
        id=END,
        position={'x': 1374.8045005525457, 'y': 978.5493669568815},
        state=DifyEndState(
            title="结束",
            outputs=[{'value_selector': ['final_editor', 'text'], 'variable': 'final_article'}, {'value_selector': ['section_iterator', 'output'], 'variable': 'sections'}],
        )
    )

    # 添加代码执行节点
    workflow.add_node(
        id="node_1749449203563",
        position={'x': 937.9239083622927, 'y': 486.7408933479527},
        state=DifyCodeState(
            title="代码执行",
            code="""import json
import re

def main(**kwargs) -> dict:
  \"""
  加强版主函数：
  1. 从可能混杂的文本中提取出最外层的 JSON 对象或数组。
  2. 将提取出的 JSON 字符串解析为 Python 对象。
  \"""
  outline_str = kwargs.get('outline_string', '')
  
  parsed_json = None
  
  # 1. 使用正则表达式查找被 {} 或 [] 包围的最长字符串
  #    这可以处理 JSON 前后有无关文字或 markdown 标记的情况
  match = re.search(r'(\\{.*\\}|\\[.*\\])', outline_str, re.DOTALL)
  
  if match:
    # 如果找到了匹配项，就用这个匹配到的干净字符串进行解析
    json_string = match.group(0)
    try:
      parsed_json = json.loads(json_string)
    except json.JSONDecodeError:
      parsed_json = None # 解析失败
  else:
    # 如果正则没找到，尝试直接解析整个原始字符串
    try:
      parsed_json = json.loads(outline_str)
    except json.JSONDecodeError:
      parsed_json = None # 还是解析失败

  # 2. 检查解析结果并返回
  #    我们的目标是获取 "sections" 里面的那个列表
  final_list = []
  if isinstance(parsed_json, dict) and 'sections' in parsed_json and isinstance(parsed_json['sections'], list):
    # 如果解析结果是一个字典，并且里面有 'sections' 键，且其值是列表
    final_list = parsed_json['sections']
  elif isinstance(parsed_json, list):
    # 如果解析结果本身就是一个列表（对应您最初的 Prompt）
    final_list = parsed_json

  return {
    'result': final_list
  }""",
            code_language="python3",
            outputs={'result': {'children': None, 'type': 'array[object]'}},
            variables=[{'value_selector': ['outline_generator', 'text'], 'variable': 'outline_string'}],
        )
    )

    # 添加连接边
    workflow.add_edge(START, "outline_generator")
    workflow.add_edge("section_iterator", "final_editor")
    workflow.add_edge("section_iteratorstart0", "node_1749443261566")
    workflow.add_edge("outline_generator", "node_1749449203563")
    workflow.add_edge("node_1749449203563", "section_iterator")
    workflow.add_edge("final_editor", END)

    # 编译并保存
    yaml_result = workflow.compile()
    workflow.save("playground/dify/outputs/dify_workflow_output.yaml")
    print(f"工作流已生成，YAML长度: {len(yaml_result)} 字符")


if __name__ == "__main__":
    main()