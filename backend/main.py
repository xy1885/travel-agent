from langchain_openai import ChatOpenAI
from config import api_key, tavily_api_key, base_url, model_name

llm = ChatOpenAI(
    model=model_name, temperature=0.1, openai_api_key=api_key, base_url=base_url
)

response = llm.invoke("你好吗")

print(response.content)
