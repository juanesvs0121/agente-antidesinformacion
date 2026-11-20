import mimetypes
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from src.tools.busqueda_web import buscar_en_web
from src.tools.factcheck import buscar_verificaciones
from src.tools.lector_url import leer_url

load_dotenv()

# Si da error 404, tomen un nombre de modelo vigente desde Google AI Studio
MODELO = "gemini-2.5-flash"

INSTRUCCIONES = """
Eres un agente verificador de información. Tu objetivo es ayudar a las personas
a determinar qué tan confiable es una afirmación, usando evidencia y no opinión.

Procedimiento obligatorio:
1. EXTRACCIÓN: si recibes una imagen, identifica el texto visible y las
   afirmaciones verificables que contiene. Separa hechos de opiniones.
2. VERIFICACIÓN PREVIA: para cada afirmación relevante, consulta primero
   buscar_verificaciones.
3. CONTRASTE: si no hay verificaciones previas o hace falta contexto, usa
   buscar_en_web. Prefiere medios y organizaciones reconocidas.
4. LECTURA: usa leer_url sobre las fuentes más relevantes antes de citarlas.
   Si una página no se puede leer, dilo y no inventes su contenido.
5. EVALUACIÓN DE FUENTES: considera quién publica, si hay varias fuentes
   independientes y si la información es reciente.

Reglas:
- Nunca inventes fuentes, enlaces ni datos. Cita solo lo que las herramientas devolvieron.
- Si la evidencia es insuficiente, el veredicto es "No verificable". No fuerces una conclusión.
- Responde siempre en español, con tono claro y neutral.

Formato de respuesta:
**Afirmación analizada:** (resumen breve)
**Veredicto:** Respaldada / Falsa / Engañosa / Parcialmente cierta / No verificable
**Nivel de confianza:** Alto / Medio / Bajo
**Explicación:** (máximo 5 líneas, basada en la evidencia)
**Fuentes:** (lista de enlaces realmente consultados)
**Limitaciones:** (qué no pudiste comprobar)
"""

HERRAMIENTAS = [buscar_verificaciones, buscar_en_web, leer_url]

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _leer_imagen(ruta: str) -> types.Part:
    mime, _ = mimetypes.guess_type(ruta)
    if mime is None:
        mime = "image/jpeg"
    with open(ruta, "rb") as f:
        return types.Part.from_bytes(data=f.read(), mime_type=mime)


def verificar(texto: str = "", ruta_imagen: str | None = None) -> str:
    """Analiza una afirmación (texto, imagen o ambos) y devuelve el veredicto."""
    contenido = []
    if ruta_imagen:
        try:
            contenido.append(_leer_imagen(ruta_imagen))
        except OSError as e:
            return f"No se pudo abrir la imagen: {e}"
    contenido.append(texto or "Analiza las afirmaciones verificables de esta imagen.")

    config = types.GenerateContentConfig(
        system_instruction=INSTRUCCIONES,
        tools=HERRAMIENTAS,
        temperature=0.2,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            maximum_remote_calls=10
        ),
    )

    # Reintentos simples ante el límite de cuota de la capa gratuita (429)
    for intento in range(3):
        try:
            respuesta = cliente.models.generate_content(
                model=MODELO, contents=contenido, config=config
            )
            return respuesta.text or "El modelo no devolvió texto."
        except errors.APIError as e:
            if e.code == 429 and intento < 2:
                print("Límite de cuota alcanzado. Reintentando en 30 s...")
                time.sleep(30)
                continue
            return f"Error de la API de Gemini ({e.code}): {e.message}"
    return "No se pudo completar la verificación."