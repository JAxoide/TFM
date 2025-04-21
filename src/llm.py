from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from config import OPENAI_API_KEY, MODEL_NAME
from rag import get_retriever

def get_chatbot():
    """Crea un chatbot con RAG y memoria de conversación."""
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        openai_api_key=OPENAI_API_KEY,
        temperature=0  # 0 = más preciso, 1 = más creativo
    )
    retriever = get_retriever()
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chatbot = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
    )
    
    return chatbot

def ask_question(question: str):
    """Consulta al chatbot y devuelve la respuesta, incluyendo preguntas de validación."""
    chatbot = get_chatbot()

    # Primera respuesta del chatbot
    response = chatbot.run(question)

    # Si se detectan riesgos, hacer preguntas adicionales
    follow_up_questions = generate_risk_questions(response)
    return response, follow_up_questions

def generate_risk_questions(response):
    """Genera preguntas de validación si el chatbot detecta riesgos en la respuesta."""
    risk_indicators = ["sesgo", "privacidad", "discriminación", "seguridad", "cumplimiento"]
    questions = []

    for risk in risk_indicators:
        if risk in response.lower():
            questions.append(f"🔍 ¿Puedes proporcionar más detalles sobre posibles problemas de {risk}?")

    return questions
