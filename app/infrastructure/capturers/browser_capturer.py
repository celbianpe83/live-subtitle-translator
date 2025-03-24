from infrastructure.websocket.subtitle_ws_server import WebSocketSubtitleReceiver
from infrastructure.capturers.base.base_capturer import SubtitleCapturer

class BrowserSubtitleCapturer(SubtitleCapturer):
    def __init__(self, on_texto):
        self.receiver = WebSocketSubtitleReceiver(on_texto)

    def start(self):
        self.receiver.start()

    def stop(self):
        self.receiver.stop()  # ✅ agora corretamente invoca a lógica de parada