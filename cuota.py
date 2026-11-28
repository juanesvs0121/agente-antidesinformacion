import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

crudo = cliente.chat.completions.with_raw_response.create(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    messages=[{"role": "user", "content": "Responde solo: ok"}],
    max_tokens=20,
)

for clave in (
    "x-ratelimit-limit-tokens",
    "x-ratelimit-remaining-tokens",
    "x-ratelimit-reset-tokens",
    "x-ratelimit-limit-requests",
    "x-ratelimit-remaining-requests",
    "x-ratelimit-reset-requests",
):
    print(f"{clave}: {crudo.headers.get(clave)}")