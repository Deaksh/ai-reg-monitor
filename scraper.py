import requests
from bs4 import BeautifulSoup

URL = "https://gdpr-info.eu/art-32-gdpr/"

def fetch_article():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    article = soup.find("div", {"class": "entry-content"})
    if not article:
        return []

    # grab paragraphs and list items
    elements = article.find_all(["p", "li"])
    paragraphs = [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]

    return paragraphs
