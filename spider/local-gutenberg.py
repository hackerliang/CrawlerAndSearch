import os
import re
import django
import warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ws2_project.settings")
django.setup()
from dashboard.models import News
count = 1
for filename in os.listdir("/home/uic/Downloads/gutenberg/hackerliang-xyz-assignment4/"):
    # print(filename.replace("-", " ").replace("_", " "))
    # print()
    title = str(filename).replace("___", "\t").split("\t")[1].replace("-", " ")
    author = re.findall(".*?___", filename)[0].replace("___", "").replace("-", " ")
    with open("/home/uic/Downloads/gutenberg/hackerliang-xyz-assignment4/" + str(filename), 'r') as file:
        content = file.read()
        # print(content)
    # print(author)
    # print(title)
        if not News.objects.filter(title=title).count() >= 1:
            News.objects.create(
                title=title,
                author=author,
                content=content
            )
            print(filename)
            print(count)
        else:
            print("{} already exist!".format(title))
        count += 1