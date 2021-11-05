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

usd_buy = float('{:.4f}'.format(usd_buy))
usd_buy = float('{:.4f}'.format(usd_buy))

eur_buy = float('{:.4f}'.format(eur_buy))
eur_sold = float('{:.4f}'.format(eur_sold))

rub_buy = float('{:.4f}'.format(rub_buy))
rub_sold = float('{:.4f}'.format(rub_sold))

print(usd_buy, usd_sold)
print(eur_buy, eur_sold)
print(rub_buy, rub_sold)


# print(f'usd: {usd}, eur: {eur}')