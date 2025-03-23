# 📝 CHANGELOG

## [v1.0.0] - 2025-03-23
### 🎉 Versión inicial estable

#### ✨ Nuevas características
- Interfaz gráfica flotante con `Tkinter`, control de opacidad y botones de inicio/detención.
- Traducción automática en tiempo real desde subtítulos en pantalla.
- Soporte para selección de filme y modo "nuevo filme".
- Guardado de traducciones en SQLite (`traduciones.db`).
- Colores dinámicos: amarillo si viene de cache, cian si proviene de la API.
- Persistencia de traducciones por película.

#### 🧠 Arquitectura basada en DDD
- `domain/`: Servicio de traducción (`TranslationService`)
- `data/`: Repositorio de persistencia (`TranslationRepository`)
- `infrastructure/`: Captura OCR (`OCRCapturer`)
- `ui/`: Interfaz de usuario (`TranslationUI`)
- `app.py`: Coordinador general del proyecto

#### 🛠 Mejoras técnicas
- Cache en memoria para evitar repetir consultas a la API.
- API Gemini configurada vía `.env`
- Separación limpia de responsabilidades y reutilización de código.

---

Próximas mejoras propuestas:
- Configuración de idioma y región desde la UI.
- Soporte a múltiples idiomas de entrada/salida.
- Exportación de traducciones.

---

🎯 Proyecto mantenido con ❤️ por el usuario ✨

