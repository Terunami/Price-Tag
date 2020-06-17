import requests
import time
from bs4 import BeautifulSoup


# playstation Storeの商品ページをスクレイピング

class playstation():


    # 定価取得
    def get_list_price(str_url):

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
        
        time.sleep(1)

        if is_int(p_decoded.replace(',', '')):
            return int(p_decoded.replace(',', ''))
        else:
            if p_decoded == '無料':
                return 0
            else:
                return p_decoded

    # 現価取得
    def get_current_price(str_url):

        res = requests.get(str_url)
        html_doc = res.text

        soup = BeautifulSoup(html_doc, 'html.parser')
        price_display_price = soup.find('h3', {"class": 'price-display__price'})

        p_encoded = price_display_price.get_text().encode('cp932', "ignore")
        p_decoded = p_encoded.decode('cp932')

        time.sleep(1)
        
        if is_int(p_decoded.replace(',', '')):
            return int(p_decoded.replace(',', ''))
        else:
            if p_decoded == '無料':
                return 0
            else:
                return p_decoded

# 任天堂ストアはscraping ができない？
# 取得できるhtmlの形式が違うためか？
class nintendo():

    # 定価取得
    def get_list_price(str_url):

        res = requests.get(str_url)
        html_doc = res.text

        print(html_doc)

        soup = BeautifulSoup(html_doc, 'html.parser')
        # class'price' が存在しない場合はclass'price-display__price'が定価
        item_price = soup.find({"class": 'item-price'})
        fixed = soup.find({"class": 'o_p-product-detail__fixed-price'})
        price_price = soup.find(class_='o_p-product-detail__price--price')
        if item_price:
            p_encoded = item_price.get_text().encode('cp932', "ignore")
        elif fixed :
            p_encoded = fixed.get_text().encode('cp932', "ignore")
        elif price_price:
            p_encoded = price_price.get_text().encode('cp932', "ignore")
        else:
            print("test")

        print(soup.find(class_="o_p-product-detail__discount-detail-wrap"))
        
        print(fixed)
        print(item_price)
        print(price_price)
        p_decoded = p_encoded.decode('cp932')
        
        time.sleep(1)

        if is_int(p_decoded.replace(',', '').replace('円', '')):
            return int(p_decoded.replace(',', ''))
        else:
            if p_decoded == '無料':
                return 0
            else:
                return p_decoded

    # 現価取得
    def get_current_price(str_url):

        res = requests.get(str_url)
        html_doc = res.text

        soup = BeautifulSoup(html_doc, 'html.parser')
        price_price = soup.find('div', {"class": 'po_p-product-detail__price--price'})

        p_encoded = price_price.get_text().encode('cp932', "ignore")
        p_decoded = p_encoded.decode('cp932')

        time.sleep(1)
        
        if is_int(p_decoded.replace(',', '')):
            return int(p_decoded.replace(',', ''))
        else:
            if p_decoded == '無料':
                return 0
            else:
                return p_decoded


# int型に変換可能かどうかを返す
def is_int(s):
    try:
        int(s)
    except:
        return False
    return True












