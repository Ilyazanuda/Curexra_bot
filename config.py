from work_db import WorkDB
from currency import Currency
import re

# create TOKEN
TOKEN = '2029757069:AAEnh31xRTcVLNZ0PE_3BmvlbfaDqXzxFbs'
# chat that will receive notifications about errors
check_chat = (-607441191)
# create database for bot work with stages, user_id(chat_id) etc
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
    "]+"
    )


