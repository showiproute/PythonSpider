#!/usr/bin/env python
#coding:utf-8

import requests
import re
import json
import time

url="https://www.jianshu.com/trending/monthly?utm_medium=index-banner-s&utm_source=desktop"

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
}

def get_html(url):
    response=requests.get(url,headers=headers)
    if response.status_code==200:
        return response.text
    return None

#1:title 2:description 3:author 4:comment 5:likes 6:coin
def parse_html(html):
    pattern=re.compile('<a class="title".*?">(.*?)</a>.*?<p class="abstract">(.*?)</p>.*?\
<a class="nickname".*?>(.*?)</a>\
.*?<i class="iconfont ic-list-comments.*?></i>(.*?)</a>\
.*?<i class="iconfont ic-list-like.*?</i>(.*?)</span>\
.*?<i class="iconfont ic-list-money.*?</i>(.*?)</span>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield{
            'title':item[0],
            'description':item[1],
            'author':item[2],
            'comment':item[3],
            'likes':item[4],
            'coin':item[5]
        }

def write_into_file(content):
    with open('result.txt','a+',encoding='utf-8') as file:
        file.write(json.dumps(content,ensure_ascii=False)+'\n')


if __name__=='__main__':
    html=get_html(url)
    for item in parse_html(html):
        write_into_file(item)
        time.sleep(1)