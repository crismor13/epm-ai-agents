from bs4 import BeautifulSoup
import json

def parse_interrupciones(html: str) -> str:
    """Parsea el HTML para extraer la información de las interrupciones y la devuelve como un string JSON."""
    if not html:
        return "No se pudo obtener la información de la página de EPM."

    soup = BeautifulSoup(html, 'html.parser')
    interrupciones = []

    # Se buscan todos los <article> que son visibles (no tienen 'display: none').
    # La clase 'cmp-contentfragment' identifica cada bloque de interrupción.
    for item in soup.find_all('article', class_='cmp-contentfragment', style=lambda s: s is None or 'display: none' not in s):
        # Usamos selectores más específicos para encontrar el valor (<dd>) dentro de cada clase de elemento.
        # El '.get_text(strip=True)' es más robusto que '.text.strip()'
        sector = item.select_one('.cmp-contentfragment__element--sector .cmp-contentfragment__element-value')
        fecha_inicio = item.select_one('.cmp-contentfragment__element--startDate .cmp-contentfragment__element-value')
        fecha_restablecimiento = item.select_one('.cmp-contentfragment__element--restoreDate .cmp-contentfragment__element-value')
        tiempo_aproximado = item.select_one('.cmp-contentfragment__element--approximateTime .cmp-contentfragment__element-value')
        direccion = item.select_one('.cmp-contentfragment__element--address .cmp-contentfragment__element-value')
        tanque = item.select_one('.cmp-contentfragment__element--tank .cmp-contentfragment__element-value')

        # Se crea el diccionario solo si los campos esenciales existen, para evitar errores.
        if all([sector, fecha_inicio, fecha_restablecimiento]):
            interrupciones.append({
                "barrio_sector": sector.get_text(strip=True),
                "direccion": direccion.get_text(strip=True) if direccion else "No especificada",
                "fecha_inicio": fecha_inicio.get_text(strip=True),
                "fecha_restablecimiento": fecha_restablecimiento.get_text(strip=True),
                "tiempo_aproximado": tiempo_aproximado.get_text(strip=True) if tiempo_aproximado else "No especificado",
                "tanque": tanque.get_text(strip=True) if tanque else "No especificado"
            })


    if not interrupciones:
        return json.dumps({"mensaje": "No se encontraron interrupciones programadas en este momento."}, indent=2, ensure_ascii=False)

    return json.dumps(interrupciones, indent=2, ensure_ascii=False)