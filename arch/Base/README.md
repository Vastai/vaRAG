## Base

`Base`版本主要针对搭载八张VA16的一体机场景。在该场景下，所支持的大模型包括DS3系列和Qwen3系列。其中，DS3系列、Qwen3系列大模型部署在VA16加速卡上。而Embedding模型和Rerenk 模型可根据实际情况部署在CPU端或VA16上。

   - 如果大模型为DS3系列模型，则Embedding模型和Rerenk模型只能部署在CPU端。

   - 如果大模型为Qwen3系列模型，则Embedding模型和Rerenk模型可根据实际情况部署在CPU端或VA16上。

### DS3系列方案架构

![](../../images/arch/Base-DS3.png)

### Qwen3系列方案架构

![](../../images/arch/Base-Qwen3.png)

### 环境要求

- CPU: Intel CPU
- CPU >= 128核
- RAM >= 512 GB
- Docker >= 24.0.0 
- Docker Compose >= v2.26.1



### 安装Docker

```bash
sudo apt-get update

# 安装 apt 依赖包
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
    
# 添加 Docker 的官方 GPG 密钥
sudo curl -fsSL https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

# 使用以下指令设置稳定版仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://mirrors.ustc.edu.cn/docker-ce/linux/ubuntu/ \
 $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 
sudo apt-get update

# 安装最新版本的 Docker Engine-Community 和 containerd 
sudo apt-get install docker-ce docker-ce-cli containerd.io

docker --version
# Docker version 28.1.1, build 4eba377
```

### 安装Docker-compose

Docker Compose需高于v2.26.1版本，以下为安装方法。

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-linux-$(uname -m)" -o /usr/bin/docker-compose

sudo chmod +x /usr/bin/docker-compose

docker-compose --version
# Docker Compose version v2.26.1
```

docker-compose命令详解如下：

```bash
docker-compose up -d   # 重新构建镜像并启动
docker-compose down    # 停止并删除旧容器（如果存在）
docker-compose stop    # 停止容器（保留容器）
docker-compose start   # 后续重新启动
docker-compose logs -f vacc_ds3 # 查看logs
```

### 安装Driver

```bash
sudo apt-get install make cmake

# cmake version 3.22.1
# GNU Make 4.3

sudo chmod a+x vastai_driver_install_d3_3_v2_7_a3_0_9c31939_00.25.08.11.run

sudo ./vastai_driver_install_d3_3_v2_7_a3_0_9c31939_00.25.08.11.run install --setkoparam "dpm=1"

