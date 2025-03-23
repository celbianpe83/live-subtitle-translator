class TranslationService:
    """
    Servicio de traducción con control de caché y sincronización de nuevas traducciones.
    """

    def __init__(self, translator_adapter):
        """
        Inicializa el servicio de traducción con un adaptador externo (por ejemplo, Gemini).

        :param translator_adapter: Objeto que implementa el método traducir(texto)
        """
        self.translator = translator_adapter
        self.cache = {}
        self.nuevas = {}

    def traducir(self, texto):
        """
        Traduce el texto si no está en caché; si ya existe, lo devuelve directamente.

        :param texto: Texto original a traducir
        :return: Tuple (traduccion, en_cache: bool)
        """
        if texto in self.cache:
            return self.cache[texto], True

        traduccion = self.translator.traducir(texto)
        self.cache[texto] = traduccion
        self.nuevas[texto] = traduccion
        return traduccion, False

    def configurar_cache(self, traducciones_guardadas):
        """
        Carga traducciones anteriores desde base de datos al caché.

        :param traducciones_guardadas: Dict con claves "original" y valores "traducido"
        """
        self.cache.update(traducciones_guardadas)
        self.nuevas.clear()

    def obtener_nuevas_traducciones(self):
        """
        Devuelve solo las nuevas traducciones registradas desde la última sesión.

        :return: Dict de traducciones nuevas
        """
        return self.nuevas
