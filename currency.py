from work_db import WorkDB


class Currency:

    def __init__(self):
        self.Bot_DB = WorkDB('database.db')

    def exchange(self, value, user_id):
        dir_rates = self.Bot_DB.get_rates()
        if self.Bot_DB.get_buy(user_id=user_id) == 1:
            if self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (dir_rates['usd_sell'] / dir_rates['eur_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (dir_rates['usd_sell'] / dir_rates['rub_sell'] / 100)))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * dir_rates['usd_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 2:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (dir_rates['eur_sell'] / dir_rates['usd_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (dir_rates['eur_sell'] / dir_rates['rub_sell'] / 100)))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * dir_rates['eur_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 3:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (dir_rates['rub_sell'] / 100 / dir_rates['usd_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (dir_rates['rub_sell'] / 100 / dir_rates['eur_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * dir_rates['rub_sell'] / 100))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 4:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (1 / dir_rates['usd_buy'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (1 / dir_rates['eur_buy'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (1 / dir_rates['rub_buy'] / 100)))
                return result

    def rates(self, currency):
        dir_rates = self.Bot_DB.get_rates()
        values = []
        for _ in dir_rates:
            if currency in _:
                values.append(dir_rates[_])
        return values
