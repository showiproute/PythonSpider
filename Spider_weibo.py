#!/usr/bin/env python
#coding:utf-8


import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient
from urllib.parse import  urlencode

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/1670421223',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

client = MongoClient()
db = client['weibo']
collection = db['weibo']

def get_json(page):
    params={
        'type':'uid',
        'value':'1670421223',
        'containerid':'1076031670421223',
        'page':page
    }
    url=base_url+urlencode(params)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json(),page
    except requests.ConnectionError as e:
        print(e.args)

def parse_json(json,page):
    if json:
        items=json.get('data').get('cards')
        for index,item in enumerate(items):
            if index==1 and page==1:
                continue
            else:
                item=item.get('mblog')
                data={}
                data['attitudes_count']=item.get('attitudes_count')
                data['comments_count']=item.get('comments_count')
                data['text']=pq(item.get('text')).text()
                yield data

def get_total(json_data):
    if json_data:
        count = int(json_data.get('data').get('cardlistInfo').get('total'))
        if count%10==0:
            total=int(count/10)
        else:
            total=int(count/10)+1
        return total
    else:
        return None

def save_to_mongo(result):
    if collection.insert(result):
        print('Saved to Mongo')



if __name__=='__main__':
    json_data,page=get_json(2)
    total=get_total(json_data)
    for i in list(range(1,total)):
        json_data=get_json(i)
        results=parse_json(*json_data)
        for result in results:
            print(result)
            save_to_mongo(result)