```

### 启动模型服务

>以下模型服务示例以 `x86 架构` 为例，ARM 架构的配置方法类似，具体请参考 [ARM 架构配置说明](./docker_model_arm/)。

**Note:** 模型服务端口可在模型服务yaml文件中查看

#### 启动Embedding模型服务和Rerank模型服务

- 如果大模型为DS3系列模型，则Embedding模型和Rerenk模型只能部署在CPU端。

- 如果大模型为Qwen3系列模型，则Embedding模型和Rerenk模型可根据实际情况部署在CPU端或VA16上。如果部署在VA16上，需先按照[VastModelZOO流程](https://github.com/Vastai/VastModelZOO/tree/develop/nlp/text2vec/bge)将模型转换为`vacc`格式。

以bge-m3/bge-reranker-v2-m3为例进行说明。 

> [bge-m3](https://huggingface.co/BAAI/bge-m3)/[bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3)模型可从huggingface上进行下载。

1. 配置Embedding模型和Rerank模型参数。

    a. 在`docker_model/docker_text2vec/.env`文件中配置模型路径等参数。

    ```
    # 基础路径
    HOST_DATA_DIR=/vastai/
    # emb/rerank模型目录的路径,模型目录下可以包含多个尺寸的模型，例如：[512,1024,2048,4096,8192]，每个尺寸是一个子目录
    HOST_EMBED_DATA_DIR=/vastai/vacc_deploy/bge-m3-vacc/
    HOST_RERANK_DATA_DIR=/vastai/vacc_deploy/bge-reranker-v2-m3-vacc/

    # 镜像设置
    TEXT2VEC_CPU_IMAGE=xprobe/xinference:v1.4.0-cpu
    TEXT2VEC_VACC_IMAGE=harbor.vastaitech.com/ai_deliver/xinference_vacc_151:AI3.0_SP9_0811
    # CPU端模型参数设置
    instance_nums=4
    embed_cpu_model_name=bge-m3
    embed_cpu_model_path=bge-m3
    rerank_cpu_model_name=bge-reranker-v2-m3
    rerank_cpu_model_path=bge-reranker-v2-m3

    # vacc端模型参数设置
    embed_model_name=bge-m3-vacc
    rerank_model_name=bge-reranker-v2-m3-vacc

    model_len=512
    embed_GPUs=0,1
    rerank_GPUs=2,3

    embed_instance_nums=2
    rerank_instance_nums=2
    ```

    b. 执行`source .env`使配置文件生效。

2. 通过docker-compose启动镜像。

   - 若大模型为Qwen3系列，`bge-m3/bge-reranker-v2-m3`模型可在VA16上运行。
        - 启动模型服务前，需按照[VastModelZOO流程](https://github.com/Vastai/VastModelZOO/tree/develop/nlp/text2vec/bge)将`bge-m3/bge-reranker-v2-m3`模型转为`vacc`格式存放在`以模型输入长度命令`的子目录下，最终放到`/vastai/vacc_deploy/bge-m3-vacc/`或`/vastai/vacc_deploy/bge-reranker-v2-m3-vacc/`目录下。
        - 转成`vacc`格式后，还需要在`vacc`模型子目录下创建文件夹`tokenizer`，并将原始模型文件中的`tokenizer_config.json`和`tokenizer.json`两个文件拷贝到`tokenizer`目录下。
        - 在`tokenizer`文件夹下还需要添加`vacc_config.json`文件。
        - `vacc_config.json`文件内容如下：具体参数值根据实际情况设置
            - batch_size：模型Batch Size。
            - max_seqlen：模型输入长度。子目录的名字，比如，加载的模型尺寸是512，batch size 1
        ```json
            {
                "batch_size": 1,
                "max_seqlen": 512 
            }
        ```
   ```BASH
   # Qwen3系列
   sudo docker-compose -f docker_model/docker_text2vec/docker-compose-vacc.yaml up -d
   ```

   - 若大模型为DS3系列，`bge-m3/bge-reranker-v2-m3`模型需在CPU端运行。

   ```BASH
   # DS3系列
   sudo docker-compose -f docker_model/docker_text2vec/docker-compose-cpu.yaml up -d
   ```

#### 启动DS3系列模型服务

以DeepSeek-V3为例进行说明。

1. 配置模型参数。

    a. 在`docker_model/docker_ds3/.env`文件中配置模型路径等参数。

    ```
    # change model path
    HOST_DATA_DIR=/vastai/
    DS3_IMAGE=harbor.vastaitech.com/ai_deliver/xinference_vacc_151:AI3.0_SP9_0811  
    # 参数设置
    model_name=deepseek-v3
    model_path=DeepSeek-V3-0324  
    ```

    b. 执行`source .env`使配置文件生效。

2. 通过docker-compose启动镜像。

   - 如果开启MTP，则执行如下指令。
   ```BASH
   # DS3系列,开mtp
   sudo docker-compose -f docker_model/docker_ds3/docker-compose-mtp.yaml up -d
   ```

    - 如果不开启MTP，则执行如下指令。
   ```BASH
   # DS3系列,不开mtp
   sudo docker-compose -f docker_model/docker_ds3/docker-compose.yaml up -d
   ```

3. 验证模型服务。

    ```
    curl http://localhost:9998/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "deepseek-v3",
        "messages": [
        {"role": "user", "content": "写一首七言绝句，主题为比熊"}
        ],
        "temperature": 0.5
    }'
            
    #{"id":"chatcmpl-ae8fd45507a7417dbb46b5c3469aca5f","object":"chat.completion","created":1751447682,"model":"deepseek-v3","choices":[{"index":0,"message"{"role":"assistant","reasoning_content":null,"content":"《咏比熊犬》  \n雪绒团卧玉阶前，  \n巧笑追风绕膝旋。  \n莫道此身无勇力，  \n蓬松尾扫一方天。  \n\n注：诗中“雪绒”喻熊犬洁白蓬松的毛发，“巧笑”拟其欢悦神态。尾句以夸张手法展现其尾巴摆动的灵动，暗喻小生灵亦有撑开自我天地的气魄，在娇憨中见昂扬之趣。","tool_calls":[]},"logprobs":null"finish_reason":"stop","stop_reason":null}],"usage":{"prompt_tokens":14,"total_tokens":117,"completion_tokens":103,"prompt_tokens_details":null}"prompt_logprobs":null}
    ```

#### 启动Qwen3系列模型服务

以Qwen3-30B-A3B-Thinking-2507-FP8为例进行说明。

1. 配置模型参数。
    a. 在`docker_model/docker_qwen3/.env`文件中配置模型路径等参数。

    ```
    # 基础路径
    HOST_DATA_DIR=/vastai/
    # 镜像设置
    xinfer_vacc_IMAGE=harbor.vastaitech.com/ai_deliver/xinference_vacc_151:AI3.0_SP9_0811
    # 模型参数设置
    model_name=qwen3
    model_path=Qwen3-30B-A3B-Thinking-2507-FP8
    # GPU_PARIS的列表数量=TP*instance_nums。TP只能为2或4。GPU_PARIS 表示卡Die ID 列表。
    GPU_PAIRS=4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31
    #tp=4
    instance_nums=7
    #tp=2时，instance_nums=14
    ```

    b. 执行`source .env`使配置文件生效。

2. 通过docker-compose启动镜像。

   -  如果TP为4，则执行如下指令。
   ```BASH
   # Qwen3系列，TP=4
   sudo docker-compose -f docker_model/docker_qwen3/docker-compose-think-tp4.yaml up -d
   ```

   -  如果TP为2，则执行如下指令。
   ```BASH
   # Qwen3系列，TP=2
   sudo docker-compose -f docker_model/docker_qwen3/docker-compose-think-tp2.yaml up -d
   ```
   >若模型为非思考模型`Qwen3-30B-A3B-Instruct-2507-FP8`,则需要使用不带`-think`的docker-compose文件。

3. 测试模型服务。

    ```bash
    curl -X POST "http://localhost:9997/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "qwen3",
        "messages": [
        {"role": "user", "content": "Tell me a joke about AI"}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
        "stream": true
    }'
    ```

### RAG with Dify

#### 启动Dify服务

   ```bash
   cd docker_dify
   sudo docker-compose up -d
   ```

在浏览器输入`http://ip/install`启动服务后，配置账户名及密码。

