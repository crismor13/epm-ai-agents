# src/rag/ingest_rag_data.py

import os
import sys

# --- Imports modernos y correctos ---
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def main(api_key: str):
    """Procesa los documentos de la carpeta 'docs' y crea un Vector Store."""
    print("Iniciando la carga de documentos...")

    # Buscamos la carpeta 'docs' desde la raíz del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    docs_path = os.path.join(project_root, 'docs')
    index_path = os.path.join(project_root, 'faiss_index')
    
    print(f"Buscando documentos en: {docs_path}")
    loader = DirectoryLoader(docs_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    if not documents:
        print("Error: No se encontraron documentos PDF en la carpeta 'docs'.")
        return

    print(f"Se cargaron {len(documents)} páginas de documentos.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"Documentos divididos en {len(docs)} chunks.")

    embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    print("Creando y guardando el Vector Store en 'faiss_index'...")
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local(index_path)

    print("¡Proceso completado! El Vector Store ha sido creado exitosamente.")

if __name__ == '__main__':
    # Esta configuración permite que el script se ejecute como un módulo.
    # Añadimos la ruta raíz del proyecto para asegurar que todos los imports funcionen.
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from src.core.config import OPENAI_API_KEY
    
    if not OPENAI_API_KEY:
        print("Error: La variable de entorno OPENAI_API_KEY no está configurada en tu archivo .env")
    else:
        main(api_key=OPENAI_API_KEY)
