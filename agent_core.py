from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_dashscope import ChatDashScope  # 替换成通义千问
from prompt_template import AGENT_PLAN_PROMPT
from rag_core import rag_qa


# 状态定义
class AgentState(TypedDict):
    query: str
    plan: str
    context: str
    answer: str


# 初始化通义千问大模型
llm = ChatDashScope(model="qwen-turbo", temperature=0)


# 1. 规划节点
def plan_node(state: AgentState):
    prompt = AGENT_PLAN_PROMPT.format(query=state["query"])
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"plan": response.content}


# 2. 执行节点
def execute_node(state: AgentState, db, chain):
    answer = rag_qa(db, chain, state["query"])
    return {"answer": answer}


# 3. 构建Agent图
def build_agent(db, chain):
    workflow = StateGraph(AgentState)

    workflow.add_node("plan_node", plan_node)
    workflow.add_node("execute", lambda s: execute_node(s, db, chain))

    workflow.set_entry_point("plan_node")
    workflow.add_edge("plan_node", "execute")
    workflow.add_edge("execute", END)

    return workflow.compile()