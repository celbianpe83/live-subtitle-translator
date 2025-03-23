from tkinter import Tk
from domain.translation_service import TranslationService
from infrastructure.ocr import OCRCapturer
from data.repository import TranslationRepository
from ui.gui import TranslationUI

# --- Inicialización ---
db = TranslationRepository()
translator = TranslationService()
ocr = OCRCapturer(region={"top": 800, "left": 100, "width": 1000, "height": 120})
root = Tk()

# --- Funciones de control ---
def iniciar(filme):
    translator.cargar_cache(filme, db)
    ocr.start(lambda texto: translator_callback(texto, filme))

def detener():
    ocr.stop()
    translator_ui.set_texto("💾 Guardando nuevas traducciones...")
    root.update_idletasks()
    translator.sincronizar_con_db(translator_ui.get_film(), db)
    translator_ui.set_texto("")

def translator_callback(texto, filme):
    if texto:
        traducido = translator.traducir(texto, etiqueta=translator_ui.get_etiqueta())
        translator_ui.set_texto(traducido)
    else:
        translator_ui.set_texto("")

# --- UI ---
translator_ui = TranslationUI(root, iniciar, detener, db.obtener_titulos_existentes())
root.mainloop()
