import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = "models/gemini-2.0-flash-lite"

class TranslationService:
    def __init__(self):
        self.cache = {}
        self.nuevas = {}

    def traducir(self, texto, etiqueta=None):
        if texto in self.cache:
            if etiqueta:
                etiqueta.config(fg="yellow")
            return self.cache[texto]

        if etiqueta:
            etiqueta.config(fg="cyan")

        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=f"Traduce al espanol lo siguiente, responde solo con la traducción:\n\n\"{texto}\"")],
            ),
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

        traduccion = resultado.strip()
        self.cache[texto] = traduccion
        self.nuevas[texto] = traduccion
        return traduccion

    def cargar_cache(self, filme, db):
        resultados = db.obtener_traducciones_por_filme(filme)
        for original, traducido in resultados:
            self.cache[original] = traducido

    def sincronizar_con_db(self, filme, db):
        for original, traducido in self.nuevas.items():
            db.guardar_traduccion(filme, original, traducido)
        self.nuevas.clear()
