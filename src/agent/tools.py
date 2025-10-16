from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from ..core.config import EPM_URL, OPENAI_API_KEY, FAISS_INDEX_PATH
from ..scraping.epm_scraper import fetch_interrupciones_html
from ..scraping.epm_parser import parse_interrupciones

@tool
def obtener_info_cortes_de_agua() -> str:
    """
    Útil para responder preguntas sobre interrupciones o cortes del servicio de agua.
    Consulta la página oficial de EPM para obtener información actualizada sobre las interrupciones programadas.
    """
    print("🔧 Usando la herramienta de cortes de agua...")
    html = fetch_interrupciones_html(EPM_URL)
    info = parse_interrupciones(html)
    return info

@tool
def buscar_en_guias_epm(pregunta: str) -> str:
    """
    Útil para responder preguntas generales sobre EPM que NO están relacionadas con cortes de agua.
    Busca en documentos y guías internas sobre temas como facturación, trámites, reportar daños, etc.
    """
    print("📚 Usando la herramienta de búsqueda en guías...")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # Carga el índice local de FAISS (nuestra 'memoria')
    vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    # Busca los documentos más relevantes para la pregunta
    retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # k=3 trae los 3 chunks más relevantes
    docs_relevantes = retriever.invoke(pregunta)

    # Une el contenido de los documentos relevantes en un solo string
    contexto = "\n---\n".join([doc.page_content for doc in docs_relevantes])
    return contexto