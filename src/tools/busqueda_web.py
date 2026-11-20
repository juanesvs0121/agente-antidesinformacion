import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


def buscar_en_web(consulta: str, max_resultados: int = 5) -> dict:
    """Busca información actual en la web sobre un tema o afirmación.

    Úsala para contrastar la afirmación con medios y fuentes reales cuando
    Fact Check no tenga resultados o para ampliar el contexto. Devuelve
    título, enlace y un extracto de cada resultado.

    Args:
        consulta: texto de búsqueda, corto y específico.
        max_resultados: cantidad de resultados (máximo recomendado: 5).
    """
    try:
        cliente = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        respuesta = cliente.search(query=consulta, max_results=max_resultados)
    except Exception as e:
        return {"resultados": [], "error": f"Fallo en la búsqueda web: {e}"}

    resultados = [
        {
            "titulo": r.get("title"),
            "enlace": r.get("url"),
            "extracto": (r.get("content") or "")[:500],
        }
        for r in respuesta.get("results", [])
    ]
    return {"resultados": resultados, "error": None}