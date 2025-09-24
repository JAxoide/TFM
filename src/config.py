import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "Clave OPEN AI")
MODEL_NAME = "gpt-4-turbo"
VECTOR_DB_PATH = "data/vector_db"
