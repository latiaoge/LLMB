import aiohttp  # 异步 HTTP 客户端
from typing import List, Optional, Dict
import logging

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
# 本地ollama api
DEFAULT_OLLAMA_API_URL = "http://127.0.0.1:11434/v1/chat/completions"

async def call_ollama(
    messages: List[Dict[str, str]],
    model: str = "en2.5-3bnsfw",
    temperature: float = 0.7,
    top_p: Optional[float] = None,
    api_url: str = DEFAULT_OLLAMA_API_URL,
    timeout: int = 20
) -> Optional[str]:
    """
    异步调用 Ollama API 并返回生成的响应内容。
    """
    try:
        # 参数验证
        if not isinstance(messages, list) or not all(
            isinstance(msg, dict) and "role" in msg and "content" in msg for msg in messages
        ):
            logger.error(f"Invalid messages format: {messages}")
            return "请求参数格式错误。"

        # 构建请求数据
        request_data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "temperature": temperature,
        }
        if top_p is not None:
            request_data["top_p"] = top_p

        # 打印请求数据
        logger.info(f"Request payload: {request_data}")

        # 发送异步请求
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=request_data, timeout=timeout) as response:
                response.raise_for_status()
                response_json = await response.json()

                # 解析响应
                logger.info(f"Response from API: {response_json}")
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    return response_json["choices"][0]["message"]["content"]
                else:
                    logger.error(f"Unexpected response format: {response_json}")
                    return "抱歉，我暂时无法回答您的问题。"

    except aiohttp.ClientError as e:
        logger.error(f"调用 Ollama API 出错: {e}")
        return "抱歉，我暂时无法回答您的问题。"

    except Exception as e:
        logger.error(f"未知错误: {e}")
        return "抱歉，我暂时无法回答您的问题。"
