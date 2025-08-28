# ==============================================================================
#
# Copyright (C) 2025 VastaiTech Technologies Inc.  All rights reserved.
#
# ==============================================================================
#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import requests
import json

class LLMService():
    def __init__(self, base_url, model_name):
        self.url = f"{base_url}/chat/completions"
        self.model_name = model_name

    def chat_stream(self, messages):
        '''Send a chat request to the LLM.'''
        # 设置请求头

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 57344,
            "stream": True
        }

        response = requests.post(
            self.url,
            headers=headers,
            json=payload,
            stream=True
        )

        if response.status_code != 200:
            raise Exception(f"请求失败，状态码: {response.status_code}")

        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        # print(json.loads(decoded_line[5:])["choices"][0]["delta"])
                        # reasoning_content = json.loads(decoded_line[5:])["choices"][0]["delta"]["reasoning_content"]  # 跳过前5个字符
                        answer = json.loads(decoded_line[5:])["choices"][0]["delta"]["content"] # 跳过前5个字符
                        # print(reasoning_content, end='', flush=True)  # 输出推理内容并刷新缓冲区
                        print(answer, end='', flush=True)  # 输出答案并刷新缓冲区
                    except:
                        pass

        except KeyboardInterrupt:
            print("用户中断了流式请求")
        finally:
            response.close()

    def chat(self, messages):
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 57344,
            "stream": False
        }


        try:
            # 发送 POST 请求（非流式）
            response = requests.post(
                self.url,
                headers=headers,
                json=payload
            )

            response.raise_for_status()  # 自动抛出 4xx/5xx 错误
            
            # 解析 JSON 响应
            response_data = response.json()

            return response_data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP 错误: {http_err}")
            if response.text:
                print(f"错误详情: {response.text}")
        except requests.exceptions.RequestException as req_err:
            print(f"请求异常: {req_err}")
        except json.JSONDecodeError:
            print("响应不是有效的 JSON 格式")
            print(f"原始响应: {response.text}")


if __name__ == "__main__":
    base_url = "http://192.168.30.127:8389/v1"
    model_name = "Qwen3-30B-A3B"
    llm_service = LLMService(base_url, model_name)
    
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你是谁"
        }
    ]
    llm_service.chat_stream(messages)  # Example usage