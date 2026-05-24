from pydantic import BaseModel, Field
from enum import Enum
from typing import Set


class PersonComposition(str, Enum):
    family = "家人"
    friend = "朋友"
    company = "公司"
    couple = "情侣"


class TripStyle(str, Enum):
    """旅行偏好"""

    delicious_food = "美食"
    humanistic_landscape = "人文景观"
    natural_landscape = "自然景观"


class AccommodationPreference(str, Enum):
    """住宿偏好"""

    city_center = "繁华市区"
    aside_attraction = "景点旁"
    affordable = "经济型"


class UserInfo(BaseModel):
    location: str = Field(description="用户从该城市出发")
    target: str = Field(description="目标城市")
    day_num: int = Field(description="天数", ge=1)
    person_num: int = Field(description="旅游人数", ge=1)
    person_composition: PersonComposition = Field(description="旅行人员构成")
    has_old: bool = Field(description="是否有老人")
    has_child: bool = Field(description="是否有小孩")
    style: Set[TripStyle] = Field(default=set(), description="旅行偏好，可多选")
    budget: int = Field(description="预算，单位为人名币", gt=0)
    accommodation_preference: AccommodationPreference = Field(description="住宿偏好")
    extra_info: str = Field(default="", description="用户补充信息")
