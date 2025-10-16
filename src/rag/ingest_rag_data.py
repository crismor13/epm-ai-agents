import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from ..core.config import OPENAI_API_KEY # Importamos la key desde la config

def main():
    """Procesa los documentos de la carpeta 'docs' y crea un Vector Store."""
    print("Iniciando la carga de documentos...")

    # Carga los PDFs de la carpeta 'docs'
    loader = DirectoryLoader('docs/', glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    if not documents:
        print("No se encontraron documentos para procesar.")
        return

    print(f"Se cargaron {len(documents)} documentos.")

    # Divide los documentos en chunks más pequeños
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)
    print(f"Documentos divididos en {len(docs)} chunks.")

    # Crea los embeddings (convierte texto a vectores)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Crea el Vector Store con FAISS y lo guarda localmente
    print("Creando y guardando el Vector Store...")
    vector_store = FAISS.from_documents(docs, embeddings)
    vector_store.save_local("faiss_index") # Se creará una carpeta 'faiss_index'

    print("¡Proceso completado! El Vector Store ha sido creado.")

if __name__ == '__main__':
    # Para poder ejecutar el script, necesitamos ajustar el path de Python
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    main()