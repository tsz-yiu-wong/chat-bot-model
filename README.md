# 聊天机器人模型项目

这是一个基于 Qwen3-1.7B 模型的聊天机器人项目！


## 安装

### 方法1：使用uv（推荐）

```bash
# 安装uv（如果还没有安装）
pip install uv

# 一键安装项目依赖
uv pip install -e .
```

### 方法2：使用pip

```bash
pip install -e .
```

## 使用方法

### 🚀 启动 OpenAI 兼容 API 服务器（推荐）

```bash
# 启动服务器
chat-bot-server
#或者
python -m chat_bot_model.server
```

服务启动后：
- 📖 API 文档: http://localhost:8000/docs  
- 🔗 聊天接口: http://localhost:8000/api/v1/chat
- 📋 模型列表: http://localhost:8000/api/v1/models
- ❤️ 健康检查: http://localhost:8000/health


### 📝 运行测试脚本

```bash
# 测试 API 功能
chat-bot-test
# 或者
python -m chat_bot_model.test
```

### 💻 在代码中使用

```python
from chat_bot_model.main import load_model, generate_chat_response

# 加载模型
tokenizer, model = load_model()

# 使用新的聊天格式
messages = [
    {"role": "system", "content": "你是一个乐于助人的AI助手。"},
    {"role": "user", "content": "你好，请介绍一下你自己"}
]

response = generate_chat_response(
    tokenizer, model, messages, 
    max_tokens=512, temperature=0.7, top_p=0.8
)
print(response)
```

## 🎛️ 支持的参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `messages` | Array | - | 包含 system/user/assistant 角色的消息数组 |
| `max_tokens` | Integer | 512 | 最大生成token数 (1-4096) |
| `temperature` | Float | 0.7 | 采样温度 (0.0-2.0) |
| `top_p` | Float | 0.8 | 核采样概率 (0.0-1.0) |
| `top_k` | Integer | 20 | top-k采样 |
| `frequency_penalty` | Float | 0.0 | 频率惩罚 (-2.0 to 2.0) |
| `presence_penalty` | Float | 0.0 | 存在惩罚 (-2.0 to 2.0) |
| `repetition_penalty` | Float | 1.1 | 重复惩罚 (0.1-2.0) |

## 📁 项目结构

```
chat-bot-model/
├── chat_bot_model/          # 主包目录
│   ├── __init__.py         # 包初始化文件
│   ├── main.py             # 核心模型加载与推理模块
│   ├── server.py           # OpenAI 兼容 API 服务器
│   └── test.py             # 内置测试脚本
├── Qwen3-1.7B_quantized/   # 量化后的模型文件
├── pyproject.toml          # 项目配置文件
├── .env                    # 环境变量配置文件
├── test.txt                # 测试问题文件（自动生成）
├── test_result.txt         # 测试结果文件（自动生成）
└── README.md               # 说明文档
```

## ⚙️ 配置说明

- 模型路径：`./Qwen3-1.7B_quantized`
- 量化方式：4bit量化（适合8GB显存）
- 数据类型：float16
- 设备映射：自动
- API 端口：8000

## 🔧 环境变量

创建 `.env` 文件来配置环境变量：

```bash
# API 认证密钥（可选，如果不设置则跳过认证）
CHAT_BOT_API_KEY="your-secret-api-key"

# 前端URL白名单（可选，支持多个URL，用逗号分隔）
FRONTEND_URLS="https://your-frontend.com,https://another-frontend.com"
```

**认证逻辑说明：**
1. 如果请求的来源在 `FRONTEND_URLS` 白名单中，则跳过Token验证
2. 如果来源不在白名单或未设置白名单，则检查 `CHAT_BOT_API_KEY`
3. 如果 `CHAT_BOT_API_KEY` 未设置，则允许所有请求（开发模式）

**示例 `.env` 文件：**
```bash
# 项目根目录下创建 .env 文件
CHAT_BOT_API_KEY=your-secret-api-key-here
FRONTEND_URLS=https://chat-bot-panel.vercel.app,https://localhost:3000
```