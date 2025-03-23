from abc import ABC, abstractmethod

class SubtitleCapturer(ABC):
    """
    Interfaz base para cualquier clase que capture subtítulos (ya sea por OCR u otro método).
    """

    @abstractmethod
    def start(self):
        """
        Inicia la captura de subtítulos.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Detiene la captura de subtítulos.
        """
        pass