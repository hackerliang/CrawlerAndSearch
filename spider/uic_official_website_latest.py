import os
import re
import time
import django
import hashlib
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
        # print("No author")
        pass
    old = News.objects.filter(url=url)
    # print(url)
    # print(old)
    if old.count() >= 1:
        old_hash = hashlib.md5(str(old[0].content).encode('UTF-8')).hexdigest()
        new_hash = hashlib.md5(str(content).encode('UTF-8')).hexdigest()
        # print(old_hash == new_hash)
        if old_hash != new_hash:
            old_obj = News.objects.get(url=url)
            old_obj.content = content
            old_obj.save()
            print("Update new content for {}".format(title))
        else:
            print("{} exist!".format(title))
    else:
        # print(hashlib.md5(str(title).encode('UTF-8')).hexdigest())
        News.objects.create(
            title=title,
            author=author,
            url=url,
            content=content
        )
        print("New news {}".format(title))
    print("")
    # print(url)

while True:
    urls = []
    position = 0
    # while True:
    base_url = "https://uic.edu.hk/en/home/news?start="
    url = base_url + str(position)
    req = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    try:
        news_list = soup.find('tbody')('tr')
    except TypeError:
        exit(0)
    for news in news_list:
        url = news.find('a')['href']
        urls.append("https://uic.edu.hk"+url)
        # position += 15
        # print(position)
    for uuu in urls:
        get_uic_content(uuu)
    time.sleep(100)