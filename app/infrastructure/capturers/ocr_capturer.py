import time
import pytesseract
from PIL import Image
import mss
import threading
from infrastructure.capturers.base.base_capturer import SubtitleCapturer  # interfaz base

class OCRCapturer(SubtitleCapturer):
    def __init__(self, region, lang="ita"):
        self.region = region
        self.lang = lang
        self.running = False
        self.last_text = ""
        self.last_time = time.time()
        self.on_text_callback = None
        pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    def start(self, on_text_callback):
        self.on_text_callback = on_text_callback
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        with mss.mss() as sct:
            while self.running:
                captura = sct.grab(self.region)
                img = Image.frombytes("RGB", captura.size, captura.rgb)
                threading.Thread(target=self._procesar, args=(img,), daemon=True).start()
                time.sleep(0.6)

    def _procesar(self, img):
        texto = pytesseract.image_to_string(img, lang=self.lang).strip()
        if texto and texto.lower() != self.last_text.lower():
            self.last_text = texto
            self.last_time = time.time()
            if self.on_text_callback:
                self.on_text_callback(texto)
        elif time.time() - self.last_time > 3:
            if self.on_text_callback:
                self.on_text_callback("")
