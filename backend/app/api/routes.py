from fastapi import APIRouter, HTTPException, Request
from app.schemas import UserInfo
from app.agent import analyze_requirements, generate_plan, check_prompt_injection
from app.limiter import limiter

router = APIRouter()


@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze(request: Request, user_info: UserInfo):
    if check_prompt_injection(user_info.extra_info):
        raise HTTPException(status_code=400, detail="补充要求包含非法内容")
    try:
        return await analyze_requirements(user_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


@router.post("/plan")
@limiter.limit("3/minute")
async def plan(request: Request, user_info: UserInfo):
    if check_prompt_injection(user_info.extra_info):
        raise HTTPException(status_code=400, detail="补充要求包含非法内容")

    try:
        return await generate_plan(user_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")
