#!/usr/bin/env python
#coding:utf-8

import json
import requests
from bs4 import BeautifulSoup
import re
from pyquery import PyQuery as pq

url="https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop"

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
}

def Get_Info(doc):
    titles=[]
    descriptions=[]
    authors=[]
    titles_query=doc('#list-container .note-list .content .title ')
    for title in titles_query.items():
        titles.append(title.text())

    descriptions_query=doc('#list-container .note-list .content .abstract')
    for desc in descriptions_query.items():
        descriptions.append(desc.text())

    authors_query=doc('#list-container .note-list .content .meta .nickname')
    for author in authors_query.items():
        authors.append(author.text())

    length=len(titles)

    for i in range(length):
        yield {
            'titles':titles[i],
            'description':descriptions[i],
            'author':authors[i]
        }

def write_to_file(content):
    with open("jianshu.txt",'a+',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False)+'\n')

if __name__=='__main__':
    doc=pq(url=url,headers=headers)
    contents=Get_Info(doc)
    for content in contents:
        write_to_file(content)



