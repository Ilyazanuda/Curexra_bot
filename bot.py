# импортируем библеотеку для работы с ботом и файл конфига с токеном
import telebot
from config import TOKEN, Bot_DB, Bot_currency, EMOJI_PATTERN
from telebot import types
import re

# создаём бота
bot = telebot.AsyncTeleBot(TOKEN)
task = bot.get_me()

a = 0
for a in range(100):
    a += 10
# создаём кнопки
# главное меню
button_rates = types.KeyboardButton('\U0001F4C8Курсы валют')
button_converter = types.KeyboardButton('\U0001F4B0Конвертер валют')
button_subscription = types.KeyboardButton('\U00002705Подписка')
# курсы валют
button_usd = types.KeyboardButton('\U0001F1FA\U0001F1F8USD')
button_eur = types.KeyboardButton('\U0001F1EA\U0001F1FAEUR')
button_rub = types.KeyboardButton('\U0001F1F7\U0001F1FARUB')
button_byn = types.KeyboardButton('\U0001F1E7\U0001F1FEBYN')
# подписка
button_sub_morning = types.KeyboardButton('\U0001F3058 утра')
button_sub_evening = types.KeyboardButton('\U0001F3078 вечера')
button_unsubscribe = types.KeyboardButton('\U0000274CОтписка')
# внутренние переходы
button_into_menu = types.KeyboardButton('\U0001F4D1К главному меню')
button_into_rates = types.KeyboardButton('\U000021A9\U0001F4C8К курсам валют')
button_into_conv = types.KeyboardButton('\U000021A9\U0001F4B1Назад к конвертеру')
button_into_back = types.KeyboardButton('\U000021A9Назад')

dict_currency = {1: '\U0001F1FA\U0001F1F8USD', 2: '\U0001F1EA\U0001F1FAEUR', 3: '\U0001F1F7\U0001F1FARUB',
                 4: '\U0001F1E7\U0001F1FEBYN'}

print('Бот запущен.')


def check_message(message):
    print(f'chat_id: {message.chat.id}, user_name: {message.from_user.first_name}, message: {message.text}')


def check_user_db_status(message):
    print(f'stage: {Bot_DB.get_stage(message.chat.id)}, sub: {Bot_DB.get_sub(message.chat.id)} '
          f'buy:{Bot_DB.get_buy(message.chat.id)}, sell: {Bot_DB.get_sell(message.chat.id)}')


def first_currency(message):
    if message.text in ('\U0001F1FA\U0001F1F8USD', 'USD'):
        Bot_DB.update_stage(user_id=message.chat.id, stage=21)
        Bot_DB.update_buy(user_id=message.chat.id, buy=1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_eur, button_rub, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f"Вы выбрали для приобретения \U0001F1FA\U0001F1F8<b><i>USD</i></b>\n"
                         f"Выберите валюту из меню для <b>продажи</b>.",
                         parse_mode='html',
                         reply_markup=markup)
    elif message.text in ('\U0001F1EA\U0001F1FAEUR', 'EUR'):
        Bot_DB.update_stage(user_id=message.chat.id, stage=21)
        Bot_DB.update_buy(user_id=message.chat.id, buy=2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_usd, button_rub, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f"Вы выбрали для приобретения \U0001F1EA\U0001F1FA<b><i>EUR</i></b>\n"
                         f"Выберите валюту из меню для <b>продажи</b>.",
                         parse_mode='html',
                         reply_markup=markup)
    elif message.text in ('\U0001F1F7\U0001F1FARUB', 'RUB'):
        Bot_DB.update_stage(user_id=message.chat.id, stage=21)
        Bot_DB.update_buy(user_id=message.chat.id, buy=3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_usd, button_eur, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f"Вы выбрали для приобретения \U0001F1F7\U0001F1FA<b><i>RUB</i></b>\n"
                         f"Выберите валюту из меню для <b>продажи</b>.",
                         parse_mode='html',
                         reply_markup=markup)
    elif message.text in ('\U0001F1FA\U0001F1F8BYN', 'BYN'):
        Bot_DB.update_stage(user_id=message.chat.id, stage=21)
        Bot_DB.update_buy(user_id=message.chat.id, buy=4)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_eur, button_rub, button_rub)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f"Вы выбрали для приобретения \U0001F1E7\U0001F1FE<b><i>BYN</i></b>\n"
                         f"Выберите валюту из меню для <b>продажи</b>.",
                         parse_mode='html',
                         reply_markup=markup)


# При получении комманды /start и /help выводит меню выбора и текст
@bot.message_handler(commands=['start', 'help'])
def start(message):

    check_message(message=message)

    if not Bot_DB.user_exists(message.chat.id):
        print(f'Пользователя "{message.from_user.first_name}" нет в БД, создаём пользователя...')
        Bot_DB.add_user(message.chat.id)
    else:
        print(f'Пользователь "{message.from_user.first_name}" есть в БД')

    # устанавливаем стадию на которой находится пользователь
    Bot_DB.update_stage(user_id=message.chat.id, stage=0)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_rates, button_converter, button_subscription)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\n'
                                      f'Я проверяю курс обмена валют в соответствии с Национальным банком РБ.\n'
                                      f'Можете сразу перейти по нужным вам пунктам меню:\n'
                                      f'Главное меню - /menu\nМеню курсов валют - /rates\n'
                                      f'Меню конвертера - /conv, /converter\nПодписка - /subscription',
                     reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /menu выводит ~
