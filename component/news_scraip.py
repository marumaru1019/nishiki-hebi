#!/usr/bin/env python
# coding: utf-8

# In[99]:


from bs4 import BeautifulSoup
import requests
import urllib

def scraiping():
    url='https://cu.unisys.co.jp'
    article=['/smash/','/toss/','/hairpin/','/push/']
    news_title=[]
    news_url=[]
    news_image=[]


    for st in article:
        url_string=url+st
        response=urllib.request.urlopen(url_string)
        soup=BeautifulSoup(response,'lxml')
    
        for a in soup.find_all(class_="card__title"):
            news_title.append(a.text)
            news_url.append(a.find('a').get('href'))
    
        for a in soup.find_all(class_="card__img"):
            news_image.append(a.find('img').get("src"))
    return news_title,news_url,news_image

    
   


# In[ ]:




