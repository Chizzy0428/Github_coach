from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

llm = ChatOpenAI(model=model_name, api_key=openai_api_key)

