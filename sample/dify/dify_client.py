# ==============================================================================
#
# Copyright (C) 2025 VastaiTech Technologies Inc.  All rights reserved.
#
# ==============================================================================
#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import requests
import json


class DifyClient:
    def __init__(self, url, api_key, user="abc-123", with_think=True):
        self.url = url
        self.api_key = api_key
        self.user = user

        self.conversation_id = ""
        self.conversation_id = self.get_conversations()
        
        self.with_think = with_think

    def ask(self, question):
        
        '''Ask a question in the session.'''

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "inputs": {},
            "query": question,
            "response_mode": "streaming",
            "conversation_id": self.conversation_id,
            "user": self.user
        }

        response = requests.post(f"{self.url}/v1/chat-messages", headers=headers, json=data, stream=True)
        output = ""
        
        if response.status_code != 200:
            raise Exception(f"请求失败，状态码: {response.status_code}")

        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    try:
                        answer = json.loads(decoded_line[5:])["answer"]  # 跳过前5个字符
                        # print(decoded_line[5:] + "\n", end='', flush=True) 
                        
                        if self.with_think:

                            output += answer

                            if '<think>' not in output:
                                print(answer)
                            
                            if '</think>' in output:
                                if answer == "</think>":
                                    continue
                                print(answer, end='', flush=True)  # 输出答案并刷新缓冲区
                            else:
                                pass  # 输出答案并刷新缓冲区

                        else:
                            print(answer, end='', flush=True)  # 输出答案并刷新缓冲区
                    
                    except:
                        pass

        except KeyboardInterrupt:
            print("用户中断了流式请求")
        finally:
            response.close()

    def get_conversations(self, limit=20):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        get_conversations_url = f"{self.url}/v1/conversations?user={self.user}&last_id=&limit={limit}"
        response = requests.get(get_conversations_url, headers=headers).json()
        if response["data"] == []:
            self.ask("你好")
            response = requests.get(get_conversations_url, headers=headers).json()
            conversation_id = response["data"][0]["id"]
            # print(f"获取到的会话ID: {conversation_id}")
            return conversation_id
        else:
            conversation_id = response["data"][0]["id"]
            # print(f"获取到的会话ID: {conversation_id}")
            return conversation_id

if __name__ == "__main__":
    base_url = "http://192.168.28.113"
    api_key = "app-y5ISTi4xMDIO9Zzd5BfjirCs"
    with_think = False
    user = "abc-123"

    client = DifyClient(base_url, api_key, user, with_think)
    client.ask("洗选煤流程")

