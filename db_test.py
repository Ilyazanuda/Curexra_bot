import sqlite3


class WorkDB:

    # инициализиуруем инфу для создания таблицы в бд если она не существует
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                 user_id INTEGER UNIQUE NOT NULL,
                                                                 stage INTEGER,
                                                                 sub INTEGER)
                            ''')

    def user_exists(self, user_id):
        result = self.cursor.execute('SELECT id FROM users WHERE user_id = ?', (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id, stage=0, sub=0):
        print(f'Создан новый пользователь. user_id: {user_id}, stage: {stage}, sub: {sub}')
        self.cursor.execute('INSERT INTO users (user_id, stage, sub) VALUES (?, ?, ?)', (user_id, stage, sub))
        return self.conn.commit()

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
