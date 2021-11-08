import sqlite3


class WorkDB:

    # инициализиуруем инфу для создания таблицы в бд если она не существует
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                 user_id INTEGER UNIQUE NOT NULL,
                                                                 stage INTEGER,
                                                                 sub INTEGER,
                                                                 buy INTEGER,
                                                                 sell INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rates (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                 usd_buy INTEGER,
                                                                 usd_sell INTEGER,
                                                                 eur_buy INTEGER,
                                                                 eur_sell INTEGER,
                                                                 rub_buy INTEGER,
                                                                 rub_sell INTEGER
                                                                 sub_time INTEGER)''')
        self.cursor.execute('''SELECT usd_sell FROM rates WHERE id = 1''')
        if not self.cursor.fetchone():
            self.cursor.execute('''INSERT INTO rates (usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell, sub_time)
                                                      VALUES (1, 1, 1, 1, 1, 1, 0)''')
            self.conn.commit()

    def user_exists(self, user_id):
        result = self.cursor.execute('SELECT id FROM users WHERE user_id = ?', (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, stage=0, sub=0, buy=0, sell=0):
        print(f'Создан новый пользователь. user_id: {user_id}, stage: {stage}, sub: {sub}, buy: {buy}, sell: {sell}')
        self.cursor.execute('INSERT INTO users (user_id, stage, sub, buy, sell) VALUES (?, ?, ?, ?, ?)',
                            (user_id, stage, sub, buy, sell))
        return self.conn.commit()

    def get_users(self):
        result = self.cursor.execute('SELECT user_id FROM users')

    def update_stage(self, user_id, stage):
        self.cursor.execute('UPDATE users SET stage = ? WHERE user_id = ?', (stage, user_id))
        return self.conn.commit()

    def get_stage(self, user_id):
        result = self.cursor.execute('SELECT stage FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    def update_sub(self, user_id, sub):
        self.cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (sub, user_id))
        return self.conn.commit()

    def get_sub(self, user_id):
        result = self.cursor.execute('SELECT sub FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    def update_buy(self, user_id, buy):
        self.cursor.execute('UPDATE users SET buy = ? WHERE user_id = ?', (buy, user_id,))
        return self.conn.commit()

    def get_buy(self, user_id):
        result = self.cursor.execute('SELECT buy FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    def update_sell(self, user_id, sell):
        self.cursor.execute('UPDATE users SET sell = ? WHERE user_id = ?', (sell, user_id,))
        return self.conn.commit()

    def get_sell(self, user_id):
        result = self.cursor.execute('SELECT sell FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    def update_rates(self, usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell):
        self.cursor.execute('UPDATE rates SET usd_buy = ?, usd_sell = ?, eur_buy = ?, eur_sell = ?, rub_buy= ?,'
                            ' rub_sell = ? WHERE id = 1',
                            (usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell))
        return self.conn.commit()

    def get_rates(self):
        select = self.cursor.execute('SELECT * FROM rates WHERE id = 1')
        result = select.fetchone()
        rates = {'usd_buy': result[1], 'usd_sell': result[2],
                 'eur_buy': result[3], 'eur_sell': result[4],
                 'rub_buy': result[5], 'rub_sell': result[6]}
        return rates

    def update_sub_time(self, sub_time):
        self.cursor.execute('UPDATE rates SET sub_time = ? WHERE id = 1', (sub_time,))
        return self.conn.commit()

    def get_sub_time(self):
        result = self.cursor.execute('SELECT sub_time FROM rates WHERE id = 1')
        return result.fetchone()[0]

