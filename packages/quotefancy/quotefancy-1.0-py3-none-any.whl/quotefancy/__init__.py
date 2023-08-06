# A script to get/download random quotes from
# QuoteFancy.com in form of text or images ...


import random
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


def get_quote(type: str = "text",
              download: bool = False):
    '''
    It can be used to get Random quotes from Quotefancy.com
    '''
    alltypes = ["image", "text", "img", "txt"]
    if type not in alltypes:
        raise Exception("UnSupported Type")
    if download and type == "text":
        raise Exception("Text Object cant be Downloaded.")
    link = "https://quotefancy.com/"
    content = urlopen(link)
    cl = bs(content, "html.parser",
            from_encoding="utf-8")
    fi = cl.find_all("div", "gridblock-title")
    randompage = random.choice(fi).findNext()["href"]
    ga = urlopen(randompage)
    ref = bs(ga,
             "html.parser",
             from_encoding="utf-8")
    if type == "text":
        hu = ref.find_all("a", "quote-a")
        rt = random.choice(hu).text
        return str(rt)
    imgs = ref.find_all("img", "load-lazily")
    img = random.choice(imgs)["data-original"]
    name = img.split("/")[::-1][0]
    if download:
        urllib.request.urlretrieve(img, name)
        return name
    return img
