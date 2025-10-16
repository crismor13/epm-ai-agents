import httpx

def fetch_interrupciones_html(url: str) -> str:
    """Obtiene el contenido HTML de la página de interrupciones de EPM."""
    try:
        with httpx.Client() as client:
            response = client.get(url, follow_redirects=True)
            response.raise_for_status()  # Lanza un error si la petición falla
            return response.text
    except httpx.RequestError as e:
        print(f"Error al hacer la petición a la URL: {e}")
        return ""