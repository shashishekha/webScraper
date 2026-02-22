import requests
from bs4 import BeautifulSoup
from home.models import News

def scrape_imdb_news():
    url = "https://www.imdb.com/news/movie/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'
    }
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_items = soup.find_all('div', class_='ipc-list-card--border-line')
    for item in news_items:
        title = item.find('a', class_="ipc-link ipc-link--base sc-a25cb019-2 gRiFWC")
        description = item.find('div', class_="ipc-html-content-inner-div")
        image = item.find('img', class_="ipc-image")
        external_link = title['href']
        title = title.text.strip() if title else "No description"
        description = description.text.strip() if title else "No description"
        image = image['src']
        image_path = None

        news = {
            "title": title,
            "description": description,
            "image": image,
            "external_link": external_link}

        News.objects.create(**news)

