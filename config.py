from work_db import WorkDB
from currency import Currency
import re

# enter your bot TOKEN
TOKEN = ''
# enter chat id, you will receive there notifications about errors
check_chat = ()
# database for bot work with stages, user_id(chat_id) etc
db_file = 'database.db'
Bot_DB = WorkDB(db_file)
# object for work with currencies
Bot_currency = Currency()
# emoji pattern for delete emoji from message
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
    "\U000021A9"             # arrow to left
    "]+"
    )

'''
database:
    tab 'user' store user's status:
        user_id:
            unique chat id
        stage:
            0 - main menu
            10 - rates menu
            20 - convert menu
            21 - when user chose first currency
            22 - when user chose second currency and can enter a value to conversion
        sub:
            0 - user has not mailing subscription
            1 - user has mailing subscription in the morning
            2 - user has mailing subscription in the evening
        buy/sell:
            1 - usd
            2 - eur
            3 - rub
            4 - byn
    tab 'rates' store currencies rates that have updating per 40 seconds
'''
