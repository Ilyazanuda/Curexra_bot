from db_test import WorkDB


class Currency:

    def __init__(self):
        self.Bot_DB = WorkDB('test.db')

    def get_rates(self):
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
        return {'usd_buy': usd_buy, 'usd_sell': usd_sell, 'eur_buy': eur_buy, 'eur_sell': eur_sell,
                'rub_buy': rub_buy, 'rub_sell': rub_sell}

    def convert(self, value, user_id):
        dir_rates = self.get_rates()

        if self.Bot_DB.get_buy(user_id=user_id) == 1:
            if self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (dir_rates['usd_sell'] / dir_rates['eur_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (dir_rates['usd_sell'] / dir_rates['rub_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * dir_rates['usd_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 2:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (dir_rates['eur_sell'] / dir_rates['usd_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (dir_rates['eur_sell'] / dir_rates['rub_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * dir_rates['eur_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 3:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (dir_rates['rub_sell'] / dir_rates['usd_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (dir_rates['rub_sell'] / dir_rates['eur_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * dir_rates['rub_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 4:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (1 / dir_rates['usd_buy'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (1 / dir_rates['eur_buy'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (1 / dir_rates['rub_buy'])))
                return result

    def rates(self, currency):
        values = []
        dir_rates = self.get_rates()
        for _ in dir_rates:
            if currency in _:
                values.append(dir_rates[_])
        return values


