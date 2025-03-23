**README.md**
```markdown
# 🎬 Live Subtitle Translator

Traduce subtítulos en pantalla en tiempo real mientras miras películas, series o anime.

---

## 🚀 Características
- Traducción automática de subtítulos desde la pantalla.
- Captura OCR con Tesseract.
- Traducción en tiempo real usando [Gemini Pro](https://ai.google.dev/).
- Ventana flotante (overlay) sobre el video.
- Compatible con pantalla completa.
- Cache para traducciones repetidas.
- Super rápido usando multihilo.

---

## 🧩 Requisitos

Instala dependencias con:
```bash
pip install -r requirements.txt
```

Además, necesitas:
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Clave API de Gemini en `.env`:
```env
GEMINI_API_KEY=tu_clave_aqui
```

---

## 🛠 Uso
```bash
python TranslateOnline.py
```

- Por defecto traduce desde **italiano a español**.
- Puedes cambiar el idioma en el prompt dentro del código (`traducir_streaming`).

---

## 💻 Configuración
Puedes ajustar la ventana, posición, tamaño y región de captura en:
```python
REGION = {"top": 800, "left": 100, "width": 1000, "height": 120}
```

---

## 📷 Ejemplo visual
![Ejemplo](docs/demo.gif)

---

## 📄 Licencia
MIT - Haz lo que quieras con este código 😄