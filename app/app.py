import tkinter as tk
from domain.translation_service import TranslationService
from data.repository import TranslationRepository
from infrastructure.capturers.ocr_capturer import OCRCapturer
from ui.gui import SubtitleApp
from infrastructure.translator_adapter import GeminiTranslatorAdapter
from infrastructure.capture_factory import CaptureStrategyFactory

REGION = {"top": 800, "left": 100, "width": 1000, "height": 120}
DB_PATH = "data/traduciones.db"

class AppController:
    def __init__(self, root):
        self.root = root
        self.db = TranslationRepository(DB_PATH)
        self.translation_service = TranslationService(GeminiTranslatorAdapter())
        self.ocr = None
        self.filme_actual = None

        self.gui = SubtitleApp(root, self.on_play, self.on_stop)
        filmes = self.db.obtener_titulos_existentes()
        self.gui.set_options(filmes)
        self.capturer_factory = CaptureStrategyFactory(use_browser=True)  # altere para True se quiser testar Browser

    def on_play(self, filme):
        self.filme_actual = filme
        traducciones = self.db.obtener_traducciones_por_filme(filme)
        self.translation_service.configurar_cache(traducciones)
        self.ocr = self.capturer_factory.create(region=REGION)
        self.ocr.start(self.traducir_texto)

    def on_stop(self):
        self.gui.show_guardando()
        nuevas = self.translation_service.obtener_nuevas_traducciones()
        for original, traducido in nuevas.items():
            self.db.guardar_traduccion(self.filme_actual, original, traducido)

        self.db.conn.commit()
        self.db.conn.close()
        self.root.quit()

    def traducir_texto(self, texto):
        if not texto:
            return  # evita traducir texto vacío
        traduccion, en_cache = self.translation_service.traducir(texto)
        color = "yellow" if en_cache else "cyan"
        self.gui.set_traduccion(traduccion, color=color)


def main():
    root = tk.Tk()
    root.geometry("850x100+180+540")
    root.title("Live Subtitle Translator")
    root.configure(bg="black")
    root.overrideredirect(True)
    root.wm_attributes("-topmost", True)

    app = AppController(root)
    root.mainloop()

if __name__ == "__main__":
    main()