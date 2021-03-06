import json
import logging

from bs4 import BeautifulSoup
import requests
import urllib

def change_news(message: dict, imgs: list, titles: list, urls: list):
    for i in range(len(message["contents"])):
        message["contents"][i]["hero"]["url"] = imgs[i]
        message["contents"][i]["body"]["contents"][0]["text"] = titles[i]
        message["contents"][i]["body"]["contents"][1]["contents"][0]["action"]["uri"] = urls[i]
    return message

def make_news(message:dict):
    fw = open('news.json', 'w')
    # ensure_ascii=Falseで文字化けの防止
    json.dump(message, fw, indent=4, ensure_ascii=False)
    logging.info("create news carousel")


def news_scraiping(url: str):
    article = ['/smash/', '/toss/', '/hairpin/', '/push/']
    news_title = []
    news_url = []
    news_image = []

    for st in article:
        url_string = url+st
        response = urllib.request.urlopen(url_string)
        soup = BeautifulSoup(response, 'lxml')

        for a in soup.find_all(class_="card__title"):
            news_title.append(a.text)
            news_url.append(a.find('a').get('href'))

        for a in soup.find_all(class_="card__img"):
            news_image.append(a.find('img').get("src"))
    return news_title, news_url, news_image