```
admin@vastai.com / admin / dify@123.
```
#### 接入模型

1. 选择模型供应商。

![](../../images/model/step-model.png)

2. 添加Embedding模型。

> `模型名称`和`API endpoint URL`需要和启动模型服务时配置的参数一致。具体参考[启动模型服务](./docker_model/docker_text2vec/docker-compose-vacc.yaml)。

![](../../images/model/step-model-embed.png)

3. 添加Rerank模型。

> `模型名称`和`API endpoint URL`需要和启动模型服务时配置的参数一致。具体参考[启动模型服务](./docker_model/docker_text2vec/docker-compose-vacc.yaml)。

![](../../images/model/step-model-rerank.png)

4. 添加LLM模型。以DeepSeek-V3模型为例。

> `模型名称`和`API endpoint URL`需要和启动模型服务时配置的参数一致。具体参考[启动模型服务](./docker_model/docker_ds3/docker-compose.yaml)。

![](../../images/model/step-model-llm.png)

> 配置LLM模型参数时需要把`流模式返回结果的分隔符`设置成`\r\n\r\n`

![](../../images/model/step-model-llm_1.png)





#### RAG应用

1. 创建知识库。

    ![](../../images/rag/rag-step1.png)

2. 选择数据源。

    ![](../../images/rag/rag-step2.png)

