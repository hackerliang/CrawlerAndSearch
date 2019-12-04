import os
import time
import django
import requests
from bs4 import BeautifulSoup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ws2_project.settings")
django.setup()
from dashboard.models import News

urls = []
for r in range(1, 1000):
    urls.append('http://www.gutenberg.org/cache/epub/' + str(r) + '/pg' + str(r) + '.txt')
    r += 1


def get_txt(url):
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, "lxml")
        return soup.find('body').get_text()
    except:
        print("ERROR")
        time.sleep(100)


# for u in urls:
#     print(os.path.split(u)[-1])
#     print(get_txt(u))
# print(News.objects.filter(title='DHSS presents strategic communication lecture').count())
# pg1.txt
for u in urls:
    if os.path.split(u)[-1] == "pg10.txt":
        continue
    # print(u)
    if News.objects.filter(title="Gutenberg-2019-11-30_{}".format(os.path.split(u)[-1])).count() >= 1:
        print("Gutenberg-2019-11-30_{} already exist!".format(os.path.split(u)[-1]))
    else:
        txt = get_txt(u)
        # print(u)
        News.objects.create(
            title="Gutenberg-2019-11-30_{}".format(os.path.split(u)[-1]),
            author="Gutenberg",
            url=u,
            content=txt
        )
        print("Insert One {}".format(os.path.split(u)[-1]))
