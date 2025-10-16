from bs4 import BeautifulSoup
import json
from datetime import datetime

def parse_interrupciones(html: str) -> str:
    """Parsea el HTML, filtra las interrupciones para mostrar solo las futuras y las devuelve como un string JSON."""
    if not html:
        return json.dumps({"mensaje": "No se pudo obtener la información de la página de EPM."}, ensure_ascii=False)

    soup = BeautifulSoup(html, 'html.parser')
    interrupciones_futuras = []
    ahora = datetime.now()

    for item in soup.find_all('article', class_='cmp-contentfragment', style=lambda s: s is None or 'display: none' not in s):
        # 1. Encontramos el elemento HTML (esto devuelve un objeto Tag o None)
        fecha_inicio_element = item.select_one('.cmp-contentfragment__element--startDate .cmp-contentfragment__element-value')

        # 2. Si el elemento no existe, continuamos con el siguiente item del bucle
        if not fecha_inicio_element:
            continue

        # 3. Extraemos el TEXTO (string) del objeto Tag antes de usarlo.
        #    Esta es la corrección clave para el TypeError.
        fecha_inicio_str = fecha_inicio_element.get_text(strip=True)

        try:
            # 4. Ahora sí, pasamos el string limpio a strptime()
            fecha_evento = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M")

            if fecha_evento >= ahora:
                # El resto de la lógica sigue igual...
                sector = item.select_one('.cmp-contentfragment__element--sector .cmp-contentfragment__element-value')
                fecha_restablecimiento = item.select_one('.cmp-contentfragment__element--restoreDate .cmp-contentfragment__element-value')
                tiempo_aproximado = item.select_one('.cmp-contentfragment__element--approximateTime .cmp-contentfragment__element-value')
                direccion = item.select_one('.cmp-contentfragment__element--address .cmp-contentfragment__element-value')
                tanque = item.select_one('.cmp-contentfragment__element--tank .cmp-contentfragment__element-value')

                interrupciones_futuras.append({
                    "barrio_sector": sector.get_text(strip=True) if sector else "No especificado",
                    "direccion": direccion.get_text(strip=True) if direccion else "No especificada",
                    "fecha_inicio": fecha_evento.strftime("%Y-%m-%d %H:%M:%S"),
                    "fecha_restablecimiento": fecha_restablecimiento.get_text(strip=True) if fecha_restablecimiento else "No especificada",
                    "tiempo_aproximado": tiempo_aproximado.get_text(strip=True) if tiempo_aproximado else "No especificado",
                    "tanque": tanque.get_text(strip=True) if tanque else "No especificado"
                })
            else:
                break

        except ValueError:
            print(f"Aviso: Se omitió una entrada por formato de fecha no reconocido: {fecha_inicio_str}")
            continue

    if not interrupciones_futuras:
        return json.dumps({"mensaje": "No se encontraron interrupciones programadas desde hoy en adelante."}, indent=2, ensure_ascii=False)

    return json.dumps(interrupciones_futuras, indent=2, ensure_ascii=False)

