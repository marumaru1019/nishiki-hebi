import json
import logging

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

