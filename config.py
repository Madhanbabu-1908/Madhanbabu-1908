import os
from dotenv import load_dotenv

load_dotenv()

LITELLM_API_KEY = os.getenv("LITELLM_API_KEY")
LITELLM_BASE_URL = os.getenv("LITELLM_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
