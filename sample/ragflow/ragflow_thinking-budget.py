# ==============================================================================
#
# Copyright (C) 2025 VastaiTech Technologies Inc.  All rights reserved.
#
# ==============================================================================
#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import os

import time

current_dir = os.path.dirname(os.path.abspath(__file__))
from core.ragflow_agent import Session
from core.llm import LLMService
from core.compression import LLMCompressor
from core.thinking_budget import ThinkingBudgetClient


def origin_services(base_url, model_name):
    llm_service = LLMService(base_url, model_name)
    return llm_service


def thinking_budget_services(base_url, tokenizer_name_or_path):
    thinking_budget_client = ThinkingBudgetClient(base_url, "EMPTY", tokenizer_name_or_path)
    return thinking_budget_client

if __name__ == "__main__":

    base_url = "http://192.168.30.127:8080"
    agent_id = "25009c4a66c811f0b60a52f6f8c18e60"
    api_key = "ragflow-U1ZWM1MTMwNTY1OTExZjA4OGQzNDYxNT"
    session = Session(base_url, agent_id, api_key)

    # model info
    llm_url = "http://192.168.30.127:8389/v1"
    model_name = "Qwen3-30B-A3B"

    # knowledges get
    question = "洗选煤意义"

    knowledges = session.ask(question, stream=True)
    # session.delete()

    knowledges = f'''你是一个乐于助人的助手，专注于知识库相关问题的解答与支持。面对用户咨询时，对用户问题结合知识库的上下文, 来生成逻辑清晰、内容详实、专业准确的回答，不要进行额外推测或联想，回答需要考虑聊天历史。
                        以下是知识库：

                        {knowledges}

                        以上是知识库。'''

    messages = [
        {
            "role": "system",
            "content": knowledges
        },
        {
            "role": "user",
            "content": question
        }
    ]

    # 添加history
    # messages.append({"role": "assistant", "content": "洗选煤意义：..."})

    '''
    origin llm service
    '''
    llm_service = origin_services(llm_url, model_name)
    llm_service.chat_stream(messages)  # Example usage

    '''
    thinking budget llm service
    '''
    llm_service = thinking_budget_services(llm_url, "/vastai/Qwen3-30B-A3B-FP8/")
    result = llm_service.chat_completion(
        model=model_name,
        messages=messages,
        thinking_budget=128,
        max_tokens=57344,
        stream=True
    )

