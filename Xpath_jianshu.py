#!/usr/bin/env python
#coding:utf-8

from lxml import etree
import json
import requests


url="https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop"

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
}


def get_html(url):
    response=requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# 1:titles 2:description 3:Author
def get_Info(html):
    selector=etree.HTML(html)
    titles = selector.xpath('//ul[@class="note-list"]/li/div/a/text()')
    descriptions=selector.xpath('//ul[@class="note-list"]/li/div[@class="content"]/p[@class="abstract"]/text()')
    authors=selector.xpath('//ul[@class="note-list"]/li/div[@class="content"]/div[@class="meta"]/a[@class="nickname"]/text()')
    total=len(titles)
    for i in range(total):
        yield {
            'title':titles[i].strip(),
            'description':descriptions[i].strip(),
            'author':authors[i].strip()
        }

def write_to_file(content):
    with open('jianshu.txt','a+',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False)+'\n')



if __name__=='__main__':
    html=get_html(url)
    contents=get_Info(html)
    for content in contents:
        write_to_file(content)

