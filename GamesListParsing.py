from bs4 import BeautifulSoup
import requests as req


# 1. добавить трим ценника
# 2. добавить чтение url из файлов
# 3. добавить запись в файл название игры + цена
# 4. добавить запись в гугл-таблицу
def add_game(url):
    link = req.get(url).text
    soup = BeautifulSoup(link, 'lxml')

    block = soup.find('main', id="main")
    name = block.find_all('h1')[1].text
    price = block.find_all('span')[5].text

    return name, price


print(add_game("https://store.playstation.com/ru-ru/product/EP0001-PPSA01532_00-GAME000000000000"))
