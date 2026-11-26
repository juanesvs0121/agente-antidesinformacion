import json
import os

from dotenv import load_dotenv

from src.tools.busqueda_web import buscar_en_web
from src.tools.factcheck import buscar_verificaciones
from src.tools.lector_url import leer_url

load_dotenv()

print("LLAVES EN EL .env (solo se indica si existen, no su valor):")
for variable in ("GROQ_API_KEY", "GEMINI_API_KEY", "FACTCHECK_API_KEY", "TAVILY_API_KEY"):
    valor = os.getenv(variable)
    estado = "OK" if valor and valor.lower() != "pendiente" else "FALTA O ES PLACEHOLDER"
    print(f"  {variable}: {estado}")


def mostrar(nombre, resultado):
    print("\n" + "=" * 60)
    print(nombre)
    print(json.dumps(resultado, ensure_ascii=False, indent=2)[:1500])


mostrar("FACT CHECK", buscar_verificaciones("vacunas covid infertilidad"))
mostrar("BÚSQUEDA WEB", buscar_en_web("vacunas covid infertilidad"))
mostrar("LECTOR URL", leer_url("https://es.wikipedia.org/wiki/Colombia"))