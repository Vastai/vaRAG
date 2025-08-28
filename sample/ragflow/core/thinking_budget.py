# ==============================================================================
#
# Copyright (C) 2025 VastaiTech Technologies Inc.  All rights reserved.
#
# ==============================================================================
#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from typing import Any, Dict, List

import openai
from transformers import AutoTokenizer


class ThinkingBudgetClient:
    def __init__(self, base_url: str, api_key: str, tokenizer_name_or_path: str):
        self.base_url = base_url
        self.api_key = api_key
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name_or_path)

        self.client = openai.OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        thinking_budget: int = 512,
        max_tokens: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        assert max_tokens > thinking_budget, f"thinking budget must be smaller than maximum new tokens. Given {max_tokens=} and {thinking_budget=}"

        # 1. first call chat completion to get reasoning content
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=thinking_budget,
            stream=False,
        )

        content = response.choices[0].message.content
        reasoning_content = response.choices[0].message.reasoning_content.strip("\n")
        if content is None:
            # reasoning content is too long
            reasoning_content = (
                f"{reasoning_content}"
                "\n\nConsidering the limited time by the user, "
                "I have to give the solution based on the thinking directly now."
            )
        reasoning_tokens_len = len(self.tokenizer.encode(reasoning_content, add_special_tokens=False))
        remaining_tokens = max_tokens - reasoning_tokens_len
        assert remaining_tokens > 0, f"remaining tokens must be positive. Given {remaining_tokens=}. Increase the max_tokens or lower the thinking_budget."

        # 2. append reasoning content to messages and call completion
        messages.append({"role": "assistant", "content": f"<think>\n{reasoning_content}\n</think>\n\n"})

        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            continue_final_message=True
        )
        response = self.client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=remaining_tokens,
            **kwargs
        )

        # print("Reasoning Content:", reasoning_content)

        for chunk in response:
            if hasattr(chunk, "choices"):
                print(chunk.choices[0].text, end="", flush=True)
            else:
                print(chunk, end="")

if __name__ == "__main__":

    tokenizer_name_or_path = "/vastai/Qwen3-0.6B/"
    client = ThinkingBudgetClient(
        base_url="http://192.168.30.127:8389/v1", # Qwen3 deployed in thinking mode
        api_key="EMPTY",
        tokenizer_name_or_path=tokenizer_name_or_path
    )

    result = client.chat_completion(
        model="Qwen3-30B-A3B",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "洗选煤意义."}
        ],
        thinking_budget=10,
        max_tokens=16384,
        stream=True
    )
