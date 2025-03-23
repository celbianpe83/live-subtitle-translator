import time
import pytesseract
from PIL import Image
import mss
import threading
from infrastructure.capturers.base import SubtitleCapturer  # interfaz base

class OCRCapturer(SubtitleCapturer):
    def __init__(self, region, on_texto, lang="ita"):
        self.region = region
        self.on_texto = on_texto
        self.lang = lang
        self.running = False
        self.last_text = ""
        self.last_time = time.time()
        pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

    def start(self):
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
            self.on_texto(texto)
        elif time.time() - self.last_time > 3:
            self.on_texto("")
