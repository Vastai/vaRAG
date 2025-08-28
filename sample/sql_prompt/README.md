# 生成SQL Prompt

> code: https://github.com/XGenerationLab/M-Schema/tree/main

## QuickStart

该项目基于[`M-Schema`](https://github.com/XGenerationLab/M-Schema/tree/main)生成Prompt提示词，以下为模板：

```python
prompt = """你是一名{dialect}专家，现在需要阅读并理解下面的【数据库schema】描述，以及可能用到的【参考信息】，并运用{dialect}知识生成sql语句回答【用户问题】。
【用户问题】
{question}

【数据库schema】
{db_schema}

【参考信息】
{evidence}

【用户问题】
{question}

```sql"""
```

对应的英文模板如下：
```python
prompt = """You are now a {dialect} data analyst, and you are given a database schema as follows:

【Schema】
{db_schema}

【Question】
{question}

【Evidence】
{evidence}

Please read and understand the database schema carefully, and generate an executable SQL based on the user's question and evidence. The generated SQL is protected by ```sql and ```.
"""
```

在[`generate_sql_prompt`](./generate_sql_prompt.py)中指定`db_name`、`tables`等数据库信息并运行即可生成Prompt提示词供大模型使用。