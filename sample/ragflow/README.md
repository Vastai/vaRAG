# RAGFlow Agent

> 基于RAGFlow的知识库的检索、大模型输出等流程。

## Introduction

本项目实现两种方式：

1. RAGFlow全流程服务，包括知识库检索、llm输出，代码：`ragflow_client.py`

    仅在代码中指定以下参数即可：

    ```python
    base_url = "http://192.168.30.127:8080"
    agent_id = "14a6fa6e614c11f0a3cd46159bc8723b"
    api_key = "ragflow-U1ZWM1MTMwNTY1OTExZjA4OGQzNDYxNT"
    ```

2. 基于RAGFlow搭建检索服务，获取检索结果后送进llm服务，代码入口：`ragflow_thinking-budget.py`

    此形式基础服务均在`core`文件夹下实现，包括：
    - `ragflow_agent`(知识库检索，后续可通过接口实现)服务
    - 基础`llm`服务
    - `thinking budget`模型服务(通过提前终止think过程优化思考时间过长问题)


## tools

基于RAGFlow API接口可以通过脚本实现批量上传、解析以及上传chunk功能

1. 批量上传文件。

    ```bash
    #!bin/sh
    for file in poetry/*
    do
        curl --request POST \
        --url http://10.24.73.27:8080/api/v1/datasets/e663d63e692711f0abda42288a401db2/documents \
        --header 'Content-Type: multipart/form-data' \
        --header 'Authorization: Bearer ragflow-ZhMjc4YWJlNjg4MDExZjBhZDY2NDIyOD' \
        --form 'file=@'$file 
    done
    ```

    在bash脚本中设置RAGFlow服务的IP、端口号、知识库ID以及api_key即可

2. 批量解析。

    ```python
    from ragflow_sdk import RAGFlow

    rag_object = RAGFlow(api_key="ragflow-ZhMjc4YWJlNjg4MDExZjBhZDY2NDIyOD", base_url="http://10.24.73.27:8080")

    for d in rag_object.list_datasets():
        if d.id == "33a500e2692511f0823e42288a401db2":
            dataset = d
    
    doc_num = 1281 # 文件数量

    ids = []
    for i in range(1, doc_num+1):
        for doc in dataset.list_documents(page=i, page_size=1):
            ids.append(doc.id)

    dataset.async_parse_documents(ids)

    ```


3. 上传chunks。

    ```python
    import os
    import json
    import glob
    from ragflow_sdk import RAGFlow

    rag_object = RAGFlow(api_key="ragflow-ZhMjc4YWJlNjg4MDExZjBhZDY2NDIyOD", base_url="http://10.24.73.27:8080")

    file = glob.glob("poetry/*.json")

    for d in rag_object.list_datasets():
        if d.id == "e663d63e692711f0abda42288a401db2":
            dataset = d

    doc_num = 1281

    for i in range(1, doc_num + 1):
        for doc in dataset.list_documents(page=i, page_size=1):
            print(doc.name)
            with open(os.path.join("poetry", doc.name), "r") as f:
                data = json.load(f)
                try:
                    for num in range(len(data)):
                        chunk = doc.add_chunk(content=str(data[num]))
                except:
                    pass

    ```

