from bs4 import BeautifulSoup
from lxml import etree
import sqlite3
import requests
import time


class Parse:

    def __init__(self):
        self.url = 'https://myfin.by/currency/minsk'
        self.headers = ({'User-Agent':
                         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                         (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                         'Accept-Language': 'en-US, en;q=0.5'})
        self.conn = sqlite3.connect('test.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rates (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                 usd_buy INTEGER,
                                                                 usd_sell INTEGER,
                                                                 eur_buy INTEGER,
                                                                 eur_sell INTEGER,
                                                                 rub_buy INTEGER,
                                                                 rub_sell INTEGER)''')
        self.cursor.execute('''SELECT usd_sell FROM rates WHERE id = 1''')
        if not self.cursor.fetchone():
            self.cursor.execute('''INSERT INTO rates (usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell)
                                              VALUES (1, 1, 1, 1, 1, 1)''')
            self.conn.commit()

    def parse_rates(self):
        web_page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(web_page.content, 'html.parser')
        dom = etree.HTML(str(soup))
        usd_buy = float('{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[1]/td[2]')[0].text)))
        usd_sell = float('{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                         'tbody/tr[1]/td[3]')[0].text)))
        eur_buy = float('{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[2]/td[2]')[0].text)))
        eur_sell = float('{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                         'tbody/tr[2]/td[3]')[0].text)))
        rub_buy = float('{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[3]/td[2]')[0].text) / 100))
        rub_sell = float('{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                         'tbody/tr[3]/td[3]')[0].text) / 100))
        self.cursor.execute('''UPDATE rates SET usd_buy = ?, usd_sell = ?, eur_buy = ?,
                                                eur_sell = ?, rub_buy= ?, rub_sell = ? WHERE id = 1''',
                            (usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell))
        self.conn.commit()
        print(f'{"-" * 8}\nrates updated\n{"-" * 8}')
        time.sleep(120)
        self.parse_rates()


work = Parse()
work.parse_rates()
