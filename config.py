from db_test import WorkDB
from currency import Currency
import re

# токен бота
TOKEN = '2029757069:AAFODdbd4OH3KsAsSyyaq_JhCly4NIv_MEU'

# хидер сервера на котором стоит бот
my_header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,' \
            ' like Gecko) Chrome/95.0.4638.54 Safari/537.36'
# создаём базу данных где будем отслеживать стадию разговора, id юзера и его подписки
db_file = 'test.db'
Bot_DB = WorkDB(db_file)
# создаём объект работы с валютой
Bot_currency = Currency()
# Эмоджи шаблоны

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "\U000024C2-\U0001F251" 
    "]+"
    )

# конфиг конвертера валют
# stage=21 USD <- RUB stage=31
# stage=21 USD <- EUR stage=32
# stage=21 USD <- BYN stage=33
# stage=22 EUR <- USD stage=34
# stage=22 EUR <- RUB stage=35
# stage=22 EUR <- BYN stage=36
# stage=23 RUB <- USD stage=37
# stage=23 RUB <- EUR stage=38
# stage=23 RUB <- BYN stage=39
# stage=24 BYN <- USD stage=40
# stage=24 BYN <- EUR stage=41
# stage=24 BYN <- BYN stage=42
