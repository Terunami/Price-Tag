import requests
from bs4 import BeautifulSoup
import logging

# playstation Storeの商品ページをスクレイピング

# 定価取得
def get_list_price(str_url):
    # res = requests.get('https://store.playstation.com/ja-jp/product/JP0506-CUSA13909_00-SEKIRO0000000000')
    res = requests.get(str_url)
    html_doc = res.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    # class'price' が存在しない場合はclass'price-display__price'が定価
    price = soup.find('div', {"class": 'price'})
    if price :
        p_encoded = price.get_text().encode('cp932', "ignore")
    else:
        price_display_price = soup.find('h3', {"class": 'price-display__price'})
        p_encoded = price_display_price.get_text().encode('cp932', "ignore")
        
    p_decoded = p_encoded.decode('cp932')
    
    return int(p_decoded.replace(',', ''))

# 現価取得
def get_current_price(str_url):
    # res = requests.get('https://store.playstation.com/ja-jp/product/JP0506-CUSA13909_00-SEKIRO0000000000')
    res = requests.get(str_url)
    html_doc = res.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    price_display_price = soup.find('h3', {"class": 'price-display__price'})

    p_encoded = price_display_price.get_text().encode('cp932', "ignore")
    p_decoded = p_encoded.decode('cp932')

    return int(p_decoded.replace(',', ''))
