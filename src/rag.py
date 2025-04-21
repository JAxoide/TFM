from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
from config import OPENAI_API_KEY, VECTOR_DB_PATH

def create_vector_db():
    """Carga documentos desde la carpeta 'data/' y crea la base de datos vectorial."""
    if not os.path.exists("data"):
        print("⚠️ No se encontró la carpeta 'data/'. Creándola...")
        os.makedirs("data")

    loader = DirectoryLoader("data/", glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("⚠️ No se encontraron documentos en 'data/'. Agrega archivos para indexar.")
        return None

    print(f"📄 Cargando {len(documents)} documentos en la base de datos vectorial...")

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    vector_db = Chroma.from_documents(docs, OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY))
    vector_db.persist()
    
    print("✅ Base de datos vectorial creada y persistida correctamente.")
    return vector_db

def get_retriever():
    """Carga la base de datos vectorial y devuelve un recuperador."""
    if not os.path.exists(VECTOR_DB_PATH):
        print("⚠️ No se encontró la base de datos vectorial. Creándola ahora...")
        create_vector_db()

    return Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)).as_retriever()
