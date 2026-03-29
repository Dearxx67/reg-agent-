import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_dashscope import ChatDashScope  # 替换成通义千问
from prompt_template import RAG_PROMPT

load_dotenv()

# 1. 文档加载
def load_documents(file_dir="documents"):
    documents = []
    for file in os.listdir(file_dir):
        file_path = os.path.join(file_dir, file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        else:
            print(f"跳过不支持的文件格式：{file}")
            continue
        documents.extend(loader.load())
    print(f"成功加载 {len(documents)} 个文档片段")
    return documents

# 2. 文本分块
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "；", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"分块完成，共 {len(chunks)} 个文本块")
    return chunks

# 3. 构建向量库
def build_vector_db(chunks):
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="vector_db"
    )
    print("向量库构建完成并持久化")
    return db

# 4. 构建RAG链（仅修改这里，换成通义千问）
def build_rag_chain():
    # 通义千问开源模型，免费、国内直连
    llm = ChatDashScope(
        model="qwen-turbo",  # 轻量版，速度快，免费额度高
        temperature=0  # 0温度保证输出稳定，抑制幻觉
    )
    rag_chain = RAG_PROMPT | llm | StrOutputParser()
    return rag_chain

# 5. 检索+回答
def rag_qa(db, chain, question):
    retriever = db.as_retriever(search_kwargs={"k": 3})
    relevant_docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    answer = chain.invoke({"context": context, "question": question})
    return answer