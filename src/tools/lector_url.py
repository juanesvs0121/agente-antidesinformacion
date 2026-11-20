import requests
import trafilatura

MAX_CARACTERES = 6000

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
    resultado = {"url": url, "titulo": None, "texto": "", "error": None}

    try:
        respuesta = requests.get(url, headers=ENCABEZADOS, timeout=15)
        respuesta.raise_for_status()
    except requests.RequestException as e:
        resultado["error"] = f"No se pudo descargar la página: {e}"
        return resultado

    html = respuesta.text
    texto = trafilatura.extract(html, include_comments=False, favor_precision=True)
    metadatos = trafilatura.extract_metadata(html)

    if not texto:
        resultado["error"] = "No se pudo extraer texto legible (posible muro de pago)."
        return resultado

    resultado["titulo"] = metadatos.title if metadatos else None
    resultado["texto"] = texto[:MAX_CARACTERES]
    return resultado