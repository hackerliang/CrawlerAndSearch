import os
import re
import django
import warnings
import requests
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ws2_project.settings")
django.setup()
from dashboard.models import News

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}


def get_uic_content(url):
    req = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    title = soup.find(attrs={'itemprop':'headline'}).get_text()
    title = title.replace("\t", "")
    content = re.sub(r'/upload/', 'https://uic.edu.hk/upload/', str(soup.find(attrs={'itemprop':'articleBody'})))
    author = ''
    try:
        author = soup.find(attrs={'style':'text-align: right;'}).get_text()
    except AttributeError:
        print("No author")
        pass
    if News.objects.filter(title=title).count() >= 1:
        print("{} exist!".format(title))
    else:
        News.objects.create(
            title=title,
            author=author,
            url=url,
            body=content
        )
    print(url)


urls = []

position = 0
while True:
    base_url = "https://uic.edu.hk/en/home/news?start="
    url = base_url + str(position)
    req = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    try:
        news_list = soup.find('tbody')('tr')
    except TypeError:
        break
    for news in news_list:
        url = news.find('a')['href']
        urls.append("https://uic.edu.hk"+url)
    position += 15
    print(position)
for uuu in urls:
    get_uic_content(uuu)