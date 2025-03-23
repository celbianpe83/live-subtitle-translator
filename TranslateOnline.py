import os
import time
import threading
import tkinter as tk
from tkinter import StringVar, ttk
from dotenv import load_dotenv
from google import genai
from google.genai import types
import pytesseract
from PIL import Image
import mss
import sqlite3

# --- Configuraciones iniciales ---
load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = "models/gemini-2.0-flash-lite"
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# --- Estado global ---
sub_vistos = set()
ultimo_texto = ""
ultima_actualizacion = time.time()
traducciones_cache = {}
nuevas_traducciones = {}
cache_cargado = False
traduciendo = False

# --- Conexión DB ---
DB_FILE = "traduciones.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS traducciones (
        filme TEXT,
        original TEXT,
        traducido TEXT,
        UNIQUE(filme, original)
    )
""")
conn.commit()

# --- Cargar nombres de filmes ---
def obtener_titulos_existentes():
    cursor.execute("SELECT DISTINCT filme FROM traducciones")
    return [row[0] for row in cursor.fetchall()]

# --- Traducción con streaming ---
def traducir_streaming(texto):
    if texto in traducciones_cache:
        etiqueta.config(fg="yellow")
        return traducciones_cache[texto]

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

    traducciones_cache[texto] = resultado.strip()
    nuevas_traducciones[texto] = resultado.strip()
    return resultado.strip()

# --- UI principal ---
root = tk.Tk()
root.title("Overlay de subtítulos")
root.geometry("850x160+180+540")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.75)
root.configure(bg="black")

try:
    root.wm_attributes("-type", "dock")
except tk.TclError:
    pass

traducido_var = StringVar()
titulo_var = StringVar()
opacidad_var = tk.DoubleVar(value=0.75)

frame_top = tk.Frame(root, bg="black")
frame_top.pack(pady=5)

# Etiqueta y Combo
tk.Label(frame_top, text="Selecciona filme:", fg="white", bg="black").grid(row=0, column=0, padx=5)
combo = ttk.Combobox(frame_top, state="readonly")
combo.grid(row=0, column=1, padx=5)
combo_opciones = ["Selecciona filme"] + obtener_titulos_existentes() + ["Nuevo filme"]
combo["values"] = combo_opciones
combo.current(0)

entry = tk.Entry(frame_top, state="disabled")
entry.grid(row=0, column=2, padx=5)

btn_play = tk.Button(frame_top, text="Play", state="disabled")
btn_play.grid(row=0, column=3, padx=5)
btn_stop = tk.Button(frame_top, text="Stop", state="disabled")
btn_stop.grid(row=0, column=4, padx=5)

scale = tk.Scale(frame_top, from_=0.3, to=1.0, resolution=0.05, orient="horizontal", variable=opacidad_var, label="Opacidad", bg="black", fg="white")
scale.grid(row=0, column=5, padx=10)

# Etiqueta de subtítulo
etiqueta = tk.Label(
    root,
    textvariable=traducido_var,
    font=("Helvetica", 24, "bold"),
    fg="cyan",
    bg="black",
    justify="center"
)
etiqueta.pack(fill="both", expand=True, padx=40, pady=10)

def ajustar_wrap(event):
    etiqueta.config(wraplength=event.width - 80)

root.bind("<Configure>", ajustar_wrap)

# Handlers
filme_actual = ""

def on_combo_change(event):
    global filme_actual
    seleccion = combo.get()
    if seleccion == "Nuevo filme":
        entry.config(state="normal")
        btn_play.config(state="disabled")
    elif seleccion != "Selecciona filme":
        entry.config(state="disabled")
        entry.delete(0, tk.END)
        filme_actual = seleccion
        btn_play.config(state="normal")
    else:
        entry.config(state="disabled")
        btn_play.config(state="disabled")

def on_entry_change(*args):
    if entry.get().strip():
        btn_play.config(state="normal")
    else:
        btn_play.config(state="disabled")

def cargar_cache_film():
    cursor.execute("SELECT original, traducido FROM traducciones WHERE filme = ?", (filme_actual,))
    for original, traducido in cursor.fetchall():
        traducciones_cache[original] = traducido

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

ocr_thread = None
ocr_running = False

def capturar_y_traducir():
    global ocr_running
    ocr_running = True
    with mss.mss() as sct:
        while ocr_running:
            captura = sct.grab({"top": 800, "left": 100, "width": 1000, "height": 120})
            img = Image.frombytes("RGB", captura.size, captura.rgb)
            threading.Thread(target=procesar_ocr, args=(img,), daemon=True).start()
            root.wm_attributes("-alpha", opacidad_var.get())
            time.sleep(0.6)

def iniciar_traduccion():
    global filme_actual, cache_cargado, ocr_thread
    if combo.get() == "Nuevo filme":
        filme_actual = entry.get().strip()
    if not filme_actual:
        return

    if not cache_cargado:
        cargar_cache_film()
        cache_cargado = True

    traducido_var.set("")
    combo.grid_remove()
    entry.grid_remove()
    btn_play.grid_remove()
    btn_stop.config(state="normal")
    threading.Thread(target=capturar_y_traducir, daemon=True).start()

def detener_traduccion():
    global ocr_running
    ocr_running = False
    if nuevas_traducciones:
        traducido_var.set("💾 Guardando nuevas traducciones...")
        root.update_idletasks()
        for original, traducido in nuevas_traducciones.items():
            try:
                cursor.execute("INSERT OR IGNORE INTO traducciones (filme, original, traducido) VALUES (?, ?, ?)", (filme_actual, original, traducido))
            except Exception as e:
                print(f"Error al guardar: {e}")
        conn.commit()
        nuevas_traducciones.clear()
    traducido_var.set("")
    combo.grid()
    entry.grid()
    btn_play.grid()
    btn_play.config(state="disabled")
    btn_stop.config(state="disabled")
    entry.config(state="disabled")
    combo.set("Selecciona filme")

combo.bind("<<ComboboxSelected>>", on_combo_change)
entry.bind("<KeyRelease>", on_entry_change)
btn_play.config(command=iniciar_traduccion)
btn_stop.config(command=detener_traduccion)

# --- Iniciar ventana ---
root.mainloop()
