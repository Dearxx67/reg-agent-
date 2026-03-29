import streamlit as st
from rag_core import load_documents, split_documents, build_vector_db, build_rag_chain
from agent_core import build_agent

# 页面配置
st.set_page_config(page_title="RAG+Agent智能文档助手", page_icon="📚", layout="wide")
st.title("📚 基于RAG+Prompt+Agent的企业文档智能问答助手")
st.markdown("---")

# 初始化项目（只在第一次运行时执行）
if "db" not in st.session_state:
    with st.spinner("🔄 正在初始化系统：加载文档 → 分块 → 构建向量库..."):
        # 1. 加载文档
        docs = load_documents()
        # 2. 分块
        chunks = split_documents(docs)
        # 3. 构建向量库
        st.session_state.db = build_vector_db(chunks)
        # 4. 构建RAG链
        st.session_state.chain = build_rag_chain()
        # 5. 构建Agent
        st.session_state.agent = build_agent(st.session_state.db, st.session_state.chain)
    st.success("✅ 系统初始化完成！可以开始提问了")

# 聊天交互区
st.subheader("💬 问答区")
user_query = st.text_input("请输入你的问题：", placeholder="例如：请总结XX文档的核心内容？XX流程是什么？")

if user_query:
    with st.spinner("🤖 Agent正在规划任务并检索文档..."):
        # 调用Agent执行完整流程
        result = st.session_state.agent.invoke({
            "query": user_query,
            "plan": [],
            "context": "",
            "answer": ""
        })
        # 展示回答
        st.markdown("### 🎯 回答：")
        st.write(result["answer"])
        # 可选：展示Agent的规划过程（方便调试，简历可展示）
        with st.expander("🔍 查看Agent任务规划过程"):
            st.write(result["plan"][0])