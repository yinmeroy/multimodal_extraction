"""多模态大模型API配置"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI配置（支持中转站）
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# 默认配置
DEFAULT_MODEL = "gpt-4o"
TEMPERATURE = 0.1
MAX_TOKENS = 2000