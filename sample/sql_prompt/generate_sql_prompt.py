import os
from schema_engine import SchemaEngine
from sqlalchemy import create_engine

def generate_sql_prompt(db_name: str, db_engine: str, tables: list):
    schema_engine = SchemaEngine(engine=db_engine, db_name=db_name, schema=db_name, include_tables=tables)
    mschema = schema_engine.mschema
    mschema_str = mschema.to_mschema()
    # print(mschema_str)
    # mschema.save(f'./{db_name}.json')

    dialect = db_engine.dialect.name
    question = ''
    evidence = ''
    nl2sqlite_template_cn = """你是一名{dialect}专家，现在需要阅读并理解下面的【数据库schema】描述，以及可能用到的【参考信息】，并运用{dialect}知识生成sql语句回答【用户问题】。
    【用户问题】
    {question}

    【数据库schema】
    {db_schema}

    【参考信息】
    {evidence}

    【用户问题】
    {question}

    ```sql""".format(dialect=dialect, question=question, db_schema=mschema_str, evidence=evidence)

    return prompt

# Replace the function call_llm() with your own function or method to interact with a LLM API.
# response = call_llm(prompt)

if __name__ == "__main__":
    db_name = 'rag'
    tables = ["benchmark_results"]
    db_engine = create_engine(f"mysql+pymysql://root:123456@10.24.73.27:3308/rag")
    prompt = generate_sql_prompt(db_name, db_engine, tables)
    print(prompt)
