# books_detailed.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

BASE_URL = "http://books.toscrape.com/"


def scrape_book_details(log_callback=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(BASE_URL)
    time.sleep(1)

    book_links = driver.find_elements(By.CSS_SELECTOR, "article.product_pod h3 a")
    book_urls = [link.get_attribute("href") for link in book_links]

    book_data = []

    for url in book_urls:
        driver.get(url)
        time.sleep(1)

        if log_callback:
            log_callback(f"Scraping book: {url}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title = soup.h1.text.strip()
        product_table = soup.select_one("table.table.table-striped")
        product_info = {
            row.th.text.strip(): row.td.text.strip()
            for row in product_table.find_all("tr")
        }
        description_tag = soup.select_one("#product_description ~ p")
        description = description_tag.text.strip() if description_tag else "N/A"
        category = soup.select("ul.breadcrumb li a")[-1].text.strip()
        image_rel_url = soup.select_one("div.item.active img")["src"]
        image_url = BASE_URL + image_rel_url.replace("../", "")

        book_data.append(
            {
                "Title": title,
                "UPC": product_info.get("UPC"),
                "Price (excl. tax)": product_info.get("Price (excl. tax)"),
                "Availability": product_info.get("Availability"),
                "Category": category,
                "Description": description,
                "Image": image_url,
            }
        )

    driver.quit()
    return book_data
