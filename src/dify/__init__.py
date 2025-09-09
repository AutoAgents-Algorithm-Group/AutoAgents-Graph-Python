# src/dify/__init__.py
from .DifyGraph import DifyGraphBuilder, START, END
from .DifyTypes import *

# 为了兼容性，将DifyGraphBuilder导出为DifyGraph
DifyGraph = DifyGraphBuilder

__all__ = ["DifyGraph", "DifyGraphBuilder", "START", "END"]

