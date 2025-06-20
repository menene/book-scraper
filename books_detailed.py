# books_detailed.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"


def scrape_book_details(log_callback=None):
    detailed_books = []

    # Get the first page of books
    if log_callback:
        log_callback("Scraping: " + BASE_URL)

    res = requests.get(BASE_URL)
    if res.status_code != 200:
        if log_callback:
            log_callback("❌ Error al acceder a la página principal")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    books = soup.select("article.product_pod h3 a")

    for i, book in enumerate(books, start=1):
        relative_url = book["href"]
        detail_url = BASE_URL + relative_url.replace("../", "")
        if log_callback:
            log_callback(f"Scraping: {detail_url}")

        detail_res = requests.get(detail_url)
        if detail_res.status_code != 200:
            if log_callback:
                log_callback(f"⚠️ Error al acceder al detalle: {detail_url}")
            continue

        detail_soup = BeautifulSoup(detail_res.text, "html.parser")

        title = detail_soup.find("div", class_="product_main").h1.get_text(strip=True)
        price = (
            detail_soup.find("p", class_="price_color")
            .get_text(strip=True)
            .replace("Â", "")
        )
        availability = detail_soup.find("p", class_="instock availability").get_text(
            strip=True
        )
        rating = detail_soup.find("p", class_="star-rating")["class"][1]
        description_tag = detail_soup.select_one("#product_description ~ p")
        description = (
            description_tag.get_text(strip=True) if description_tag else "No disponible"
        )
        image_rel = detail_soup.find("div", class_="item active").img["src"]
        image_url = BASE_URL + image_rel.replace("../", "")

        detailed_books.append(
            {
                "Title": title,
                "Price": price,
                "Availability": availability,
                "Rating": rating,
                "Description": description,
                "Image": image_url,
            }
        )

    return detailed_books
