from infrastructure.capturers.ocr_capturer import OCRCapturer
from infrastructure.capturers.browser_capturer import BrowserSubtitleCapturer  # futura clase

class CaptureStrategyFactory:
    def __init__(self, use_browser=False):
        self.use_browser = use_browser

    def create(self, region, on_texto):
        if self.use_browser:
            return BrowserSubtitleCapturer(on_texto=on_texto)
        else:
            return OCRCapturer(region=region, on_texto=on_texto)
