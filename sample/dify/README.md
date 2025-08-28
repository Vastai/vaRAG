# Dify

> 基于Dify的全流程服务。

## Introduction

本项目主要实现dify全流程服务，包括知识库检索、LLM输出，在代码中指定以下参数即可：

```python
base_url = "http://192.168.28.113"
api_key = "app-y5ISTi4xMDIO9Zzd5BfjirCs"
with_think = False # 大模型是否包含think块输出
user = "abc-123" # 注：dify开源协议规定禁止修改logo和多租户sass改造
```