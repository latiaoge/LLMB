import requests

# FastAPI 服务的 URL
FASTAPI_URL = "http://127.0.0.1:11405/v1/chat/completions"

# 发送消息到 FastAPI 服务
def send_message(messages):
    """
    发送消息到 FastAPI 服务，并返回模型的回复。

    :param messages: 消息列表，格式为 [{"role": "user", "content": "你的消息"}]
    :return: 模型的回复内容
    """
    payload = {
        "model": "qwen2.5-3bnsfw",  # 固定的模型名称
        "messages": messages,
        "max_tokens": 100,  # 默认参数
        "temperature": 0.7,  # 默认参数
        "stream": False  # 默认参数
    }

    # 发送 POST 请求
    response = requests.post(FASTAPI_URL, json=payload)
    response_data = response.json()

    # 检查并返回响应
    if "choices" in response_data and len(response_data["choices"]) > 0:
        return response_data["choices"][0]["message"]["content"]

    return "没有收到有效的回复。"

if __name__ == "__main__":
    print("欢迎使用简单聊天应用！")

    while True:
        user_input = input("你: ")
        if user_input.lower() in ["退出", "exit", "quit"]:
            print("聊天结束。")
            break

        messages = [{"role": "user", "content": user_input}]
        reply = send_message(messages)
        print("AI: ", reply)
