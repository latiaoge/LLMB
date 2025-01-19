
# LLMB项目 - 本地大模型记忆系统

## 简介

LLMB（Large Language Model with Memory）项目旨在构建一个高效、功能丰富的本地大模型记忆系统。它集成了Langchain框架、Ollama语言模型、中文向量模型（text2vec-large-chinese），以及关系型数据库（如SQLite），实现了向量检索和持久化存储功能。该系统能够接收用户的输入，利用内存管理和向量存储来跟踪对话上下文，并通过调用外部的语言模型（Ollama）生成智能回复。此外，LLMB还维护聊天历史数据库，并使用Redis加速某些操作或保持会话状态。

本项目适用于多种应用场景，包括但不限于客户服务聊天机器人、虚拟助手、自动化问答系统等。

---

## 目录结构与代码说明

- **database.py**  
  处理SQLite数据库连接和会话历史的持久化。
  
- **vector_store.py**  
  实现向量存储和检索功能，支持FAISS和SentenceTransformer模型，用于保存用户输入和AI回复的嵌入向量，并通过向量检索找到相关的历史记录。
  
- **ollama_client.py**  
  封装了对Ollama API的调用逻辑，负责### 优化后的 README 文件（含文件结构）

---

# LLMB项目 - 强大的本地大模型记忆系统

## 简介

LLMB（Large Language Model with Memory）项目旨在构建一个高效、功能丰富的本地大模型记忆系统。它集成了Langchain框架、Ollama语言模型、中文向量模型（text2vec-large-chinese），以及关系型数据库（如SQLite），实现了向量检索和持久化存储功能。该系统能够接收用户的输入，利用内存管理和向量存储来跟踪对话上下文，并通过调用外部的语言模型（Ollama）生成智能回复。此外，LLMB还维护聊天历史数据库，并使用Redis加速某些操作或保持会话状态。

本项目适用于多种应用场景，包括但不限于客户服务聊天机器人、虚拟助手、自动化问答系统等。

---

## 文件结构与代码说明

以下是项目的文件结构及每个文件/目录的简要说明：

```
.
├── analyze_logs.py        # 日志分析脚本
├── chat_history.db       # SQLite 数据库文件，用于存储聊天记录
├── database.py           # 处理 SQLite 数据库连接和会话历史的持久化
├── gunicorn_conf.py      # Gunicorn 配置文件
├── logger.py             # 日志模块实现
├── logs/                 # 存储日志文件的目录
├── main.py               # 主应用逻辑入口
├── memory_manager.py     # 内存管理器实现，用于存储用户的重要信息
├── models.py             # 定义请求和响应的数据模型
├── ollama_client.py      # 封装了对 Ollama API 的调用逻辑
├── README.md             # 项目文档
├── requirements.txt      # Python 依赖包列表
├── testclient.py         # 测试客户端脚本
├── text2vec-large-chinese/ # 中文向量模型目录
├── utils.py              # 工具函数集合
├── vector_store/         # 向量存储相关资源
└── vector_store.py       # 实现向量存储和检索功能
└── __pycache__/          # 编译后的 Python 字节码缓存
```

---

## 核心功能

- **数据库持久化聊天历史**  
  使用SQLite数据库记录每轮对话的用户输入和模型输出，这些聊天历史将作为上下文信息的一部分，帮助生成更准确的回复。

- **向量存储与检索**  
  利用FAISS库和`text2vec-large-chinese`模型，为用户输入和AI回复创建高维嵌入向量，并通过快速近似最近邻搜索算法实现高效的向量检索。

- **Ollama 模型调用**  
  通过封装好的接口轻松调用Ollama API，获取高质量的语言模型回复。

- **记忆管理**  
  设计了一个简单的记忆管理器，可以存储用户的重要信息（如姓名等），以便在后续对话中引用。

- **完整提示生成**  
  构建包含聊天历史、向量检索结果和当前用户输入的完整提示，提供给语言模型作为生成回复的上下文。

---

## 快速开始指南

### 步骤 1: 环境准备

请确保您的环境中已经安装了以下组件：

- Python 3.7+
- Ollama（本地运行的大语言模型服务）
- Langchain 库
- Redis服务及其客户端

### 步骤 2: 安装依赖

执行以下命令安装所需的Python库：

```bash
pip install -r requirements.txt
```

### 步骤 3: 启动应用

选择一种方式启动FastAPI应用：

#### 使用 Uvicorn 启动：
```bash
uvicorn main:app --host 0.0.0.0 --port 11405
```

#### 使用 Gunicorn 启动：
```bash
gunicorn -c gunicorn_conf.py main:app
```

### 步骤 4: 测试

