import time

import requests
import trafilatura

MAX_CARACTERES = 3000

ENCABEZADOS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def leer_url(url: str) -> dict:
    """Descarga una página web y devuelve su texto principal.

    Úsala para leer el contenido completo de una fuente (por ejemplo, un
    resultado de la búsqueda web) antes de citarla. Si hay muro de pago o
    la página bloquea la descarga, el campo 'error' lo indica.

    Args:
        url: dirección completa de la página, con https://.
    """
    print(f"[herramienta] Leyendo URL: {url}")
    resultado = {"url": url, "titulo": None, "texto": "", "error": None}

    respuesta = None
    for intento in range(2):  # un reintento ante fallos de red intermitentes
        try:
            respuesta = requests.get(url, headers=ENCABEZADOS, timeout=15)
            respuesta.raise_for_status()
            break
        except requests.RequestException as e:
            if intento == 1:
                resultado["error"] = f"No se pudo descargar la página: {e}"
                return resultado
            time.sleep(2)

    html = respuesta.text
    texto = trafilatura.extract(html, include_comments=False, favor_precision=True)
    metadatos = trafilatura.extract_metadata(html)

    if not texto:
        resultado["error"] = "No se pudo extraer texto legible (posible muro de pago)."
        return resultado

    resultado["titulo"] = metadatos.title if metadatos else None
    resultado["texto"] = texto[:MAX_CARACTERES]
    return resultado