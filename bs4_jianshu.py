#!/usr/bin/env python
#coding:utf-8

from bs4 import BeautifulSoup
import re
import requests
import json

url="https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop"

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
}

def get_html(url):
    response=requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

#1:title 2:description 3:author
def parse_html(html):
    soup=BeautifulSoup(html,'lxml')
    titles=[]
    descriptions=[]
    authors=[]
    for title in soup.find_all(class_='title'):
        titles.append(title.string)

    for desc in soup.find_all(class_="abstract"):
        descriptions.append(desc.string.strip())

    for author in soup.find_all(class_="nickname"):
        authors.append(author.string.strip())

    length=len(titles)
    for i in range(length):
        yield {
            'title':titles[i],
            'description':descriptions[i],
            'author':authors[i]
        }

def write_to_file(content):
    with open("jianshu.txt",'a+',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False)+'\n')

if __name__=='__main__':
    html=get_html(url)
    contents=parse_html(html)
    for content in contents:
        write_to_file(content)
