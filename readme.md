# 🎬 TranslateOnline

Traducción automática en tiempo real de subtítulos en pantalla utilizando OCR, Google Gemini y una interfaz superpuesta.

---

## 📦 Estructura del proyecto (basado en DDD)

```
translater/
├── app.py                          # Punto de entrada
├── domain/
│   └── translation_service.py      # Lógica de traducción (cache + Gemini)
├── infrastructure/
│   └── ocr.py                      # Captura de subtítulos con OCR
├── data/
│   └── repository.py               # Acceso a la base de datos SQLite
├── ui/
│   └── gui.py                      # Interfaz gráfica con Tkinter
├── traduciones.db                  # Base de datos SQLite con las traducciones
├── .env                            # Contiene tu API KEY de Gemini (no subir)
├── .gitignore                      # Ignora archivos sensibles
├── requirements.txt                # Dependencias del proyecto
└── README.md                       # Este archivo
```

---

## 🚀 Cómo ejecutar

1. **Clona el repositorio:**
```bash
git clone <URL-del-repo>
cd translater
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Crea un archivo `.env` con tu API Key de Gemini:**
```
GEMINI_API_KEY=tu_clave_aqui
```

4. **Ejecuta el programa:**
```bash
python app.py
```

---

## 🧠 Funcionalidades

- Traduce automáticamente subtítulos desde cualquier película o serie.
- Guarda y reutiliza traducciones para mejorar velocidad.
- Modo "Nuevo filme" para agregar películas distintas.
- Traducciones se almacenan por título.
- Control de opacidad.
- Diferencia de color si proviene de caché (amarillo) o API (cian).
- Interfaz siempre al frente, incluso en modo pantalla completa.

---

## 🧱 Requisitos
- Python 3.10+
- Tesseract OCR instalado y accesible desde tu sistema:
    - macOS (via Homebrew):
      ```bash
      brew install tesseract
      ```

---

## ⚠️ Notas
- Las traducciones solo se guardan al presionar el botón **Stop**.
- La base de datos `traduciones.db` se actualiza de forma incremental.
- El modelo usado por defecto es `gemini-2.0-flash-lite` para mejor velocidad.

---

## 📄 Licencia
MIT © 2025

