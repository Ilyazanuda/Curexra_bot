from bs4 import BeautifulSoup
from lxml import etree
from work_db import WorkDB
from config import TOKEN
import requests
import time
import telebot

bot_auto = telebot.AsyncTeleBot(TOKEN)


class Parse:

    def __init__(self):
        self.url = 'https://myfin.by/currency/minsk'
        self.headers = ({'User-Agent':
                         'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                         (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                         'Accept-Language': 'en-US, en;q=0.5'})
        self.Bot_DB = WorkDB('database.db')

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
        if "08:02:00" >= time.strftime('%X') >= "08:00:00":
            if self.Bot_DB.get_sub_time() == 0:
                print(f'Do mailing {time.strftime("%X")}')
                self.mailing(1)
                self.Bot_DB.update_sub_time(sub_time=1)
        elif "20:02:00" >= time.strftime('%X') >= "20:00:00":
            if self.Bot_DB.get_sub_time() == 0:
                print(f'Do mailing {time.strftime("%X")}')
                self.mailing(2)
                self.Bot_DB.update_sub_time(sub_time=1)
        else:
            self.Bot_DB.update_sub_time(sub_time=0)
        print(f'{"-" * 8}\nrates updated')
        time.sleep(40)
        self.parse_rates()

    def mailing(self, sub):
        rates = self.Bot_DB.get_rates()
        users_id = self.Bot_DB.get_sub_users(sub=sub)
        mailing_rates = (f'Ежедневная <b><i>Рассылка "Курсы валют"</i></b>\U0001F4C8 '
                         f'в соответствии c сервисом <i><b>myfin</b></i> на <b>{time.strftime("%x")}</b>.\n'
                         f'Курс <b>покупки \U0001F1FA\U0001F1F8USD</b>: {rates["usd_buy"]} '
                         f'<b>\U0001F1E7\U0001F1FEBYN</b>\n'
                         f'Курс <b>продажи \U0001F1FA\U0001F1F8USD</b>: {rates["usd_sell"]} '
                         f'<b>\U0001F1E7\U0001F1FEBYN</b>\n'
                         f'Курс <b>покупки \U0001F1EA\U0001F1FAEUR</b>: {rates["eur_buy"]} '
                         f'<b>\U0001F1E7\U0001F1FEBYN</b>\n'
                         f'Курс <b>продажи \U0001F1EA\U0001F1FAEUR</b>: {rates["eur_sell"]} '
                         f'<b>\U0001F1E7\U0001F1FEBYN</b>\n'
                         f'Курс <b>покупки \U0001F1F7\U0001F1FARUB</b>: {rates["rub_buy"]} '
                         f'<b>\U0001F1E7\U0001F1FEBYN</b>\n'
                         f'Курс <b>продажи \U0001F1F7\U0001F1FARUB</b>: {rates["rub_sell"]} '
                         f'<b>\U0001F1E7\U0001F1FEBYN</b>')
        for chat_id in users_id:
            bot_auto.send_message(chat_id[0], mailing_rates, parse_mode='html')


if __name__ == '__main__':
    run_script = Parse()
    run_script.parse_rates()


