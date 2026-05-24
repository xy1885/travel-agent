from langchain_core.tools import tool
from tavily import TavilyClient
from config import tavily_api_key

client = TavilyClient(api_key=tavily_api_key)


@tool
def search_attractions(query: str) -> str:
    """搜索景点的相关信息，返回景点相关内容"""
    response = client.search(query=f"{query} 景点 推荐 必去", max_results=5)
    results = response["results"]
    return "\n\n".join([f"【{r['title']}】\n{r['content']}" for r in results])


@tool
def search_restaurants(query: str) -> str:
    """搜索景点相关餐厅或者美食"""
    response = client.search(query=f"{query} 餐厅 美食 推荐", max_results=5)
    results = response["results"]
    return "\n\n".join([f"【{r['title']}】\n{r['content']}" for r in results])


@tool
def search_practical_info(query: str) -> str:
    """搜索目的地的交通、住宿、注意事项等实用信息"""
    response = client.search(query=f"{query} 交通 住宿 注意事项", max_results=5)
    results = response["results"]
    return "\n\n".join([f"【{r['title']}】\n{r['content']}" for r in results])
