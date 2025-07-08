import os
import aiohttp


async def ask_openrouter(prompt: str) -> str:
    """
    Se comunica con la API de OpenRouter para obtener una respuesta del modelo de IA.
    Maneja los errores de forma silenciosa, devolviendo un mensaje genérico al usuario.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "tngtech/deepseek-r1t2-chimera:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Actúas como 'Nortex', un chatbot que se presenta solo una vez. "
                    "Después de eso, hablas de manera natural, clara y útil, en español. "
                    "Evita repetir que eres un asistente o usar saludos innecesarios. "
                    "Tu objetivo es responder como una persona normal, sin ser robótico ni formal. "
                    "Prohibido usar emojis, no puedes utilizar emojis."
                    "Utilizarás respuestas muy cortas, en cualquier caso. "
                    "Cada respuesta estará limitada a un máximo de 100 "
                    "caracteres."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    friendly_error_message = "Lo siento, no he podido procesar tu solicitud " \
                             "en este momento. Por favor, inténtalo de " \
                             "nuevo más tarde."

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=json_data, timeout=30) as resp:
                if resp.status != 200:
                    return friendly_error_message
                data = await resp.json()
                return data['choices'][0]['message']['content']

    except Exception:
        return friendly_error_message