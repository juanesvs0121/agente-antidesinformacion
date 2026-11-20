import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
cliente = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

respuesta = cliente.search(
    query="¿las vacunas contra el covid causan infertilidad?",
    max_results=3,
)

for r in respuesta.get("results", []):
    print("-" * 60)
    print("Título:", r.get("title"))
    print("URL:", r.get("url"))
    print("Extracto:", (r.get("content") or "")[:200])