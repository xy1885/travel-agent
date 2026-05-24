from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class IssueType(str, Enum):
    vague = "模糊描述"
    conflict = "与表单信息冲突"


class ClarificationIssue(BaseModel):
    issue_type: IssueType = Field(description="问题类型：模糊描述或与表单信息冲突")
    original_text: str = Field(description="用户原始要求中有问题的那句话")
    explanation: str = Field(description="解释为什么这里有歧义或冲突")
    suggestion: str = Field(description="给用户的修改建议")


class ClarificationResponse(BaseModel):
    needs_clarification: bool = Field(description="是否需要用户澄清")
    issues: List[ClarificationIssue] = Field(
        default=[], description="所有模糊或冲突的问题列表"
    )
