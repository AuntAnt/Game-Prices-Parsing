from bs4 import BeautifulSoup
import requests as req
import string


# 1.[DONE] добавить трим ценника
# 2. добавить чтение url из файлов
# 3. добавить запись в файл название игры + цена
# 4. добавить запись в гугл-таблицу
# 5*. реализовать UI (???)
def extract_block(url):
    link = req.get(url).text
    soup = BeautifulSoup(link, 'lxml')
    block = soup.find('main', id="main")
    return block


def extract_price(block):
    price = block.find_all('span')[5].text
    return price


def extract_name(block):
    name = block.find_all('h1')[1].text
    return name


def normalize_price(price):
    final_price = ""
    for i in price:
        if i in string.digits:
            final_price = final_price + i
            final_price = final_price[:4]

    return final_price


valhalla = "https://store.playstation.com/ru-ru/product/EP0001-PPSA01532_00-GAME000000000000"
chronos = "https://store.playstation.com/ru-ru/product/EP4389-CUSA15161_00-CHRONOSEU0000000"


ext_price = extract_price(extract_block(chronos))
ext_name = extract_name(extract_block(chronos))
norm_price = normalize_price(ext_price)

print(ext_name, norm_price)
