from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

# Añade la raíz del proyecto al path para permitir importaciones absolutas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agent.agent_creator import create_agent_executor

app = FastAPI(
    title="Agente de IA para EPM",
    description="Un agente para responder preguntas sobre cortes de agua y guías de EPM."
)

# Creamos una instancia global del ejecutor del agente para que no se cree en cada petición
agent_executor = create_agent_executor()

class Query(BaseModel):
    """Modelo de la petición que recibirá la API."""
    pregunta: str

@app.post("/preguntar")
async def preguntar_al_agente(query: Query):
    """
    Endpoint para recibir preguntas de los usuarios y obtener una respuesta del agente.
    """
    print(f"Recibida pregunta: {query.pregunta}")

    respuesta = agent_executor.invoke({
        "input": query.pregunta
    })

    return {"respuesta": respuesta["output"]}

@app.get("/")
def read_root():
    return {"status": "El agente de EPM está listo para recibir preguntas en el endpoint /preguntar"}