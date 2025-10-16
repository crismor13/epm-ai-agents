from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .tools import obtener_info_cortes_de_agua, buscar_en_guias_epm
from ..core.config import OPENAI_API_KEY

def create_agent_executor():
    """Crea y configura el Agente de LangChain."""

    # 1. Elige el Modelo (LLM)
    llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=OPENAI_API_KEY)

    # 2. Define el Prompt (las instrucciones)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Eres un asistente virtual de EPM muy amigable y servicial. Responde las preguntas de los usuarios de forma clara y concisa. Si la información no está en tus herramientas, indica que no pudiste encontrarla."),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 3. Define las Herramientas
    tools = [obtener_info_cortes_de_agua, buscar_en_guias_epm]

    # 4. Crea el Agente
    agent = create_openai_tools_agent(llm, tools, prompt)

    # 5. Crea el Ejecutor del Agente (AgentExecutor)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose=True nos muestra qué piensa el agente

    return agent_executor