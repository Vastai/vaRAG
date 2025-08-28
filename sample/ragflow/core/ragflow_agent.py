# ==============================================================================
#
# Copyright (C) 2025 VastaiTech Technologies Inc.  All rights reserved.
#
# ==============================================================================
#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import requests
import json

from ragflow_sdk import RAGFlow

class Session():
    def __init__(self, base_url, agent_id, api_key):

        '''Initialize a session with the RAGFlow API.'''
        
        self.url = f"{base_url}/api/v1/agents/{agent_id}/completions"
        self.api_key = api_key

        self.delete_url = f"{base_url}/api/v1/agents/{agent_id}/sessions"

        rag_object = RAGFlow(api_key=api_key, base_url=base_url)
        agent = rag_object.list_agents(id = agent_id)[0]
        session = agent.create_session()
        self.id = session.id

    def ask(self, question: str, stream: bool = True):
        '''Ask a question in the session.'''
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }


        payload = {
            "question": question,
            "stream": False,
            "session_id": self.id
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
            
            if "data" in response_data:
                # print("\n提取的答案：")
                return response_data["data"]["answer"]
            else:
                print("响应中未找到 'data' 字段")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP 错误: {http_err}")
            if response.text:
                print(f"错误详情: {response.text}")
        except requests.exceptions.RequestException as req_err:
            print(f"请求异常: {req_err}")
        except json.JSONDecodeError:
            print("响应不是有效的 JSON 格式")
            print(f"原始响应: {response.text}")


    def delete(self):
        '''Delete the session.'''
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "ids": [self.id]
        }

        response = requests.delete(
            self.delete_url,
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            raise Exception(f"删除会话失败，状态码: {response.status_code}")
        else:
            print("会话已成功删除")

if __name__ == "__main__":
    # Example usage
    # Replace with your actual base URL, agent ID, and API key     
    base_url = "http://192.168.30.127:8080"
    agent_id = "25009c4a66c811f0b60a52f6f8c18e60"
    api_key = "ragflow-U1ZWM1MTMwNTY1OTExZjA4OGQzNDYxNT"

    session = Session(base_url, agent_id, api_key)

    session.ask("洗选煤流程", stream=True)
    # session.delete()