#!/usr/bin/env python
#coding:utf-8

import requests
import re
import json
from bs4 import BeautifulSoup

url="https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop"

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
}

def get_html(url):
    response=requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_html(html):
    soup=BeautifulSoup(html,'lxml')
    titles=[]
    descriptions=[]
    authors=[]
    title_select=soup.select('#list-container .note-list .content .title ')
    for title in title_select:
        titles.append(title.string)

    desc_select=soup.select('#list-container .note-list .content .abstract')
    for desc in desc_select:
        descriptions.append(desc.string.strip())

    author_select=soup.select('#list-container .note-list .content .meta .nickname')
    for author in author_select:
        authors.append(author.string.strip())

    length=len(titles)
    for i in range(length):
        yield {
            'title':titles[i],
            'description':descriptions[i],
            'author':authors[i]
        }

def write_to_file(content):
    with open('jianshu.txt','a+',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False)+'\n')

if __name__=='__main__':
    html=get_html(url)
    contents=parse_html(html)
    for content in contents:
        write_to_file(content)
