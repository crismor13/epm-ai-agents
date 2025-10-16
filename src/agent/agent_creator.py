from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# Importamos el componente de memoria
from langchain.memory import ConversationBufferMemory

from .tools import obtener_info_cortes_de_agua, buscar_en_guias_epm
from ..core.config import OPENAI_API_KEY

# La memoria se debe crear fuera para que persista entre llamadas
# NOTA: En una aplicación real con múltiples usuarios, gestionarías una memoria por cada sesión de usuario.
# Una memoria global es suficiente para la demostración.
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def create_agent_executor():
    """Crea y configura el Agente de LangChain con memoria."""
    
    llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=OPENAI_API_KEY)

    # --- CAMBIO PRINCIPAL: Añadimos el placeholder para la memoria ---
    # Este placeholder le dice al agente dónde inyectar el historial de la conversación.
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente virtual de EPM muy amigable y servicial. Responde las preguntas de los usuarios de forma clara y concisa. Si la información no está en tus herramientas, indica que no pudiste encontrarla."),
        MessagesPlaceholder(variable_name="chat_history"), # <-- NUEVO
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    tools = [obtener_info_cortes_de_agua, buscar_en_guias_epm]
    
    agent = create_openai_tools_agent(llm, tools, prompt)

    # --- CAMBIO PRINCIPAL: Añadimos la memoria al ejecutor ---
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory, # <-- NUEVO
        verbose=True
    )

    return agent_executor