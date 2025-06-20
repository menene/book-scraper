# 📚 Book Scraper

Esta aplicación desarrollada con **Streamlit** permite hacer _web scraping_ del sitio [books.toscrape.com](http://books.toscrape.com), un sitio de prueba diseñado para practicar técnicas de scraping.

## 🚀 Funcionalidades

- **Libros**: Extrae todos los libros disponibles en el sitio, página por página.
- **Detallado**: Visita cada libro listado en la primera página y extrae toda su información.
- **Log persistente**: Se muestra el historial de scraping en tiempo real y se mantiene durante toda la sesión.
- **Exportación**: Permite descargar los resultados en formato CSV, JSON y Excel.
- **Imágenes**: Las portadas de los libros se muestran directamente en la interfaz.
- **Interfaz amigable**: Diseñada para facilitar la navegación entre modos de scraping.

---

## 🧰 Tecnologías usadas

- `Python`
- `BeautifulSoup` para scraping
- `Streamlit` para la interfaz web
- `pandas` para manipulación de datos
- `openpyxl` para exportación a Excel

---

## 📦 Instalación local

```bash
git clone https://github.com/menene/book-scraper
cd book-scraper
pip install -r requirements.txt
streamlit run app.py
```

> Asegúrate de tener `Python 3.8+` instalado.

---

## 📄 Estructura del proyecto

```
book-scraper-app/
├── app.py                # Aplicación principal de Streamlit
├── books.py              # Scraper general de libros
├── books_detailed.py     # Scraper de libros con detalles individuales
├── requirements.txt      # Dependencias
└── README.md             # Este archivo
```

## ⚠️ Aviso

Este scraper se conecta a un sitio de práctica que **no representa una tienda real**. No se recomienda usar este tipo de herramientas en sitios reales sin su consentimiento explícito.
