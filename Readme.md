# ✦ TravelAgent — AI 智能旅行规划助手

> 基于 LangChain Agent + DeepSeek + Vue 3 的全栈 AI 应用，能够自主搜索真实旅游信息，生成个性化可视化攻略。
> 本演示采用了LangSmith分析agent运行流，具体使用时可以不配置。
> 若您使用其他厂家api_key，请自行修改 ./backend/.env 和 ./backend/config.py
> 如果使用非deepseek的key报错，请尝试把 ./backend/llm.py 内的 extra_body 参数注释掉

```
llm = init_chat_model(
    model=model_name,
    api_key=llm_api_key,
    base_url=llm_base_url,
    temperature=0.1,
    extra_body={"thinking": {"type": "disabled"}}  # DeepSeek 专用，其他模型请删除此行
)
```

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-orange)

---

## 项目亮点

### 1. Human-in-the-Loop 需求澄清机制

区别于大多数 Agent 应用"埋头执行"的方式，TravelAgent 在规划前会先分析用户的补充要求，检测其中的**模糊描述**或**与表单信息的冲突**，主动向用户确认后再继续，确保规划结果符合用户真实意图。

### 2. Agent 自主搜索 + 结构化输出解耦

规划流程分为两步：

- **Step 1**：LangChain Agent 自主调用 Tavily 搜索工具，分别获取景点、餐饮、实用信息
- **Step 2**：将搜索结果交给 LLM，通过 `with_structured_output` 生成符合 Pydantic Schema 的结构化攻略

这种解耦设计解决了 DeepSeek 在多工具场景下 `response_format` 兼容性问题，系统更稳定可控。

### 3. 可视化攻略页面

AI 输出不是冷冰冰的文字，而是渲染成完整的可视化攻略页面，包含行程时间线、景点卡片、餐厅推荐、实用信息面板。

### 4. 工程化设计

- Pydantic Schema 严格约束 LLM 输出格式，保证前端可消费
- `prompts.py` 统一管理所有 Prompt，便于迭代优化
- `schemas/__init__.py` 统一导出，模块间解耦
- IP 限流防止接口被滥用
- Prompt 注入检测保护 LLM 安全

---

## 技术栈

| 层级        | 技术                           |
| ----------- | ------------------------------ |
| LLM         | DeepSeek V4（OpenAI 兼容接口） |
| Agent 框架  | LangChain + `create_agent`     |
| 搜索工具    | Tavily Search API              |
| 后端        | FastAPI + uvicorn              |
| 数据校验    | Pydantic v2                    |
| 前端        | Vue 3 + Vite + Pinia           |
| HTTP 客户端 | Axios                          |
| 限流        | SlowAPI                        |

---

## 项目结构

```
travel-agent/
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── analyzer.py       # 需求分析，Human-in-the-Loop 核心
│   │   │   ├── planner.py        # Agent 搜索 + 结构化输出
│   │   │   ├── tools.py          # Tavily 搜索工具（景点/餐饮/实用信息）
│   │   │   ├── prompts.py        # 统一 Prompt 管理
│   │   │   └── guard.py          # Prompt 注入防护
│   │   ├── api/
│   │   │   └── routes.py         # FastAPI 路由
│   │   ├── schemas/
│   │   │   ├── travel.py         # 攻略数据结构
│   │   │   ├── clarification.py  # 澄清响应数据结构
│   │   │   └── trip_base.py      # 用户表单数据结构
│   │   └── llm.py                # LLM 单例
│   ├── main.py                   # FastAPI 入口 + 限流配置
│   ├── config.py                 # 统一配置管理
│   └── requirements.txt
└── frontend/
    └── src/
        ├── views/
        │   ├── HomeView.vue      # 表单 + 澄清 + 加载流程
        │   └── PlanView.vue      # 可视化攻略页面
        ├── stores/
        │   └── travelStore.js    # Pinia 状态管理
        ├── api/
        │   └── agent.js          # 后端请求封装
        └── router/
            └── index.js
```

---

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- uv（Python 包管理器）

### 1. 克隆项目

```bash
git clone https://github.com/xy1885/travel-agent.git
cd travel-agent
```

### 2. 配置后端环境变量

```bash
cd backend
cp .env.example .env
```

编辑 `.env`：

```env
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-v4-flash
TAVILY_API_KEY=你的 Tavily API Key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=你的 LangSmith API Key（可选）
LANGCHAIN_PROJECT=travel-agent
```

### 3. 启动后端

```bash
cd backend
uv sync
uv run run.py
```

后端启动后访问 `http://localhost:8000/docs` 查看接口文档。

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173` 开始使用。

---

## 核心流程

```
用户填写表单（出发城市、目的地、天数、预算、偏好等）
         ↓
Prompt 注入检测
         ↓
LLM 分析补充要求（analyzer.py）
         ↓
    ┌────┴────┐
  有冲突/模糊   无问题
    ↓           ↓
 返回澄清     直接规划
 用户确认
    ↓
Agent 自主搜索（planner.py）
├── search_attractions  景点信息
├── search_restaurants  餐饮推荐
└── search_practical_info  实用信息
         ↓
LLM 结构化输出（TravelPlan Schema）
         ↓
Vue 渲染可视化攻略页面
```

---

## 为什么选择链式调用而非 LangGraph？

本项目的规划流程是**线性的**：分析 → 澄清 → 搜索 → 输出，没有复杂的状态机或多 Agent 协作需求。LangChain 的链式调用已经足够，引入 LangGraph 反而会增加不必要的复杂度。

LangGraph 更适合：需要动态路由、条件分支、多 Agent 协作、持久化状态的复杂场景。

---

## API 文档

启动后端后访问 `http://localhost:8000/docs`

| 接口           | 方法 | 说明                        | 限流      |
| -------------- | ---- | --------------------------- | --------- |
| `/api/analyze` | POST | 分析用户需求，检测模糊/冲突 | 10次/分钟 |
| `/api/plan`    | POST | 生成完整旅行攻略            | 3次/分钟  |

---

## 环境变量说明

| 变量名                 | 必填 | 说明                             |
| ---------------------- | ---- | -------------------------------- |
| `DEEPSEEK_API_KEY`     | ✅   | DeepSeek API Key                 |
| `DEEPSEEK_BASE_URL`    | ✅   | DeepSeek API 地址                |
| `MODEL_NAME`           | ✅   | 模型名称，如 `deepseek-v4-flash` |
| `TAVILY_API_KEY`       | ✅   | Tavily 搜索 API Key              |
| `LANGCHAIN_TRACING_V2` | ❌   | 开启 LangSmith 追踪              |
| `LANGCHAIN_API_KEY`    | ❌   | LangSmith API Key                |
| `LANGCHAIN_PROJECT`    | ❌   | LangSmith 项目名                 |

---

## License

MIT