@bot.message_handler(commands=['menu'])
def menu(message):

    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=0)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_rates, button_converter, button_subscription)
    bot.send_message(message.chat.id, f'Вы перешли в главное меню.\n'
                                      f'Я проверяю курс обмена валют в соответствии с Национальным банком РБ',
                     reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /rates выводит меню курсов валют и текст
@bot.message_handler(commands=['rates'])
def rates(message):

    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=10)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_usd, button_eur, button_rub)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, "Вы перешли в меню \U0001F4C8 <b><i>курсы валют</i></b> \U0001F4C8, "
                                      "выберите валюту из меню.",
                     parse_mode="html",
                     reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /conv или /converter выводит меню выбора валюты для конвертации и текст
@bot.message_handler(commands=['converter', 'conv'])
def converter(message):

    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=20)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_usd, button_eur)
    markup.row(button_rub, button_byn)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, f"Вы перешли в меню \U0001F4B0 <b><i>конвертации валют</i></b> \U0001F4B0\n"
                                      f"Выберите валюту из меню, которую желаете <b>приобрести</b>.",
                     parse_mode='html',
                     reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /subscription
@bot.message_handler(commands=['subscription', 'sub'])
def subscription(message):

    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=60)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_sub_morning, button_sub_evening, button_unsubscribe)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, f"Пы перешли в меню \U00002705 <b><i>подписки</i></b> \U00002705.\n"
                                      f"Выберите варианты подписки на рассылку обновления валют.",
                     parse_mode='html',
                     reply_markup=markup)

    check_user_db_status(message=message)


@bot.message_handler(commands=['unsub', 'unsubscribe'])
def unsubscribe(message):

    check_message(message=message)

    Bot_DB.update_sub(user_id=message.chat.id, sub=0)

    check_user_db_status(message=message)

    pass


# При получении текста проходится по условия и выполняет их
@bot.message_handler(content_types=['text'])
def bot_answer(message):
    check_message(message=message)
    check_user_db_status(message=message)
    # try:
    #     emoji_in_message = re.findall(EMOJI_PATTERN, message.text)[0]
    #     print('Module TRY_EMOJI. Emoji in message:', emoji_in_message)
    # except IndexError:
    #     print("Module TRY_EMOJI. Emoji is not found")
    #
    # message.text = re.sub(EMOJI_PATTERN, r'', message.text)

    # message.text = re.sub(EMOJI_PATTERN, r'', message.text)

    # try:
    #     numb_to_conv = re.sub(EMOJI_PATTERN, r'', message.text)
    #     numb_to_conv = float((re.findall(r"\d+(?:[^a-zA-Z-а-яА-ЯёЁ].\d+|)?", numb_to_conv)[0].replace(',', '.')))
    # except IndexError:
    #     numb_to_conv = None
    #     print('Module TRY_NUMB Error, numb_to_conv is not exist.')
    #
    # if Bot_DB.get_stage(message.chat.id) in (21, 22, 23) and type(numb_to_conv) is float:
    #     print(message.text)
    #     check_message(message=message)
    #     converter_rate(message=message, numb=numb_to_conv)

    # переход в меню курсов валют
    if message.text.lower() in ('\U0001F4C8курсы валют', 'курсы валют', 'курсы'):
        rates(message)
    # переход в меню конвертера
    elif message.text.lower() in ('\U0001F4B0конвертер валют', 'конвертер валют', 'конвертер'):
        converter(message)
    # переход в главное меню
    elif message.text.lower() in ('\U0001F4D1к главному меню', 'к главному меню'):
        menu(message)
    # переход в меню подписки
    elif message.text.lower() in ('\U00002705подписка', 'подписка'):
        subscription(message)
    # кнопка возврата на начальное меню конвертера
    elif message.text.lower() in ('\U000021A9назад', 'назад'):
        if Bot_DB.get_stage(user_id=message.chat.id) == 22:
            converter(message)
    elif Bot_DB.get_stage(user_id=message.chat.id) in (20, 21, 22):
        for i in dict_currency:
            if message.text in dict_currency[i]:
                if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                    first_currency(message=message)
                elif Bot_DB.get_stage(user_id=message.chat.id) == 21:
                    for _ in dict_currency:
                        if message.text in dict_currency[_]:
                            Bot_DB.update_sell(user_id=message.chat.id, sell=_)
                            Bot_DB.update_stage(user_id=message.chat.id, stage=22)
                            bot.send_message(message.chat.id, f'Вы выбрали для продажи <b><i>{dict_currency[_]}</i></b>'
                                                              f'\nВведите сумму, которую хотите <b>приобрести</b>.',
                                             parse_mode='html')
                elif Bot_DB.get_stage(user_id=message.chat.id) == 22:
                    first_currency(message=message)
        if Bot_DB.get_stage(user_id=message.chat.id) == 22:
            message_no_emoji = re.sub(EMOJI_PATTERN, r'', message.text)
            if message_no_emoji.isdigit():
                value = float((re.findall(r"\d+(?:[^a-zA-Z-а-яА-ЯёЁ].\d+|)?",
                                          message_no_emoji)[0].replace(',', '.')))
                bot.send_message(message.chat.id, f"Вы можете приобрести <b>{value} "
                                                  f"{dict_currency[Bot_DB.get_buy(user_id=message.chat.id)]}</b> за <b>"
                                                  f"{Bot_currency.convert_parse(value, user_id=message.chat.id)}"
                                                  f" {dict_currency[Bot_DB.get_sell(user_id=message.chat.id)]}</b>",
                                 parse_mode='html')











    else:
        bot.send_message(message.chat.id, 'Извините, я не понимаю, чего вы хотите.\n'
                                          'Напишите сообщение в рамках того меню в котором находитесь.')



bot.polling(none_stop=True)