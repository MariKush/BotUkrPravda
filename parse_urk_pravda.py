import requests
from bs4 import BeautifulSoup
import validators


def fix_url(url):
    if validators.url(url):
        return url
    return "https://www.pravda.com.ua" + url


class News:
    def __init__(self, text, url, img=None):
        self.text = text
        self.url = fix_url(url)
        self.img = img

    def __repr__(self):
        return f'News(\'{self.text}\', {self.url}, {self.img})'

    def to_telegram_message(self):
        return f'<a href="{self.url}">{self.text}</a>'


def get_all_news():
    url = 'https://www.pravda.com.ua/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.find_all('div', class_='article_news_list')

    news_list = []
    for div in divs:
        img = div.find("img")
        img_url = img.get('src') if img else None

        a_tags = div.find('a')
        em = a_tags.find('em')
        if em is not None:
            em.extract()

        news = News(a_tags.text, a_tags.get('href'), img_url)
        news_list.append(news)

    return news_list


def get_last_url():
    with open("last_url", 'r') as f:
        return f.readline()


def store_last_url(url):
    with open("last_url", 'w') as f:
        return f.write(url)


def get_new_news():
    last_url = get_last_url()
    all_news = get_all_news()
    store_last_url(all_news[0].url)
    new_news = []
    for news in all_news:
        if news.url == last_url:
            break
        new_news.append(news)
    new_news.reverse()
    return new_news
