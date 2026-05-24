from langchain.agents import create_agent
from app.agent.tools import (
    search_attractions,
    search_practical_info,
    search_restaurants,
)
from app.llm import llm
from app.schemas import TravelPlan, UserInfo

agent_prompt = """你是一个旅行规划智能体助手，你的主要任务是通过工具查询旅游地点的真实信息，并且把相关信息通过结构化输出返回给用户
"""

tools = [search_restaurants, search_attractions, search_practical_info]

agent = create_agent(
    model=llm, tools=tools, system_prompt=agent_prompt, response_format=TravelPlan
)


def generate_plan(user_info: UserInfo) -> TravelPlan:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_info.model_dump_json(indent=2)}]}
    )
    # result 是 AgentState，结构化输出在 result["structured_response"] 里
    return result["structured_response"]
