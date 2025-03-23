# ✨ Proyecto: Traducción de Subtítulos en Tiempo Real

Este proyecto permite capturar subtítulos desde cualquier plataforma de streaming (como Prime Video, Netflix, etc.) y traducirlos en tiempo real utilizando OCR (Tesseract) y la API de Gemini.

---

## 📦 Instalación de dependencias

### 1. Clonar el repositorio o crear el directorio del proyecto

Asegúrate de tener el archivo `TranslateOnline.py` en tu carpeta de trabajo.

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar los requisitos del proyecto

```bash
pip install -r requirements_subtitulos.txt
```

---

## 🔐 Variables de entorno

Crea un archivo `.env` en el directorio del proyecto con la siguiente variable:

```env
GEMINI_API_KEY=tu_clave_de_google_ai_aquí
```

Puedes obtener una clave de API desde [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🧠 Instalación de Tesseract

### En macOS:

```bash
brew install tesseract
```

### En Ubuntu/Debian:

```bash
sudo apt update && sudo apt install tesseract-ocr
```

### En Windows:

- Descarga desde: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Agrega la ruta del ejecutable a la variable de entorno `PATH`.
- Edita la siguiente línea en tu script si es necesario:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
```

---

## ▶️ Ejecutar la aplicación

Con todo configurado:

```bash
python TranslateOnline.py
```

Esto abrirá una ventana flotante con fondo negro que mostrará la traducción de los subtítulos que aparecen en pantalla.

---

## 📅 Características

- Traducción en tiempo real con Gemini 2.0 Flash Lite
- Cacheo de traducciones para mejor rendimiento
- OCR optimizado con Tesseract en una región de pantalla definida
- Ventana flotante sobre cualquier aplicación, incluso a pantalla completa
- Ajuste automático del texto al tamaño de ventana

---

## 🚀 Requisitos clave (resumen)

- Python 3.9+
- `tesseract` instalado y configurado
- Cuenta de Google AI con clave de API
- Dependencias listadas en `requirements_subtitulos.txt`

---

## ✅ Contribuciones

Este proyecto fue desarrollado para ayudar a personas multilingües o estudiantes de idiomas a ver contenido traducido en tiempo real.

¡Pull requests y sugerencias son bienvenidas!

---

## © Licencia

Este proyecto está disponible bajo la licencia MIT.

