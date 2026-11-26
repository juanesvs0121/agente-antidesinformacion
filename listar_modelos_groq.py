import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Se omiten modelos de audio y moderación, que no sirven para este agente
OMITIR = ("whisper", "orpheus", "tts", "guard")

modelos = sorted(cliente.models.list().data, key=lambda m: m.id)

print(f"{'MODELO':55} {'CONTEXTO':>10}  {'MAX. SALIDA':>11}")
for m in modelos:
    if any(palabra in m.id.lower() for palabra in OMITIR):
        continue
    contexto = getattr(m, "context_window", "?")
    salida = getattr(m, "max_completion_tokens", "?")
    print(f"{m.id:55} {str(contexto):>10}  {str(salida):>11}")