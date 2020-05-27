import requests
from bs4 import BeautifulSoup

def get_price(url):
    # res = requests.get('https://store.playstation.com/ja-jp/product/JP0506-CUSA13909_00-SEKIRO0000000000')
    res = requests.get(url)
    html_doc = res.text

    soup = BeautifulSoup(html_doc, 'html.parser')
    price_display_price = soup.find('h3', {"class": 'price-display__price'})

    p_encoded = price_display_price.get_text().encode('cp932', "ignore")
    p_decoded = p_encoded.decode('cp932')
    # print(p_decoded)

    return p_decoded
