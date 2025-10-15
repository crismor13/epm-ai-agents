import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EPM_URL = "https://www.epm.com.co/client/interrupciones-del-servicio-de-agua"