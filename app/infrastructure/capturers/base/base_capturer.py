from abc import ABC, abstractmethod
from typing import Callable

class SubtitleCapturer(ABC):
    """
    Interface base para qualquer classe que capture subtítulos (por OCR, navegador, etc.).
    """

    @abstractmethod
    def start(self, on_text_callback: Callable[[str], None]):
        """
        Inicia a captura de subtítulos e chama o callback ao detectar novo texto.
        :param on_text_callback: Função que recebe o texto detectado.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Detém a captura de subtítulos.
        """
        pass
