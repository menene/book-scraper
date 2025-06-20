# app.py
import io
import streamlit as st
import pandas as pd
from books import scrape_all_books
from books_detailed import scrape_book_details

st.set_page_config(
    page_title="Data Scraper", layout="wide", initial_sidebar_state="expanded"
)

st.sidebar.title("🔴 Data Scraper")
option = st.sidebar.radio(
    "Selecciona una de las opciones",
    ["About", "Libros", "Detallado"],
)

# Inicializar estado
if "log_messages" not in st.session_state:
    st.session_state.log_messages = []

if "books_df" not in st.session_state:
    st.session_state.books_df = None

if option == "About":
    st.title("📘 Acerca de la aplicación")

    st.markdown(
        """
    Esta herramienta fue desarrollada para demostrar el uso de técnicas de scraping en sitios web de práctica.

    ### ¿Qué puede hacer esta app?

    - **Libros:** Obtiene todos los libros listados en [books.toscrape.com](http://books.toscrape.com) y muestra el título, precio, calificación y portada.
    - **Libros detallados:** Ingresa a cada libro individual en la primera página para extraer toda la información disponible.
    - **Exportación:** Permite exportar los resultados en formatos CSV, JSON y Excel.
    - **Historial:** Muestra un log en tiempo real del proceso de scraping, que se mantiene durante la sesión.
    
    ### Tecnologías usadas
    - `Python` y `BeautifulSoup` para el scraping
    - `Streamlit` para la interfaz gráfica
    - `pandas` para el manejo de datos
    - `openpyxl` para exportar a Excel

    ### Notas
    - Este sitio de libros es solo para pruebas, y **no representa una tienda real**.
    - Se decidió utilizar este sitio ya que éticamente no presenta ningún dilema, sino que es de uso didáctico.
    """
    )

    st.image(
        "https://raw.githubusercontent.com/menene/book-scraper/refs/heads/main/assets/purely_academic.gif"
    )


elif option == "Libros":
    st.title("Obtener todos los libros")

    col1, col2 = st.columns(2)

    if col2.button("🧹 Limpiar log", use_container_width=True):
        st.session_state.log_messages.clear()

    with st.expander("📜 Historial del scraping", expanded=True):
        log_display = st.empty()
        log_display.text("\n".join(st.session_state.log_messages))

    def streamlit_log(message):
        if message not in st.session_state.log_messages:
            st.session_state.log_messages.append(message)
        log_display.text("\n".join(st.session_state.log_messages))

    if col1.button("🏁 Iniciar", use_container_width=True):
        with st.spinner("Scraping..."):
            st.session_state.log_messages = []  # limpiar al iniciar
            books = scrape_all_books(log_callback=streamlit_log)
            df = pd.DataFrame(books)
            st.session_state.books_df = df

    # Mostrar resultados y botones si ya hay datos
    if st.session_state.books_df is not None:
        df = st.session_state.books_df

        st.success("✅ Proceso terminado")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        json = df.to_json(orient="records", force_ascii=False)

        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "📥 Descargar CSV",
                csv,
                "books_all.csv",
                "text/csv",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                "📥 Descargar JSON",
                json,
                "data.json",
                "application/json",
                use_container_width=True,
            )

        with col3:
            st.download_button(
                "📥 Descargar XLS",
                excel_buffer.getvalue(),
                "data.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

elif option == "Detallado":
    st.title("Obtener detalle de libros")

    # Inicializar log y DataFrame
    if "log_messages_details" not in st.session_state:
        st.session_state.log_messages_details = []

    if "books_detailed_df" not in st.session_state:
        st.session_state.books_detailed_df = None

    col1, col2 = st.columns(2)

    if col2.button("🧹 Limpiar log", use_container_width=True, key="clear_details_log"):
        st.session_state.log_messages_details.clear()

    with st.expander("📜 Historial del scraping", expanded=True):
        log_display_details = st.empty()
        log_display_details.text("\n".join(st.session_state.log_messages_details))

    def log_detail(message):
        if message not in st.session_state.log_messages_details:
            st.session_state.log_messages_details.append(message)
        log_display_details.text("\n".join(st.session_state.log_messages_details))

    if col1.button("🏁 Iniciar", use_container_width=True, key="start_details"):
        with st.spinner("Scraping book details..."):
            st.session_state.log_messages_details = []  # limpiar log al iniciar
            books = scrape_book_details(log_callback=log_detail)
            df = pd.DataFrame(books)
            st.session_state.books_detailed_df = df

    if st.session_state.books_detailed_df is not None:
        df = st.session_state.books_detailed_df

        st.success("✅ Proceso terminado")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        json = df.to_json(orient="records", force_ascii=False)

        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine="openpyxl")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "📥 Descargar CSV",
                csv,
                "books_details.csv",
                "text/csv",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                "📥 Descargar JSON",
                json,
                "books_details.json",
                "application/json",
                use_container_width=True,
            )

        with col3:
            st.download_button(
                "📥 Descargar XLS",
                excel_buffer.getvalue(),
                "books_details.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
