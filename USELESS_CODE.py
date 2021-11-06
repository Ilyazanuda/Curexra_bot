

# При получении текста проходится по условия и выполняет их
@bot.message_handler(content_types=['text'])
def bot_answer(message):
    check_message(message=message)
    check_user_db_status(message=message)
    # try:
    #     emoji_in_message = re.findall(EMOJI_PATTERN, message.text)[0]
    #     print('Module TRY_EMOJI. Emoji in message:', emoji_in_message)
    # except IndexError:
    #     print("Module TRY_EMOJI. Emoji is not found")
    #
    # message.text = re.sub(EMOJI_PATTERN, r'', message.text)

    # message.text = re.sub(EMOJI_PATTERN, r'', message.text)

    # try:
    #     numb_to_conv = re.sub(EMOJI_PATTERN, r'', message.text)
    #     numb_to_conv = float((re.findall(r"\d+(?:[^a-zA-Z-а-яА-ЯёЁ].\d+|)?", numb_to_conv)[0].replace(',', '.')))
    # except IndexError:
    #     numb_to_conv = None
    #     print('Module TRY_NUMB Error, numb_to_conv is not exist.')
    #
    # if Bot_DB.get_stage(message.chat.id) in (21, 22, 23) and type(numb_to_conv) is float:
    #     print(message.text)
    #     check_message(message=message)
    #     converter_rate(message=message, numb=numb_to_conv)

    # переход в меню курсов валют
    if message.text.lower() in ('\U0001F4C8курсы валют', 'курсы валют', 'курсы'):
        rates(message)
    # переход в меню конвертера
    elif message.text.lower() in ('\U0001F4B0конвертер валют', 'конвертер валют', 'конвертер'):
        converter(message)
    # переход в главное меню
    elif message.text.lower() in ('\U0001F4D1к главному меню', 'к главному меню'):
        menu(message)
    # переход в меню подписки
    elif message.text.lower() in ('\U00002705подписка', 'подписка'):
        subscription(message)
    # кнопка возврата на начальное меню конвертера
    elif message.text.lower() in ('\U000021A9назад', 'назад'):
        if Bot_DB.get_stage(user_id=message.chat.id) in range(21, 43):
            converter(message)

    elif Bot_DB.get_stage(user_id=message.chat.id) in (20, 21, 22, 23, 24) or range(31, 42):
        if message.text.lower() in ('\U0001F1FA\U0001F1F8usd', 'usd'):
            if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                Bot_DB.update_stage(user_id=message.chat.id, stage=21)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row(button_eur, button_rub, button_byn)
                markup.row(button_into_back)
                markup.row(button_into_menu)
                bot.send_message(message.chat.id, 'Вы выбрали для покупки \U0001F1FA\U0001F1F8<b>USD</b>\n'
                                                  'Выберите валюту для продажи из меню.',
                                 parse_mode='html',
                                 reply_markup=markup)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 22:
                Bot_DB.update_stage(user_id=message.chat.id, stage=34)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 23:
                Bot_DB.update_stage(user_id=message.chat.id, stage=37)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 24:
                Bot_DB.update_stage(user_id=message.chat.id, stage=40)

        elif message.text.lower() in ('\U0001F1EA\U0001F1FAeur', 'eur'):
            if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                Bot_DB.update_stage(user_id=message.chat.id, stage=22)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row(button_usd, button_rub, button_byn)
                markup.row(button_into_back)
                markup.row(button_into_menu)
                bot.send_message(message.chat.id, 'Вы выбрали для покупки \U0001F1EA\U0001F1FA<b>EUR</b>\n'
                                                  'Выберите валюту для продажи из меню.',
                                 parse_mode='html',
                                 reply_markup=markup)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 21:
                Bot_DB.update_stage(user_id=message.chat.id, stage=32)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 23:
                Bot_DB.update_stage(user_id=message.chat.id, stage=38)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 24:
                Bot_DB.update_stage(user_id=message.chat.id, stage=41)

        elif message.text.lower() in ('\U0001F1F7\U0001F1FArub', 'rub'):
            if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                Bot_DB.update_stage(user_id=message.chat.id, stage=23)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row(button_usd, button_eur, button_byn)
                markup.row(button_into_back)
                markup.row(button_into_menu)
                bot.send_message(message.chat.id, 'Вы выбрали для покупки \U0001F1F7\U0001F1FA<b>RUB</b>\n'
                                                  'Выберите валюту для продажи из меню.',
                                 parse_mode='html',
                                 reply_markup=markup)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 21:
                Bot_DB.update_stage(user_id=message.chat.id, stage=31)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 22:
                Bot_DB.update_stage(user_id=message.chat.id, stage=35)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 24:
                Bot_DB.update_stage(user_id=message.chat.id, stage=42)

        elif message.text.lower() in ('\U0001F1E7\U0001F1FEbyn', 'byn'):
            if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                Bot_DB.update_stage(user_id=message.chat.id, stage=24)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.row(button_usd, button_eur, button_rub)
                markup.row(button_into_back)
                markup.row(button_into_menu)
                bot.send_message(message.chat.id, 'Вы выбрали для покупки \U0001F1E7\U0001F1FE<b>BYN</b>\n'
                                                  'Выберите валюту для продажи из меню.',
                                 parse_mode='html',
                                 reply_markup=markup)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 21:
                Bot_DB.update_stage(user_id=message.chat.id, stage=33)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 22:
                Bot_DB.update_stage(user_id=message.chat.id, stage=36)
            elif Bot_DB.get_stage(user_id=message.chat.id) == 23:
                Bot_DB.update_stage(user_id=message.chat.id, stage=39)


    else:
        bot.send_message(message.chat.id, 'Извините, я не понимаю, чего вы хотите.\n'
                                          'Напишите сообщение в рамках того меню в котором находитесь.')



