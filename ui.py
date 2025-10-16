# ui.py

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.agent.agent_creator import create_agent_executor

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Asistente Virtual EPM",
    page_icon="💧",
    layout="centered"
)

st.title("Asistente Virtual de EPM 💧")
st.caption("Pregúntame sobre cortes de agua o consulta las guías de EPM.")

# --- Inicialización del Agente y del Historial del Chat ---
# Usamos el cache de Streamlit para no recrear el agente en cada re-render
@st.cache_resource
def load_agent():
    return create_agent_executor()

agent_executor = load_agent()

# Inicializa el historial de mensajes si no existe
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¿Cómo puedo ayudarte hoy?"}]

# --- Lógica de la Interfaz de Chat ---
# Muestra los mensajes existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura la nueva pregunta del usuario
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    # Añade la pregunta del usuario al historial y la muestra
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Genera y muestra la respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            # Llama a tu agente de LangChain
            response = agent_executor.invoke({"input": prompt})
            full_response = response.get("output", "No pude encontrar una respuesta.")
            st.markdown(full_response)
    
    # Añade la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": full_response})