3. 导入本地文本。

    ![](../../images/rag/rag-step3.png)

4. 配置知识库。

    ![](../../images/rag/rag-step4.png)

5. 等待创建向量知识库。

    ![](../../images/rag/rag-step5.png)

6. 召回测试。

    ![](../../images/rag/rag-step6.png)

7. 导入[DSL](./config/RAG-Base.yml)。

    ![](../../images/rag/rag-step-load.png)

8. 更新编排中的LLM模型服务。

    ![](../../images/rag/rag-step8.png)

9. 添加知识库并发布应用。

    ![](../../images/rag/rag-step-add-base.png)

10. 应用对话示例。

    ![](../../images/rag/rag-base.png)

### 创建RAGFlow知识库

`RAGFlow`支持PDF中的表格、图片、公式解析，检索准确率显著高于Dify原生方案，且API无缝接入Dify外部知识库。

#### 启动RAGFlow服务

```bash
cd docker_ragflow
sudo docker-compose -f docker-compose.yml up -d
```

在浏览器输入`http://ip:8080`启动服务后，配置账户名及密码。

```
admin@vastai.com / admin / ragflow@123.
```

#### 配置RAGFlow

1. 配置模型。
   
   a. 选择模型供应商。

    ![](../../images/rag_with_ragflow/step_ragflow_1.png)

   b. 添加LLM模型。
    ![](../../images/rag_with_ragflow/step_ragflow_2-base.png)

   c. 添加Embedding模型。

    ![](../../images/rag_with_ragflow/step_ragflow_3-base.png)

   d. 添加Rerank模型。
    ![](../../images/rag_with_ragflow/step_ragflow_4-base.png)

   e. 设置默认模型。

   ![](../../images/rag_with_ragflow/step_ragflow_5-base.png)

2. 上传知识库文档。
    
    a. 创建知识库。
    ![](../../images/rag_with_ragflow/rag_ragflow_1.png)

    b. 配置知识库。
    ![](../../images/rag_with_ragflow/ragflow_knowledge.png)
    
    c. 上传数据。

    ![](../../images/rag_with_ragflow/ragflow_knowledge_2.png)

    d. 解析数据。
    ![](../../images/rag_with_ragflow/ragflow_knowledge_3.png)

3. 创建RAGFlow API密钥。

    ![](../../images/rag_with_ragflow/RAGFlow_api.png)

4. 检索测试。
    ![](../../images/rag_with_ragflow/ragflow_test.png)

5. 记录知识库ID。

    该ID会在Dify连接RAGFlow知识库时使用。

    ![](../../images/rag_with_ragflow/RAGFlow_id.png)

#### 通过Dify连接RAGFlow知识库

1. 在Dify平台配置外部知识库API。

> `API Key`为[RAGFlow API密钥](../../images/rag_with_ragflow/RAGFlow_api.png)。

![](../../images/rag_with_ragflow/RAGFlow_setting.png)

2. 连接外部知识库。

![](../../images/rag_with_ragflow/RAGFlow_dify-base.png)

3. 召回测试。

![](../../images/rag_with_ragflow/RAGFlow_dify-test.png)

4. 在编排中添加外部知识库。

![](../../images/rag_with_ragflow/RAGFlow_dify-2.png)

