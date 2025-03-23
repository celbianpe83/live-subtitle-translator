import os
import time
import threading
import tkinter as tk
from tkinter import StringVar
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pytesseract
from PIL import Image
import mss
import concurrent.futures
import sqlite3

# --- Configuraciones iniciales ---
load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = "models/gemini-2.0-flash-lite"

# --- Región de captura de subtítulos ---
REGION = {"top": 800, "left": 100, "width": 1000, "height": 120}
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# --- Estado global ---
sub_vistos = set()
ultimo_texto = ""
ultima_actualizacion = time.time()
traducciones_cache = {}
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# --- Inicializar banco de dados SQLite com controle de concorrência ---
lock_db = threading.Lock()
db_conn = sqlite3.connect("traduciones.db", check_same_thread=False)
db_cursor = db_conn.cursor()
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS traducciones (
        filme TEXT,
        original TEXT,
        traducido TEXT,
        UNIQUE(filme, original)
    )
""")
db_conn.commit()

# --- Funções para salvar e recuperar traduções ---
def salvar_traducao_segura(filme, original, traducido):
    with lock_db:
        try:
            db_cursor.execute("INSERT OR IGNORE INTO traducciones (filme, original, traducido) VALUES (?, ?, ?)", (filme, original, traducido))
            db_conn.commit()
        except Exception as e:
            print(f"Erro ao salvar tradução: {e}")

def carregar_traduzidos_filme(filme):
    with lock_db:
        db_cursor.execute("SELECT original, traducido FROM traducciones WHERE filme = ?", (filme,))
        return dict(db_cursor.fetchall())

# --- Traducción usando streaming com Gemini ---
def traducir_streaming(texto):
    try:
        if texto in traducciones_cache:
            return traducciones_cache[texto]

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=f"Traduce al espanol lo siguiente, responde solo con la traducción:\n\n\"{texto}\""),
                ],
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

        resultado = resultado.strip()
        traducciones_cache[texto] = resultado
        salvar_traducao_segura(filme_atual.get(), texto, resultado)
        return resultado

    except Exception as e:
        return f"⚠️ Error: {e}"

# --- Criar interface gráfica ---
root = tk.Tk()
root.title("Overlay de subtítulos")
root.geometry("850x100+180+540")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.75)
root.configure(bg="black")

try:
    root.wm_attributes("-type", "dock")
except tk.TclError:
    pass

traducido_var = StringVar()
filme_atual = StringVar()

etiqueta = tk.Label(
    root,
    textvariable=traducido_var,
    font=("Helvetica", 24, "bold"),
    fg="cyan",
    bg="black",
    justify="center"
)
etiqueta.pack(fill="both", expand=True, padx=40, pady=20)

entrada_filme = tk.Entry(root, textvariable=filme_atual, font=("Helvetica", 14))
entrada_filme.place(x=10, y=5, width=400)

boton_iniciar = tk.Button(root, text="▶️ Iniciar", command=lambda: iniciar_traduccion(), font=("Helvetica", 12))
boton_iniciar.place(x=420, y=5)

# Ajustar largura

def ajustar_wrap(event):
    etiqueta.config(wraplength=event.width - 80)

root.bind("<Configure>", ajustar_wrap)

# --- Captura de pantalla y procesamiento ---
def procesar_ocr(img):
    global ultimo_texto, ultima_actualizacion
    texto = pytesseract.image_to_string(img, lang="ita").strip()

    if texto and texto.lower() != ultimo_texto.lower():
        ultimo_texto = texto
        ultima_actualizacion = time.time()
        traduccion = traducir_streaming(texto)
        traducido_var.set(traduccion)
    elif time.time() - ultima_actualizacion > 3:
        traducido_var.set("")

# --- OCR loop com concorrência ---
def capturar_y_traducir():
    traducciones_cache.update(carregar_traduzidos_filme(filme_atual.get()))
    with mss.mss() as sct:
        while True:
            captura = sct.grab(REGION)
            img = Image.frombytes("RGB", captura.size, captura.rgb)
            executor.submit(procesar_ocr, img)
            time.sleep(0.6)

# --- Controlador do botão ---
def iniciar_traduccion():
    threading.Thread(target=capturar_y_traducir, daemon=True).start()

root.mainloop()
