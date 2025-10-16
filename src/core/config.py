import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EPM_URL = "https://www.epm.com.co/clientesyusuarios/interrupciones-del-servicio/agua/"

# 1. Obtenemos la ruta absoluta del directorio donde está este archivo (src/core)
_current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Definimos la RUTA RAÍZ del proyecto (subiendo dos niveles desde src/core)
PROJECT_ROOT = os.path.abspath(os.path.join(_current_dir, "..", ".."))

# 3. Construimos una ruta absoluta y robusta hacia la carpeta faiss_index
FAISS_INDEX_PATH = os.path.join(PROJECT_ROOT, "faiss_index")