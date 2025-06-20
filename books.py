# books_all.py
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/"
CATALOGUE_URL = BASE_URL + "catalogue/"


def scrape_all_books(log_callback=None):
    books = []
    page = 1
    max_pages = 100

    for page in range(1, max_pages + 1):
        url = f"{CATALOGUE_URL}page-{page}.html" if page > 1 else BASE_URL
        if log_callback:
            log_callback(f"Scraping {page}: {url}")
        res = requests.get(url)
        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, "html.parser")
        container = soup.find("ol", class_="row")
        if not container or not container.find_all("article", class_="product_pod"):
            break  # No more books to process

        for book in container.find_all("article", class_="product_pod"):
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text.strip().replace("Â", "")
            rating = book.p["class"][1]
            image_url = BASE_URL + book.img["src"].replace("../", "")

            books.append(
                {"Title": title, "Price": price, "Rating": rating, "Image": image_url}
            )

    return books
