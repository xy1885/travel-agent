from pydantic import BaseModel, Field
from typing import Optional, List, Set, Union
from enum import Enum

class Attraction(BaseModel):
    '''单个景点相关信息'''
    name:str = Field(description="景点名")
    description: str = Field(description="对于该景点的一段话描述")
    duration_hours: float = Field(description="建议游玩时长，单位为小时，必须为0.5的整数倍",ge=0.5)
    image_url: Optional[str] = Field(default=None, description="图片链接，可为空")
    tips: str = Field(description="小贴士，一句话描述，主要是对用户的提醒或者小建议，比如提前预约等")

class DayPlan(BaseModel):
    '''每日规划，包含主题和景点信息'''
    day: int = Field(description="旅行的第几天",ge=1)
    theme: str = Field(description="当天主题，如果设计多项可以分时间段说明,如'上午：植物园观光，下午：美食一条街'")
    attractions: List[Attraction]

class PriceRange(str, Enum):
    low = "$"
    mid = "$$"
    high = "$$$"

class Restaurant(BaseModel):
    '''推荐的就餐餐馆'''
    name: str = Field(description="餐馆名")
    cuisine: Optional[str] = Field(default=None, description="餐馆主打菜系，如果是混合菜系可以为空")
    price_range: PriceRange = Field(description="用$符号描述价格是贵还是便宜")
    recommendation: str = Field(description="推荐这个餐馆的理由")

class Season(str, Enum):
    spring = "春季"
    summer = "夏季"
    autumn = "秋季"
    winter = "冬季"
    all = "任意季节"
 
class PracticalInfo(BaseModel):
    best_season: Union[Set[Season], Season] = Field(description="推荐去该地点旅游的季节，可多选，'任意季节'不能和其他季节一起选")
    transportation: str = Field(description="推荐的旅行方式")
    budget_estimate: int = Field(description="预计全程旅行费用，单位为人民币",gt=0)
    tips: List[str] = Field(description="给用户的小提醒，比如提前注意天气(室外旅游)等")

class TravelPlan(BaseModel):
    '''完整旅行规划'''
    destination: str = Field(description="旅游攻略的目的地")
    duration_days : int = Field(description="旅游天数", ge=1)
    summary: str = Field(description="一句话描述此次攻略信息")
    days: List[DayPlan]
    restaurants: List[Restaurant]
    practical_info: PracticalInfo