-------------------------------------------
        from bs4 import BeautifulSoup
        from lxml import etree
        from config import Bot_DB
        import requests
        import time

        class RateConvert:

            def __init__(self):
                self.url = 'https://myfin.by/currency/minsk'
                self.headers = ({'User-Agent':
                                     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                                     (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
                                 'Accept-Language': 'en-US, en;q=0.5'})

            def parse_rates(self, currency):
                web_page = requests.get(self.url, headers=self.headers)
                soup = BeautifulSoup(web_page.content, 'html.parser')
                dom = etree.HTML(str(soup))

                def usd_buy():
                    return float(
                        '{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[1]/td[2]')[0].text)))

                def usd_sell():
                    return float(
                        '{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[1]/td[3]')[0].text)))

                def eur_buy():
                    return float(
                        '{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[2]/td[2]')[0].text)))

                def eur_sell():
                    return float(
                        '{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[2]/td[3]')[0].text)))

                def rub_buy():
                    return float(
                        '{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[3]/td[2]')[0].text) / 100))

                def rub_sell():
                    return float(
                        '{:.4f}'.format(float(dom.xpath('//*[@id="workarea"]/div[1]/div[2]/div/div/div/div/table/'
                                                        'tbody/tr[3]/td[3]')[0].text) / 100))

                if currency == 'usd_buy':
                    return usd_buy()
                elif currency == 'usd_sell':
                    return usd_sell()
                elif currency == 'eur_buy':
                    return eur_buy()
                elif currency == 'eur_sell':
                    return eur_sell()
                elif currency == 'rub_buy':
                    return rub_buy()
                elif currency == 'rub_sell':
                    return rub_sell()

            def convert_parse(self, message):

                if Bot_DB.get_buy(message.chat.id) == 1:
                    if Bot_DB.get_sell(message.chat.id) == 2:
                        result = message.text * (self.parse_rates('usd_sell') / self.parse_rates('eur_sell'))
                        print(result)
                    elif Bot_DB.get_sell(message.chat.id) == 3:
                        result = message.text * (self.parse_rates('usd_sell') / self.parse_rates('rub_sell'))
                        print(result)
                    elif Bot_DB.get_sell(message.chat.id) == 4:
                        result = message.text * self.parse_rates('usd_sell')
                        print(result)
                elif Bot_DB.get_buy(message.chat.id) == 2:
                    if Bot_DB.get_sell(message.chat.id) == 1:
                        result = message.text * (self.parse_rates('eur_sell') / self.parse_rates('usd_sell'))
                        print(result)
                    elif Bot_DB.get_sell(message.chat.id) == 3:
                        result = message.text * (self.parse_rates('eur_sell') / self.parse_rates('rub_sell'))
                        print(result)
                    elif Bot_DB.get_sell(message.chat.id) == 4:
                        result = message.text * self.parse_rates('eur_sell')
                        print(result)

                elif Bot_DB.get_buy(message.chat.id) == 3:
                    if Bot_DB.get_sell(message.chat.id) == 1:
                        result = message.text * (self.parse_rates('rub_sell') / self.parse_rates('usd_sell'))
                        print(result)

                    elif Bot_DB.get_sell(message.chat.id) == 2:
                        result = message.text * (self.parse_rates('rub_sell') / self.parse_rates('eur_sell'))
                        print(result)

                    elif Bot_DB.get_sell(message.chat.id) == 4:
                        result = message.text * self.parse_rates('rub_sell')
                        print(result)

                elif Bot_DB.get_buy(message.chat.id) == 4:
                    if Bot_DB.get_sell(message.chat.id) == 1:
                        result = message.text * (1 / self.parse_rates('usd_buy'))
                        print(result)
                    elif Bot_DB.get_sell(message.chat.id) == 2:
                        result = message.text * (1 / self.parse_rates('eur_buy'))
                        print(result)
                    elif Bot_DB.get_sell(message.chat.id) == 3:
                        result = message.text * (1 / self.parse_rates('rub_buy'))
                        print(result)

        start_time = time.time()
        rate = RateConvert()
        rate.convert_parse(5)
        print('%s seconds' % (time.time() - start_time))