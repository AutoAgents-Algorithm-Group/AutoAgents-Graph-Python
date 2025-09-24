from autoagents_graph.agentify import FlowGraph, START
from autoagents_graph.agentify.models import (
    QuestionInputState, Pdf2MdState, ConfirmReplyState, 
    AiChatState, AddMemoryVariableState
)

def main():
    graph = FlowGraph(
        personal_auth_key="your_auth_key",
        personal_auth_secret="your_auth_secret",
        base_url="https://uat.agentspro.cn"
    )

    # 添加节点
    graph.add_node(
        id=START,
        state=QuestionInputState(
            inputText=True,
            uploadFile=True,
            uploadPicture=False,
            fileContrast=False,
            initialInput=True
        )
    )

    graph.add_node(
        id="pdf2md1",
        state=Pdf2MdState(
            pdf2mdType="deep_pdf2md"
        )
    )

    graph.add_node(
        id="confirmreply1",
        state=ConfirmReplyState(
            text=r"文件内容：{_{pdf2md1_pdf2mdResult}}",
            stream=True
        )
    )

    graph.add_node(
        id="ai1",
        state=AiChatState(
            model="doubao-deepseek-v3",
            quotePrompt="""
<角色>
你是一个文件解答助手，你可以根据文件内容，解答用户的问题
</角色>

<文件内容>
{{@pdf2md1_pdf2mdResult}}
</文件内容>

<用户问题>
{{@question1_userChatInput}}
</用户问题>
            """,
            knSearch="",
            temperature=0.1
        )
    )

    # 配置记忆变量
    memory_variables = {
        "question1_userChatInput": {
            "key": "question1_userChatInput",
            "value_type": "String"
        },
        "pdf2md1_pdf2mdResult": {
            "key": "pdf2md1_pdf2mdResult", 
            "value_type": "String"
        },
        "ai1_answerText": {
            "key": "ai1_answerText",
            "value_type": "String"
        }
    }

    graph.add_node(
        id="addMemoryVariable1",
        position={"x": 0, "y": 1500},
        state=AddMemoryVariableState(
            variables=memory_variables
        )
    )

    # 添加连接边
    graph.add_edge(START, "pdf2md1", "finish", "switchAny")
    graph.add_edge(START, "pdf2md1", "files", "files")
    graph.add_edge(START, "addMemoryVariable1", "userChatInput", "question1_userChatInput")

    graph.add_edge("pdf2md1", "confirmreply1", "finish", "switchAny")
    graph.add_edge("pdf2md1", "addMemoryVariable1", "pdf2mdResult", "pdf2md1_pdf2mdResult")
    
    graph.add_edge("confirmreply1", "ai1", "finish", "switchAny")

    graph.add_edge("ai1", "addMemoryVariable1", "answerText", "ai1_answerText")
    
    # 编译
    graph.compile(
        name="AWF文档提问助手",
        intro="这是一个专业的文档助手，可以帮助用户分析和理解文档内容",
        category="文档处理",
        prologue="你好！我是你的文档助手，请上传文档，我将帮您分析内容。",
        shareAble=True,
        allowVoiceInput=False,
        autoSendVoice=False
    )

if __name__ == "__main__":
    main()