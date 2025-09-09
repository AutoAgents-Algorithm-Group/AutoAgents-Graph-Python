# src/agentify/__init__.py - Agentify 模块
from .FlowGraph import FlowGraph, START
from .NodeRegistry import NODE_TEMPLATES
# from .AutoWorkFlow import AutoWorkFlow  # AutoWorkFlow文件不存在
from .FlowInterpreter import FlowInterpreter
# from .Text2Workflow import Text2Workflow  # Text2Workflow已移动到src根目录
from .Utils import (
    StateConverter, NodeValidator, NodeBuilder, EdgeValidator, GraphProcessor,
    DataConverter, TemplateProcessor
)
from .types import *
# from .api.GraphAPI import GraphAPI  # GraphAPI类不存在，注释掉

__all__ = [
    "FlowGraph", "NODE_TEMPLATES", "FlowInterpreter", "START", 
    "StateConverter", "NodeValidator", "NodeBuilder", "EdgeValidator", "GraphProcessor",
    "DataConverter", "TemplateProcessor"
]

def main() -> None:
    print("Hello from Agentify modules!")