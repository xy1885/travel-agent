from app.agent.prompts import analyze_prompt
from app.schemas import ClarificationResponse, UserInfo
from app.llm import llm

llm_with_structured = llm.with_structured_output(ClarificationResponse)

chain = analyze_prompt | llm_with_structured


def analyze_requirements(user_info: UserInfo) -> ClarificationResponse:
    """前置分析函数，用于分析用户的原始输入信息，检查是否有矛盾或者模糊描述"""
    return chain.invoke(
        {
            "user_info": user_info.model_dump_json(indent=2, exclude={"extra_info"}),
            "extra_info": user_info.extra_info,
        }
    )
