# импортируем библеотеку для работы с ботом и файл конфига с токеном
import telebot
from config import TOKEN, Bot_DB, EMOJI_PATTERN
from telebot import types
import re

# создаём бота
bot = telebot.TeleBot(TOKEN)
# создаём кнопки
# главное меню
button_rates = types.KeyboardButton('\U0001F4C8Курсы валют')
button_converter = types.KeyboardButton('\U0001F4B1Конвертер валют')
button_subscription = types.KeyboardButton('\U00002705Подписка')
# курсы валют
button_usd_rate = types.KeyboardButton('\U0001F1FA\U0001F1F8Курс доллара ')
button_eur_rate = types.KeyboardButton('\U0001F1EA\U0001F1FAКурс евро')
button_rub_rate = types.KeyboardButton('\U0001F1F7\U0001F1FAКурс рос. рубля')
# конвертер
button_buy_usd = types.KeyboardButton('\U0001F1FA\U0001F1F8Купить доллар')
button_buy_eur = types.KeyboardButton('\U0001F1EA\U0001F1FAКупить евро')
button_buy_rub = types.KeyboardButton('\U0001F1F7\U0001F1FAКупить рубль')
# подписка
button_sub_morning = types.KeyboardButton('\U0001F3058 утра')
button_sub_evening = types.KeyboardButton('\U0001F3078 вечера')
button_unsubscribe = types.KeyboardButton('\U0000274CОтписка')
# внутренние переходы
button_into_menu = types.KeyboardButton('\U0001F4D1К главному меню')
button_into_rates = types.KeyboardButton('\U000021A9\U0001F4C8К курсам валют')
button_into_conv = types.KeyboardButton('\U000021A9\U0001F4B1Назад к конвертеру')
button_into_back = types.KeyboardButton('\U000021A9Назад')

list_emoji = ('\U0001F1FA\U0001F1F8', '\U0001F1EA\U0001F1FA', '\U0001F1F7\U0001F1FA',
              '\U0001F305', '\U0001F307', '\U0000274C', '\U0001F4D1', '\U0001F4C8', '\U0001F4B1', '\U00002705')
print('Бот запущен.')


def check_message(message):
    print(f'chat_id: {message.chat.id}, user_name: {message.from_user.first_name}, message: {message.text}')


def check_user_db_status(message):
    print(f'stage: {Bot_DB.get_stage(message.chat.id)}, sub: {Bot_DB.get_sub(message.chat.id)}')


def converter_rate(message, numb):
    rate = 2.50
    result = numb * rate
    return bot.send_message(message.chat.id, f"Количество валюты {numb} можно купить за {str(result)} BYN")


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
    markup.row(button_usd_rate, button_eur_rate, button_rub_rate)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, "Вы перешли в меню курсов валют, выберите валюту из меню.", reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /conv или /converter выводит меню выбора валюты для конвертации и текст
@bot.message_handler(commands=['converter', 'conv'])
def converter(message):

    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=20)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_buy_usd, button_buy_eur, button_buy_rub)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, f"Вы перешли в меню конвертации валют, выберите валюту из меню.",
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
    bot.send_message(message.chat.id, f"Выберите варианты подписки на рассылку обновления валют.",
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

    # try:
    #     emoji_in_message = re.findall(EMOJI_PATTERN, message.text)[0]
    #     print('Module TRY_EMOJI. Emoji in message:', emoji_in_message)
    # except IndexError:
    #     print("Module TRY_EMOJI. Emoji is not found")
    #
    # message.text = re.sub(EMOJI_PATTERN, r'', message.text)

    message.text = re.sub(EMOJI_PATTERN, r'', message.text)

    try:
        numb_to_conv = re.sub(EMOJI_PATTERN, r'', message.text)
        numb_to_conv = float((re.findall(r"\d+(?:[^a-zA-Z-а-яА-ЯёЁ].\d+|)?", numb_to_conv)[0].replace(',', '.')))
    except IndexError:
        numb_to_conv = None
        print('Module TRY_NUMB Error, numb_to_conv is not exist.')

    if Bot_DB.get_stage(message.chat.id) in (21, 22, 23) and type(numb_to_conv) is float:
        print(message.text)
        check_message(message=message)
        converter_rate(message=message, numb=numb_to_conv)

    # переход в меню курсов валют
    elif message.text.lower() in ('\U0001F4C8курсы валют', 'курсы валют', 'курсы'):
        rates(message)
    # переход в меню конвертера
    elif message.text.lower() in ('\U0001F4B1конвертер валют', 'конвертер валют', 'конвертер'):
        converter(message)
    # переход в главное меню
    elif message.text.lower() in '\U0001F4D1к главному меню':
        menu(message)
    # переход в меню подписки
    elif message.text.lower() in ('\U00002705подписка', 'подписка'):
        subscription(message)
    # elif Bot_DB.get_stage(message.chat.id) in (10, 11, 12, 13):


    elif message.text.lower() in ('\U0001F1FA\U0001F1F8купить доллар', 'купить доллар'):
        check_message(message=message)

        Bot_DB.update_stage(user_id=message.chat.id, stage=21)
        bot.send_message(message.chat.id, 'Вы выбрали доллар \U0001F1FA\U0001F1F8, '
                                          'напишите сумму которую хотите конвертировать.')

        check_user_db_status(message=message)

    elif message.text.lower() == 'купить евро':
        check_message(message=message)

        Bot_DB.update_stage(user_id=message.chat.id, stage=22)
        bot.send_message(message.chat.id, 'Вы выбрали евро \U0001F1EA\U0001F1FA, '
                                          'напишите сумму которую хотите конвертировать.')

        check_user_db_status(message=message)

    elif message.text.lower() == 'купить рубль':
        check_message(message=message)

        Bot_DB.update_stage(user_id=message.chat.id, stage=23)
        bot.send_message(message.chat.id, 'Вы выбрали рубль \U0001F1F7\U0001F1FA.\n'
                                          'Напишите сумму, которую хотите конвертировать.')

        check_user_db_status(message=message)
    else:
        bot.send_message(message.chat.id, 'Извините, я не понимаю, чего вы хотите.\n'
                                          'Напишите сообщение в рамках того меню в котором находитесь.')



bot.polling(none_stop=True)