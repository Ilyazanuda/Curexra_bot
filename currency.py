from db_test import WorkDB


class Currency:

    def __init__(self):
        self.Bot_DB = WorkDB('test.db')
        self.dir_rates = self.Bot_DB.get_rates()

    def convert(self, value, user_id):
        if self.Bot_DB.get_buy(user_id=user_id) == 1:
            if self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (self.dir_rates['usd_sell'] / self.dir_rates['eur_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (self.dir_rates['usd_sell'] / self.dir_rates['rub_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * self.dir_rates['usd_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 2:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (self.dir_rates['eur_sell'] / self.dir_rates['usd_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (self.dir_rates['eur_sell'] / self.dir_rates['rub_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * self.dir_rates['eur_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 3:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (self.dir_rates['rub_sell'] / self.dir_rates['usd_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (self.dir_rates['rub_sell'] / self.dir_rates['eur_sell'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 4:
                result = float('{:.2f}'.format(value * self.dir_rates['rub_sell']))
                return result

        elif self.Bot_DB.get_buy(user_id=user_id) == 4:
            if self.Bot_DB.get_sell(user_id=user_id) == 1:
                result = float('{:.2f}'.format(value * (1 / self.dir_rates['usd_buy'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 2:
                result = float('{:.2f}'.format(value * (1 / self.dir_rates['eur_buy'])))
                return result

            elif self.Bot_DB.get_sell(user_id=user_id) == 3:
                result = float('{:.2f}'.format(value * (1 / self.dir_rates['rub_buy'])))
                return result

    def rates(self, currency):
        values = []
        for _ in self.dir_rates:
            if currency in _:
                values.append(self.dir_rates[_])
        return values


test = Currency()
print(test.convert(100, 1))


