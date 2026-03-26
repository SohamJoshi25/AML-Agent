
from langchain_openai import ChatOpenAI
from config.settings import LLM_MODEL
from dotenv import load_dotenv

load_dotenv()
def get_llm():
    return ChatOpenAI(model=LLM_MODEL,temperature=0)