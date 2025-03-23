import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = "models/gemini-2.0-flash-lite"

class GeminiTranslatorAdapter:
    """
    Adaptador para traducir textos usando el modelo Gemini de Google.
    """

    def traducir(self, texto):
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=f"Traduce al español lo siguiente, responde solo con la traducción:\n\n\"{texto}\""
                    )
                ],
            )
        ]

        config = types.GenerateContentConfig(
            temperature=0.3,
            top_p=0.9,
            top_k=20,
            max_output_tokens=128,
            response_mime_type="text/plain",
        )

        resultado = ""
        for chunk in client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config
        ):
            if chunk.text:
                resultado += chunk.text

        return resultado.strip()
