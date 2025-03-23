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
import concurrent.futures
import sqlite3

# --- Configuraciones iniciales ---
load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = "models/gemini-2.0-flash-lite"

REGION = {"top": 800, "left": 100, "width": 1000, "height": 120}
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# --- Estado global ---
cache = {}
nuevas_traducciones = {}
ultimo_texto = ""
ultima_actualizacion = time.time()
traduccion_color = "cyan"
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# --- Crear ventana ---
root = tk.Tk()
root.title("Overlay de subtítulos")
root.geometry("850x120+180+540")
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.wm_attributes("-alpha", 0.75)
root.configure(bg="black")

try:
    root.wm_attributes("-type", "dock")
except tk.TclError:
    pass

# --- UI Variables ---
traducido_var = StringVar()
status_var = StringVar()
titulo_var = StringVar()

# --- Etiquetas y controles ---
frame = tk.Frame(root, bg="black")
frame.pack(side="bottom", pady=5)

label_combo = tk.Label(frame, text="Selecciona filme:", bg="black", fg="white")
label_combo.grid(row=0, column=0)

combo_filmes = ttk.Combobox(frame, state="readonly")
combo_filmes.grid(row=0, column=1)
combo_filmes.set("Seleccionar filme")

entry_nuevo = tk.Entry(frame, state="disabled")
entry_nuevo.grid(row=0, column=2)

btn_play = tk.Button(frame, text="Play", state="disabled")
btn_play.grid(row=0, column=3, padx=5)

btn_stop = tk.Button(frame, text="Stop", state="disabled")
btn_stop.grid(row=0, column=4, padx=5)

status_label = tk.Label(root, textvariable=status_var, bg="black", fg="yellow")
status_label.pack(side="bottom")

etiqueta = tk.Label(root, textvariable=traducido_var, font=("Helvetica", 24, "bold"), fg="cyan", bg="black", justify="center")
etiqueta.pack(fill="both", expand=True, padx=40, pady=10)

def ajustar_wrap(event):
    etiqueta.config(wraplength=event.width - 80)

root.bind("<Configure>", ajustar_wrap)

# --- Base de datos ---
DB_FILE = "traduciones.db"

def obtener_filmes():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT filme FROM traducciones")
        filmes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return filmes
    except Exception as e:
        print("Error al obtener filmes:", e)
        return []

def cargar_cache_desde_db(nombre):
    global cache
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT original, traducido FROM traducciones WHERE filme = ?", (nombre,))
    for original, traducido in cursor.fetchall():
        cache[original.lower()] = traducido
    conn.close()

def sincronizar_traducciones(nombre):
    if not nuevas_traducciones:
        return
    status_var.set("Guardando nuevas traducciones...")
    root.update_idletasks()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        for original, traducido in nuevas_traducciones.items():
            cursor.execute("INSERT OR IGNORE INTO traducciones (filme, original, traducido) VALUES (?, ?, ?)", (nombre, original, traducido))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error al guardar:", e)
    status_var.set("")

# --- Traducción Gemini ---
def traducir_streaming(texto):
    if texto.lower() in cache:
        global traduccion_color
        traduccion_color = "yellow"
        return cache[texto.lower()]

    traduccion_color = "cyan"
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

    cache[texto.lower()] = resultado.strip()
    nuevas_traducciones[texto] = resultado.strip()
    return resultado.strip()

# --- OCR ---
def procesar_ocr(img):
    global ultimo_texto, ultima_actualizacion
    texto = pytesseract.image_to_string(img, lang="ita").strip()
    if texto and texto.lower() != ultimo_texto.lower():
        ultimo_texto = texto
        ultima_actualizacion = time.time()
        traduccion = traducir_streaming(texto)
        traducido_var.set(traduccion)
        etiqueta.config(fg=traduccion_color)
    elif time.time() - ultima_actualizacion > 3:
        traducido_var.set("")

# --- OCR Loop ---
def capturar_loop():
    with mss.mss() as sct:
        while btn_stop["state"] == "normal":
            captura = sct.grab(REGION)
            img = Image.frombytes("RGB", captura.size, captura.rgb)
            executor.submit(procesar_ocr, img)
            time.sleep(0.6)

# --- Eventos de UI ---
def iniciar():
    nombre = entry_nuevo.get().strip() if combo_filmes.get() == "Nuevo filme" else combo_filmes.get()
    if not nombre:
        return
    cargar_cache_desde_db(nombre)
    ocultar_controles()
    btn_stop.config(state="normal")
    threading.Thread(target=capturar_loop, daemon=True).start()

def detener():
    btn_stop.config(state="disabled")
    sincronizar_traducciones(titulo_var.get())
    mostrar_controles()

def ocultar_controles():
    combo_filmes.grid_remove()
    entry_nuevo.grid_remove()
    btn_play.grid_remove()

def mostrar_controles():
    combo_filmes.grid()
    entry_nuevo.grid()
    btn_play.grid()

def on_combo_change(event):
    seleccion = combo_filmes.get()
    entry_nuevo.config(state="normal" if seleccion == "Nuevo filme" else "disabled")
    btn_play.config(state="normal" if seleccion != "Seleccionar filme" or entry_nuevo.get().strip() else "disabled")
    if seleccion != "Nuevo filme":
        titulo_var.set(seleccion)

def on_entry_change(event):
    if combo_filmes.get() == "Nuevo filme":
        btn_play.config(state="normal" if entry_nuevo.get().strip() else "disabled")
        titulo_var.set(entry_nuevo.get().strip())

combo_filmes.bind("<<ComboboxSelected>>", on_combo_change)
entry_nuevo.bind("<KeyRelease>", on_entry_change)
btn_play.config(command=iniciar)
btn_stop.config(command=detener)

# --- Iniciar UI ---
opciones = ["Seleccionar filme", "Nuevo filme"] + obtener_filmes()
combo_filmes["values"] = opciones
combo_filmes.current(0)

root.mainloop()