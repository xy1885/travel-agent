from langchain_core.tools import tool
from tavily import TavilyClient
from config import tavily_api_key

import os
import time

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7897"

client = TavilyClient(api_key=tavily_api_key)


def safe_search(query: str, max_retries: int = 3) -> str:
    for i in range(max_retries):
        try:
            response = client.search(query=query, max_results=3)
            results = response["results"]
            return "\n\n".join([f"【{r['title']}】\n{r['content']}" for r in results])
        except Exception as e:
            if i == max_retries - 1:
                return f"搜索失败：{str(e)}"
            time.sleep(1)


@tool
def search_attractions(query: str) -> str:
    """搜索景点的相关信息，返回景点相关内容"""
    return safe_search(query=f"{query} 景点 推荐 必去")


@tool
def search_restaurants(query: str) -> str:
    """搜索景点相关餐厅或者美食"""
    return safe_search(query=f"{query} 餐厅 美食 推荐")


@tool
def search_practical_info(query: str) -> str:
    """搜索目的地的交通、住宿、注意事项等实用信息"""
    return safe_search(query=f"{query} 交通 住宿 注意事项")
