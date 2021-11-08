from bs4 import BeautifulSoup
from lxml import etree
import requests
import time
from db_test import WorkDB
import telebot
from telebot import types
from config import TOKEN

bot_auto = telebot.AsyncTeleBot(TOKEN)


class Parse:

    def __init__(self):
        self.url = 'https://myfin.by/currency/minsk'
        self.headers = ({'User-Agent':
                         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                         (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                         'Accept-Language': 'en-US, en;q=0.5'})
        self.Bot_DB = WorkDB('test.db')

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
        self.Bot_DB.update_rates(usd_buy=usd_buy, usd_sell=usd_sell, eur_buy=eur_buy, eur_sell=eur_sell,
                                 rub_buy=rub_buy, rub_sell=rub_sell)
        if "11:17:30" >= time.strftime('%X') >= "11:16:30":
            if self.Bot_DB.get_sub_time() == 0:
                print('Делаем рассылку курсов')
                self.auto_sending()
                self.Bot_DB.update_sub_time(sub_time=1)
        else:
            self.Bot_DB.update_sub_time(sub_time=0)
        print(f'{"-" * 8}\nrates updated\n')
        time.sleep(15)
        self.parse_rates()

    def auto_sending(self):
        rates = self.Bot_DB.get_rates()

        # bot_auto.send_message()
        pass


run_script = Parse()
run_script.parse_rates()

