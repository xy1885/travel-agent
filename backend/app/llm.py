from langchain.chat_models import init_chat_model
from config import api_key, model_name

llm = init_chat_model(
    api_key=api_key,
    model=model_name,
    temperature=0.1,
    extra_body={"thinking": {"type": "disabled"}},
    max_tokens=4096,
)
