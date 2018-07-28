#!/usr/bin/env python
#coding:utf-8

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote
import  pymongo

KEYWORD='iPad'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait=WebDriverWait(browser,10)

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_page(page):
    url='https://list.tmall.com/search_product.htm?q='+quote(KEYWORD)
    try:
        browser.get(url)
        if page>1:
            input=wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'#content > div.main > div.ui-page > div > b.ui-page-skip > form > input.ui-page-skipTo'))
            )
            submit=wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'#content > div.main > div.ui-page > div > b.ui-page-skip > form > button'))
            )
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#content > div.main > div.ui-page > div > b.ui-page-num > b.ui-page-cur'),str(page))
        )
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#J_ItemList'))
        )
        parse_page()
    except TimeoutException:
        print("Time out")

def parse_page():
    html=browser.page_source
    doc=pq(html)
    items=doc.find('#J_ItemList > .product').items()
    for item in items:
        product={
            'price':item.find('.productPrice').text().replace('\n',''),
            'title':item.find('.productTitle').text().replace('\n',''),
            'shop':item.find('.productShop').text().replace('\n',''),
            'status':item.find('.productStatus').text().replace('\n','')
        }
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')

if __name__=='__main__':
    for i in range(1,3):
        get_page(i)
