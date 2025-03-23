import threading
import time
from infrastructure.capturers.base import SubtitleCapturer

class BrowserSubtitleCapturer(SubtitleCapturer):
    def __init__(self, on_texto):
        self.on_texto = on_texto
        self.running = False
        self.last_text = ""
        self.last_time = time.time()

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        while self.running:
            # Simulación temporal de entrada de subtítulos desde el navegador.
            texto = self._leer_subtitulo_desde_navegador()

            if texto and texto.lower() != self.last_text.lower():
                self.last_text = texto
                self.last_time = time.time()
                self.on_texto(texto)
            elif time.time() - self.last_time > 3:
                self.on_texto("")

            time.sleep(0.6)

    def _leer_subtitulo_desde_navegador(self):
        # TODO: Implementar lectura real desde navegador (por ejemplo, via extensión o WebSocket)
        return ""