运行测试客户端验证系统是否正常工作：

```bash
python testclient.py
```

---

## 贡献者指南

如果您有兴趣为LLMB项目做出贡献，请遵循[CONTRIBUTING.md](./CONTRIBUTING.md)中的指导方针。

---

## 许可证

本项目采用MIT许可证，详情参见[LICENSE](./LICENSE)文件。

---

希望这个优化后的README文件能更好地介绍LLMB项目的特性和使用方法。如果有任何进一步的需求或问题，请随时联系。

---

### 附录：项目文件列表

以下是项目中所有文件及其最后修改时间的详细列表：

| 修改日期 | 文件大小 (字节) | 文件名 |
| --- | --- | --- |
| 2025/01/19 周日 21:49 | <DIR> | . |
| 2025/01/19 周日 21:49 | <DIR> | .. |
| 2025/01/17 周五 10:22 | 1,419 | analyze_logs.py |
| 2025/01/18 周六 23:35 | 24,576 | chat_history.db |
| 2025/01/17 周五 23:20 | 2,495 | database.py |
| 2025/01/19 周日 21:24 | 806 | gunicorn_conf.py |
| 2025/01/18 周六 00:33 | 580 | logger.py |
| 2025/01/19 周日 21:19 | <DIR> | logs/ |
| 2025/01/18 周六 23:11 | 9,488 | main.py |
| 2025/01/17 周五 10:14 | 888 | memory_manager.py |
| 2025/01/19 周日 21:25 | 867 | models.py |
| 2025/01/19 周日 21:30 | 2,498 | ollama_client.py |
| 2025/01/19 周日 22:09 | 3,634 | README.md |
| 2025/01/19 周日 21:44 | 87 | requirements.txt |
| 2025/01/19 周日 21:46 | 1,357 | testclient.py |
| 2025/01/19 周日 21:49 | <DIR> | text2vec-large-chinese/ |
| 2025/01/17 周五 10:12 | 113 | utils.py |
| 2025/01/19 周日 21:19 | <DIR> | vector_store/ |
| 2025/01/18 周六 23:29 | 8,471 | vector_store.py |
| 2025/01/19 周日 21:19 | <DIR> | __pycache__/ |

此列表提供了项目文件的时间戳和大小信息，有助于了解项目的最新更新情况。与Ollama服务进行通信以生成模型回复。
  
- **models.py**  
  定义了请求和响应的数据模型，确保数据格式的一致性和正确性。
  
- **main.py**  
  包含主应用逻辑，协调各个模块的工作流程。
  
- **utils.py**  
  提供了一系列工具函数，简化开发过程中的常见任务。

---

## 核心功能

- **数据库持久化聊天历史**  
  使用SQLite数据库记录每轮对话的用户输入和模型输出，这些聊天历史将作为上下文信息的一部分，帮助生成更准确的回复。

- **向量存储与检索**  
  利用FAISS库和`text2vec-large-chinese`模型，为用户输入和AI回复创建高维嵌入向量，并通过快速近似最近邻搜索算法实现高效的向量检索。

- **Ollama 模型调用**  
  通过封装好的接口轻松调用Ollama API，获取高质量的语言模型回复。

- **记忆管理**  
  设计了一个简单的记忆管理器，可以存储用户的重要信息（如姓名等），以便在后续对话中引用。

- **完整提示生成**  
  构建包含聊天历史、向量检索结果和当前用户输入的完整提示，提供给语言模型作为生成回复的上下文。

---

## 快速开始指南

### 步骤 1: 环境准备

请确保您的环境中已经安装了以下组件：

- Python 3.7+
- Ollama（本地运行的大语言模型服务）
- Langchain 库
- Redis服务及其客户端

### 步骤 2: 安装依赖

执行以下命令安装所需的Python库：

```bash
pip install -r requirements.txt
```

### 步骤 3: 启动应用

选择一种方式启动FastAPI应用：

#### 使用 Uvicorn 启动：
```bash
uvicorn main:app --host 0.0.0.0 --port 11405
```

#### 使用 Gunicorn 启动：
```bash
gunicorn -c gunicorn_conf.py main:app
```

### 步骤 4: 测试

运行测试客户端验证系统是否正常工作：

```bash
python testclient.py
```

---

## 贡献者指南

如果您有兴趣为LLMB项目做出贡献，请遵循[CONTRIBUTING.md](./CONTRIBUTING.md)中的指导方针。

---

## 许可证

本项目采用MIT许可证，详情参见[LICENSE](./LICENSE)文件。

---

希望这个优化后的README文件能更好地介绍LLMB项目的特性和使用方法。如果有任何进一步的需求或问题，请随时联系。