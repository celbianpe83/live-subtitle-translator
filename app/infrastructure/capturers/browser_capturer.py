from infrastructure.websocket.subtitle_ws_server import WebSocketSubtitleReceiver
from infrastructure.capturers.base.base_capturer import SubtitleCapturer

class BrowserSubtitleCapturer(SubtitleCapturer):
    def __init__(self):
        self.receiver = None

    def start(self, on_text_callback):
        """
        Inicia o receiver WebSocket com o callback de texto.
        """
        self.receiver = WebSocketSubtitleReceiver(on_text_callback)
        self.receiver.start()

    def stop(self):
        if self.receiver:
            self.receiver.stop()
