# import requests
# from bs4 import BeautifulSoup
# from config import my_header
# USD = 'https://www.nbrb.by/statistics/rates/ratesdaily/?p=true&'
# full_page = requests.get(USD, my_header)
#
# print(full_page.content)
#
# soup = BeautifulSoup(full_page.content, 'html.parser')
#
# convert = soup.findAll(s)

import requests
from bs4 import BeautifulSoup
from lxml import etree
import requests

url = 'https://myfin.by/currency/minsk'        # адрес мобильной версии
headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

web_page = requests.get(url, headers=headers)
soup = BeautifulSoup(web_page.content, 'html.parser')
dom = etree.HTML(str(soup))

usd_buy = float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]')[0].text)
usd_sold = float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/tbody/tr[1]/td[3]')[0].text)

eur_buy = float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/tbody/tr[2]/td[2]')[0].text)
eur_sold = float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/tbody/tr[2]/td[3]')[0].text)

rub_buy = float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/tbody/tr[3]/td[2]')[0].text) / 100
rub_sold = float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/tbody/tr[3]/td[3]')[0].text) / 100

usd_buy = format(str(usd_buy), '.4f')
usd_sold = format(str(usd_sold), '.4f')
print(usd_buy, usd_sold)
print(eur_buy, eur_sold)
print(rub_buy, rub_sold)
#
# print(f'usd: {usd}, eur: {eur}')