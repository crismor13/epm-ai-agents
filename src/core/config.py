import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EPM_URL = "https://www.epm.com.co/clientesyusuarios/interrupciones-del-servicio/agua/"