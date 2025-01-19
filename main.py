from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import json
import redis
import asyncio
import hashlib
from logger import logger  # 日志模块
from database import get_db, add_chat_history
from memory_manager import memory_manager
from ollama_client import call_ollama  # 改为异步函数
from vector_store import VectorStore  # 引入 VectorStore 类

# 应用实例
app = FastAPI()

# Redis 客户端设置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    redis_client.ping()  # 测试连接
    logger.info("Connected to Redis successfully.")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None  # 防止服务崩溃

# 实例化 VectorStore
vector_store = VectorStore(dimension=1024, save_path="./vector_store")  # 保存路径指定

# 定义请求和响应模型
class Message(BaseModel):
    role: str  # 消息角色，例如 "user" 或 "assistant"
    content: str  # 消息内容

class ChatRequest(BaseModel):
    model: str  # 模型名称
    messages: List[Message]  # 消息历史记录
    max_tokens: int  # 最大生成的 token 数
    temperature: float  # 温度值，控制生成的随机性
    stream: bool  # 是否开启流式传输

class ChatMessage(BaseModel):
    role: str  # 消息角色
    content: str  # 消息内容

class ChatResponseChoice(BaseModel):
    message: ChatMessage  # AI 的单条回复

class ChatResponse(BaseModel):
    choices: List[ChatResponseChoice]  # AI 回复的列表（通常为 1 条）

# 辅助函数
async def generate_response(messages: List[dict], model: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
    """
    调用 Ollama 模型生成回复（异步版）
    """
    try:
        # 校验 messages 参数格式
        if not isinstance(messages, list) or any(
            not isinstance(m, dict) or "role" not in m or "content" not in m for m in messages
        ):
            raise ValueError("`messages` 参数格式无效，必须为包含 `role` 和 `content` 键的字典列表。")

        # 调用外部 Ollama API
        logger.info(f"调用 Ollama 模型 '{model}'，上下文: {messages[:5]}")  # 仅打印前5条消息以避免日志过长
        response_text = await call_ollama(messages, model, temperature)

        # 校验返回值是否符合预期
        if not isinstance(response_text, str):
            raise ValueError(f"Ollama API 返回值无效，期望是字符串，但得到：{type(response_text)}")

        logger.info(f"Ollama 模型回复: {response_text}")
        return response_text

    except ValueError as ve:
        logger.error(f"参数校验错误: {ve}")
        return "抱歉，输入参数格式有误，请检查后重试。"

    except Exception as e:
        logger.exception(f"调用 Ollama 模型时发生错误: {e}. Messages: {messages}, Model: {model}")
        return "抱歉，我暂时无法处理您的请求。"

def get_cached_response(redis_client, cache_key: str) -> str:
    """
    从 Redis 获取缓存
    """
    try:
        if redis_client:
            cached_response = redis_client.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit for key: {cache_key}")
                return cached_response
        else:
            logger.warning("Redis client not initialized")
    except Exception as e:
        logger.error(f"Redis error while fetching cache: {e}")
    return None

def cache_response(redis_client, cache_key: str, response_text: str, ttl: int = 3600):
    """
    保存响应到 Redis
    """
    try:
        if redis_client and response_text not in ["抱歉，Ollama API 请求超时，请稍后再试。"]:
            redis_client.setex(cache_key, ttl, response_text)
            logger.info(f"Response cached successfully for key: {cache_key}")
        else:
            logger.warning(f"Invalid response not cached for key: {cache_key}")
    except Exception as e:
        logger.error(f"Redis error while caching response: {e}")

def add_to_vector_store(user_id: str, role: str, content: str):
    """
    保存单条消息到 VectorStore
    """
    try:
        vector_store.add_to_conversation(user_id, role=role, content=content)
        logger.info(f"Added {role} message to VectorStore for user {user_id}.")
    except Exception as e:
        logger.error(f"Failed to add message to VectorStore: {e}")

# 生命周期事件
@app.on_event("startup")
async def startup_event():
    """
    在应用启动时执行初始化任务
    """
    logger.info("Starting up the application...")
    if redis_client:
        try:
            redis_client.ping()
            logger.info("Redis connection is healthy.")
        except redis.ConnectionError as e:
            logger.error(f"Redis connection failed during startup: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    在应用关闭时进行清理任务
    """
    logger.info("Shutting down the application...")
    if redis_client:
        try:
            redis_client.close()
            logger.info("Redis connection closed successfully.")
        except Exception as e:
            logger.error(f"Failed to close Redis connection: {e}")

# 健康检查
@app.get("/health")
async def health_check():
    """
    健康检查接口，用于确认服务是否正常运行
    """
    redis_status = "Connected" if redis_client and redis_client.ping() else "Disconnected"

    # 检查数据库连接
    db_status = "Connected"
    try:
        db = next(get_db())
        db.execute("SELECT 1")
    except Exception as e:
        db_status = f"Error: {e}"

    return {
        "status": "ok",
        "redis": redis_status,
        "database": db_status
    }

# 核心聊天接口
@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(chat_request: ChatRequest, db: Session = Depends(get_db)):
    """
    主业务逻辑：处理聊天请求
    """
    import time
    start_time = time.time()

    try:
        logger.info(f"Received chat request: {chat_request.json()}")

        user_id = "user123"  # 从认证系统动态获取真实用户 ID
        user_input = next((msg.content for msg in chat_request.messages if msg.role == "user"), None)

        if not user_input:
            logger.error("No valid user message found in 'messages'")
            raise HTTPException(status_code=422, detail="No valid user message found in 'messages'")

        # 加载上下文历史
        conversation_history = vector_store.get_conversation_history(user_id)
        logger.info(f"Loaded conversation history for user {user_id}: {conversation_history}")

        # 将历史记录与当前用户输入合并
        full_messages = conversation_history + [{"role": "user", "content": user_input}]
        cache_key = f"chat:{user_id}:{hashlib.md5(json.dumps(full_messages, ensure_ascii=False).encode()).hexdigest()}"

        # 检查缓存是否命中
        cached_response = get_cached_response(redis_client, cache_key)
        if cached_response:
            return ChatResponse(choices=[ChatResponseChoice(
                message=ChatMessage(role="assistant", content=cached_response)
            )])

        # 调用 AI 模型生成回复
        response_text = await generate_response(full_messages, chat_request.model, chat_request.max_tokens, chat_request.temperature)
        if not response_text:
            logger.error("Failed to generate response from model")
            raise HTTPException(status_code=500, detail="Failed to generate response")

        # 保存到 VectorStore（更新对话历史）
        try:
            vector_store.add_to_conversation(user_id, role="user", content=user_input)
            vector_store.add_to_conversation(user_id, role="assistant", content=response_text)
            logger.info(f"Updated conversation history in VectorStore for user {user_id}.")
        except Exception as e:
            logger.error(f"Failed to update conversation history: {e}")

        # 存储聊天历史到数据库
        try:
            add_chat_history(db, user_id=user_id, message=user_input, response=response_text)
            logger.info("Chat history saved successfully")
        except Exception as e:
            logger.error(f"Failed to save chat history: {e}")

        # 缓存生成的响应
        cache_response(redis_client, cache_key, response_text)

        # 返回结果
        return ChatResponse(choices=[ChatResponseChoice(
            message=ChatMessage(role="assistant", content=response_text)
        )])

    except HTTPException as he:
        logger.warning(f"HTTP exception occurred: {he.detail}")
        raise he
    except Exception as e:
        logger.error(f"Unexpected error in chat_completions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        end_time = time.time()
        logger.info(f"chat_completions execution took {end_time - start_time:.2f} seconds")
