# 基于RAG+Prompt+Agent的企业文档智能问答系统
## 项目介绍
本项目是一个基于LangChain+LangGraph构建的大模型应用，融合RAG检索增强生成、精细化Prompt工程与任务规划智能Agent，实现对PDF/Word/TXT等多格式文档的精准问答、结构化信息抽取与自动总结，支持Streamlit Web可视化部署，可直接落地为企业内部知识库助手，有效解决大模型“幻觉”问题。

## 核心功能
1.  多格式文档加载：支持PDF、Word、TXT文档的批量加载与解析
2.  RAG检索增强：实现文档分块、向量化、向量存储与精准检索，基于事实回答
3.  智能Agent规划：通过LangGraph实现任务规划，自动判断检索需求、生成检索策略
4.  Web可视化交互：基于Streamlit搭建直观的问答界面，支持Agent规划过程查看
5.  幻觉抑制：通过精细化Prompt工程，约束模型输出，确保回答基于文档事实

## 技术栈
- 编程语言：Python 3.10
- 大模型：通义千问Qwen（qwen-turbo）
- 核心框架：LangChain、LangGraph
- 向量数据库：Chroma
- 文档处理：PyPDF2、python-docx
- Web部署：Streamlit
- 其他：HuggingFace Embeddings、python-dotenv、numpy、pandas

## 环境搭建
### 1. 创建虚拟环境
```bash
conda create -n rag_agent python=3.10
conda activate rag_agent
```

### 2. 安装依赖
```bash
pip install langchain==0.2.16 langchain-chroma==0.1.4 langchain-community==0.2.16 langchain-text-splitters==0.2.4 langgraph==0.2.14 langchain-dashscope==0.1.8 pypdf python-docx streamlit sentence-transformers python-dotenv numpy pandas
```

## 运行步骤
1.  复制项目到本地，进入项目根目录
2.  在.env文件中填入通义千问API Key（DASHSCOPE_API_KEY=你的API Key）
3.  在documents文件夹中放入测试用的PDF/Word/TXT文档
4.  执行命令运行项目：
    ```bash
    streamlit run app.py
    ```
5.  浏览器自动打开，等待系统初始化完成后，即可输入问题进行问答

## 项目结构
```
rag_agent_project/
├── .env                # 存放API Key
├── app.py              # Streamlit主程序（Web界面）
├── rag_core.py         # RAG核心模块（文档加载、分块、检索等）
├── agent_core.py       # Agent核心模块（任务规划、执行）
├── prompt_template.py  # Prompt工程模块（幻觉抑制、输出规范）
├── documents/          # 存放测试文档（PDF/Word/TXT）
├── vector_db/          # 向量库存储目录
└── README.md           # 项目说明文档
```

## 注意事项
1.  确保.env文件中的API Key正确，无空格、无引号
2.  documents文件夹中需放入至少1份测试文档，否则系统初始化会卡住
3.  若出现依赖冲突，可参考requirements.txt（或重新执行环境搭建命令）
4.  运行时确保rag_agent虚拟环境已激活