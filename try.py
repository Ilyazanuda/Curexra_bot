# import re
#
# EMOJI_PATTERN = re.compile(
#     "["
#     "\U0001F1E0-\U0001F1FF"  # flags (iOS)
#     "\U0001F300-\U0001F5FF"  # symbols & pictographs
#     "\U0001F600-\U0001F64F"  # emoticons
#     "\U0001F680-\U0001F6FF"  # transport & map symbols
#     "\U0001F700-\U0001F77F"  # alchemical symbols
#     "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
#     "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
#     "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
#     "\U0001FA00-\U0001FA6F"  # Chess Symbols
#     "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
#     "\U00002702-\U000027B0"  # Dingbats
#     "\U000024C2-\U0001F251"
#     "]+"
#     )
#
# text = "23,521,231"
#
# print(re.findall(r"\d+(?:.\d+)?", text))
#
# button_usd = types.KeyboardButton('\U0001F1FA\U0001F1F8USD')
# button_eur = types.KeyboardButton('\U0001F1EA\U0001F1FAEUR')
# button_rub = types.KeyboardButton('\U0001F1F7\U0001F1FARUB')
# button_byn = types.KeyboardButton('\U0001F1E7\U0001F1FEBYN')
# import re
# message_no_emoji = '2123.213.321'
# print(True if float((re.findall(r"\d+(?:[^a-zA-Z-а-яА-ЯёЁ].\d+|)?",
#                                 message_no_emoji)[0].replace(',', '.'))) else False)
# print(float((re.findall(r"\d+(?:[^a-zA-Z-а-яА-ЯёЁ].\d+|)?",
#                         message_no_emoji)[0].replace(',', '.'))))

import sqlite3

conn = sqlite3.connect('db_db_db.db')
cur = conn.cursor()

n = "12.5"
cur.execute('''CREATE TABLE IF NOT EXISTS tab (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                               col1 INTEGER,
                                               col2 BLOB,
                                               col3 REAL,
                                               col4 NUMERIC,
                                               col5 TEXT)''')
cur.execute('''INSERT INTO  tab (col1, col2, col3, col4, col5) VALUES (?, ?, ?, ?, ?)''', (n, n, n, n, n))

cur.execute('''SELECT col1, col2, col3, col4, col5 FROM tab WHERE id = 1''')
result = cur.fetchone()
print(f'INTEGER: {result[0]} type: {type(result[0])}\n'
      f'BLOB {result[1]} type: {type(result[1])}\n'
      f'REAL {result[2]} type: {type(result[2])}\n'
      f'NUMERIC {result[3]} type: {type(result[3])}\n'
      f'TEXT {result[4]} type: {type(result[4])}')


