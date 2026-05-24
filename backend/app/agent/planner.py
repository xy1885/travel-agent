from langchain.agents import create_agent
from app.agent.tools import (
    search_attractions,
    search_practical_info,
    search_restaurants,
)
from app.llm import llm
from app.schemas import TravelPlan, UserInfo
from .prompts import agent_prompt

tools = [search_restaurants, search_attractions, search_practical_info]

agent = create_agent(model=llm, tools=tools, system_prompt=agent_prompt)


async def generate_plan(user_info: UserInfo) -> TravelPlan:
    result = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": user_info.model_dump_json(indent=2)}
            ]
        },
        config={"recursion_limit": 15},
    )
    # 第一步：拿到 Agent 的文字输出
    agent_output = result["messages"][-1].content

    # 第二步：单独调用 LLM 结构化
    structured_llm = llm.with_structured_output(TravelPlan)
    return await structured_llm.ainvoke(
        f"根据以下旅游信息生成结构化旅行规划：\n{agent_output}"
    )
