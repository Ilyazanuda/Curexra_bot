
# должен быть в  bot.py bot_answer() как сортировка от эмодзи
try:
    emoji_in_message = re.findall(EMOJI_PATTERN, message.text)[0]
    print('Module TRY_EMOJI. Emoji in message:', emoji_in_message)
except IndexError:
    print("Module TRY_EMOJI. Emoji is not found")

message.text = re.sub(EMOJI_PATTERN, r'', message.text)

try:
    numb_to_conv = float((re.findall(r"\d+(?:.\d+)?", message.text)[0].replace(',', '.')))
except IndexError:
    numb_to_conv = None
    print('Module TRY_NUMB Error, numb_to_conv is not exist.')