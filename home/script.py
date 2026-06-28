import requests
from bs4 import BeautifulSoup
from home.models import News
import os, uuid
from .tasks import download_image
from playwright.sync_api import sync_playwright


def scrape_imdb_news():
    url = "https://www.imdb.com/news/movie"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        )
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)  # let any challenge resolve / JS render
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    news_items = soup.find_all('div', class_='ipc-list-card--border-line')
    # print(len(news_items))
   
    # news_items = soup.find_all('div', class_='ipc-list-card--border-line')
    for item in news_items:
        title_tag = item.find('a', attrs={'data-testid': 'item-text-with-link'})
        description_tag = item.find('div', class_="ipc-html-content-inner-div")
        image_tag = item.find('img', class_="ipc-image")

        # Skip this card if required fields are missing
        if not title_tag or not image_tag:
            continue

        external_link = title_tag['href']
        title = title_tag.text.strip() if title_tag else "No title"
        description = description_tag.text.strip() if description_tag else "No description"
        image = image_tag['src']
        image_path = None

        if image:
            image_name = f"image_{uuid.uuid4()}.jpg"
            image_path = download_image.delay(image,'downloads/',image_name)

        news = {
            "title": title,
            "description": description,
            "image": image,
            "external_link": external_link}

        News.objects.create(**news)

