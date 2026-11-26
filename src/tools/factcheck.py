import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"


def buscar_verificaciones(afirmacion: str, idioma: str = "es") -> dict:
    """Busca si una afirmación ya fue verificada por organizaciones de fact-checking.

    Úsala SIEMPRE primero para cada afirmación. Devuelve las verificaciones
    publicadas (publicador, calificación y enlace). Si no hay resultados,
    significa que nadie la ha verificado en esta base, no que sea verdadera.

    Args:
        afirmacion: texto breve de la afirmación a consultar.
        idioma: código de idioma de las verificaciones, por ejemplo 'es' o 'en'.
    """
    print(f"[herramienta] Fact Check: {afirmacion}")

    params = {
        "query": afirmacion,
        "languageCode": idioma if idioma in ("es", "en") else "es",
        "pageSize": 3,
        "key": os.getenv("FACTCHECK_API_KEY"),
    }
    try:
        respuesta = requests.get(URL, params=params, timeout=15)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except (requests.RequestException, ValueError) as e:
        return {"resultados": [], "error": f"Fallo en Fact Check API: {e}"}

    resultados = []
    for item in datos.get("claims", []):
        for revision in item.get("claimReview", []):
            resultados.append({
                "afirmacion_verificada": item.get("text"),
                "publicador": revision.get("publisher", {}).get("name"),
                "calificacion": revision.get("textualRating"),
                "enlace": revision.get("url"),
            })
    return {"resultados": resultados, "error": None}