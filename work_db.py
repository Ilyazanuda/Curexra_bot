import sqlite3
import threading


class WorkDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # column information in config
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
        # to be able to update information in the same cells at id 1
        if not self.cursor.fetchone():
            self.cursor.execute('''INSERT INTO rates (usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell, sub_time)
                                                      VALUES (1, 1, 1, 1, 1, 1, 0)''')
            self.conn.commit()
        # for fix threading error in sqlite3
        self.lock = threading.RLock()

    # check user in the database
    def user_exists(self, user_id):
        with self.lock:
            result = self.cursor.execute('SELECT id FROM users WHERE user_id = ?', (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, stage=0, sub=0, buy=0, sell=0):
        with self.lock:
            print(f'Created new user. user_id: {user_id}, stage: {stage}, sub: {sub}, buy: {buy}, sell: {sell}')
            self.cursor.execute('INSERT INTO users (user_id, stage, sub, buy, sell) VALUES (?, ?, ?, ?, ?)',
                                (user_id, stage, sub, buy, sell))
        return self.conn.commit()

    # stage for check where user in dialog
    def update_stage(self, user_id, stage):
        with self.lock:
            self.cursor.execute('UPDATE users SET stage = ? WHERE user_id = ?', (stage, user_id))
        return self.conn.commit()

    def get_stage(self, user_id):
        with self.lock:
            result = self.cursor.execute('SELECT stage FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    # sub is about user has mailing or no, and when user will has mailing
    def update_sub(self, user_id, sub):
        with self.lock:
            self.cursor.execute('UPDATE users SET sub = ? WHERE user_id = ?', (sub, user_id))
        return self.conn.commit()

    def get_sub(self, user_id):
        with self.lock:
            result = self.cursor.execute('SELECT sub FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    # get users list these have subscription
    def get_sub_users(self, sub):
        with self.lock:
            result = self.cursor.execute('SELECT user_id FROM users WHERE sub = ?', (sub,))
        return result.fetchall()

    # buy/sell to store user's choice of currency for exchange
    def update_buy(self, user_id, buy):
        with self.lock:
            self.cursor.execute('UPDATE users SET buy = ? WHERE user_id = ?', (buy, user_id,))
        return self.conn.commit()

    def get_buy(self, user_id):
        with self.lock:
            result = self.cursor.execute('SELECT buy FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    def update_sell(self, user_id, sell):
        with self.lock:
            self.cursor.execute('UPDATE users SET sell = ? WHERE user_id = ?', (sell, user_id,))
        return self.conn.commit()

    def get_sell(self, user_id):
        with self.lock:
            result = self.cursor.execute('SELECT sell FROM users WHERE user_id = ?', (user_id,))
        return result.fetchone()[0]

    def update_rates(self, usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell):
        with self.lock:
            self.cursor.execute('UPDATE rates SET usd_buy = ?, usd_sell = ?, eur_buy = ?, eur_sell = ?, rub_buy= ?,'
                                ' rub_sell = ? WHERE id = 1',
                                (usd_buy, usd_sell, eur_buy, eur_sell, rub_buy, rub_sell))
        return self.conn.commit()

    def get_rates(self):
        with self.lock:
            select = self.cursor.execute('SELECT * FROM rates WHERE id = 1')
            result = select.fetchone()
            rates = {'usd_buy': result[1], 'usd_sell': result[2],
                     'eur_buy': result[3], 'eur_sell': result[4],
                     'rub_buy': result[5], 'rub_sell': result[6]}
        return rates

    # sub_time is about when user will has mailing
    def update_sub_time(self, sub_time):
        with self.lock:
            self.cursor.execute('UPDATE rates SET sub_time = ? WHERE id = 1', (sub_time,))
        return self.conn.commit()

    def get_sub_time(self):
        with self.lock:
            result = self.cursor.execute('SELECT sub_time FROM rates WHERE id = 1')
        return result.fetchone()[0]
