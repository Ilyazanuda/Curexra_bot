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

dict_currency = {1:'\U0001F1FA\U0001F1F8USD', 2:'\U0001F1EA\U0001F1FAEUR', 3:'\U0001F1F7\U0001F1FARUB',
                             4:'\U0001F1E7\U0001F1FEBYN'}
for _ in dict_currency:
    print(_)
    print(dict_currency[_])