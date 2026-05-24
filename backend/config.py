from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")
base_url = os.getenv("BASE_URL")
model_name = os.getenv("MODEL_NAME")
