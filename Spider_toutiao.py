#!/usr/bin/env python
#coding:utf-8

import requests
from urllib.parse import urlencode
import os
from hashlib import md5

headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'x-requested-with':'XMLHttpRequest',
    'referer':'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D',
}

base_url = 'http://www.toutiao.com/search_content/?'

START_OFFSET=0
END_OFFSET=5


def get_page(offset):
    params={
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'search_tab'
    }
    url=base_url+urlencode(params)
    try:
        response=requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.json(),offset
    except requests.ConnectionError as e:
        print(e.args)

def get_images(json,offset):
    if json:
        items=json.get('data')
        for index,item in enumerate(items):
            if index==0 and offset==0:
                continue
            elif index==1 and offset==0:
                continue
            else:
                title=item.get('title')
                image_urls=item.get('image_list')
                if image_urls:
                    for image_url in image_urls:
                        yield {
                            'title':title,
                            'image':image_url.get('url')
                        }

def save_images(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        local_list_image=item.get('image')
        local_large_image=local_list_image.replace('list','large')
        pic_url='http:'+local_large_image
        try:
            response=requests.get(pic_url)
            if response.status_code == 200:
                file_path='{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
                if not os.path.exists(file_path):
                    with open(file_path,'wb')  as f:
                        f.write(response.content)
                else:
                    print("The pic has already saved",file_path)
        except requests.ConnectionError as e:
            print(e.args)
    except BaseException:
        raise

if __name__=='__main__':
    for offset in [x*20 for x in range(START_OFFSET,END_OFFSET)]:
        json,offset=get_page(0)
        results=get_images(json,offset)
        for result in results:
            save_images(result)

