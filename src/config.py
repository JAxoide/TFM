import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
MODEL_NAME = "gpt-4-turbo"
VECTOR_DB_PATH = "data/vector_db"
