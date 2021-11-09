from config import TOKEN, Bot_DB, Bot_currency, EMOJI_PATTERN
from telebot import types
from time import sleep
import random
import sqlite3
import telebot
import re
# create var bot
bot = telebot.AsyncTeleBot(TOKEN)
# create buttons for main menus
button_rates = types.KeyboardButton('\U0001F4C8Курсы валют')
button_converter = types.KeyboardButton('\U0001F4B0Конвертер валют')
button_subscription = types.KeyboardButton('\U0001F4ECРассылка')
# create buttons for currencies
button_usd = types.KeyboardButton('\U0001F1FA\U0001F1F8USD')
button_eur = types.KeyboardButton('\U0001F1EA\U0001F1FAEUR')
button_rub = types.KeyboardButton('\U0001F1F7\U0001F1FARUB')
button_byn = types.KeyboardButton('\U0001F1E7\U0001F1FEBYN')
# create buttons for mailing
button_sub_morning = types.KeyboardButton('\U0001F3058 утра')
button_sub_evening = types.KeyboardButton('\U0001F3078 вечера')
button_unsubscribe = types.KeyboardButton('\U0000274CОтписка')
# create back buttons
button_into_menu = types.KeyboardButton('\U0001F4D1К главному меню')
button_into_back = types.KeyboardButton('\U000021A9Назад')

dict_currencies = {1: '\U0001F1FA\U0001F1F8usd', 2: '\U0001F1EA\U0001F1FAeur', 3: '\U0001F1F7\U0001F1FArub',
                   4: '\U0001F1E7\U0001F1FEbyn'}
idk_answer = 'Извините, я не понимаю, чего вы хотите.\nНапишите сообщение в рамках того меню, в котором находитесь.'

print('Bot launched.')


def check_message(message):
    print(f'chat_id: {message.chat.id}, user_name: {message.from_user.first_name}, message: {message.text}')


def check_user_db_status(message):
    try:
        print(f'stage: {Bot_DB.get_stage(message.chat.id)}, sub: {Bot_DB.get_sub(message.chat.id)} '
              f'buy:{Bot_DB.get_buy(message.chat.id)}, sell: {Bot_DB.get_sell(message.chat.id)}')
    except TypeError:
        print('User is not in database')


def delete_emoji(message):
    return re.sub(EMOJI_PATTERN, r'', message.text)


def first_currency(message):
    Bot_DB.update_stage(user_id=message.chat.id, stage=21)
    if message.text.lower() in dict_currencies[1]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_eur, button_rub, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f'Вы выбрали для <b>приобретения <i>{dict_currencies[1].upper()}</i></b>\n'
                         f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html',
                         reply_markup=markup)
    elif message.text.lower() in dict_currencies[2]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_usd, button_rub, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f'Вы выбрали для <b>приобретения <i>{dict_currencies[2].upper()}</i></b>\n'
                         f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html',
                         reply_markup=markup)
    elif message.text.lower() in dict_currencies[3]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_usd, button_eur, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f'Вы выбрали для <b>приобретения <i>{dict_currencies[3].upper()}</i></b>\n'
                         f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html',
                         reply_markup=markup)
    elif message.text.lower() in dict_currencies[4]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=4)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_eur, button_rub, button_rub)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id,
                         f'Вы выбрали для <b>приобретения <i>{dict_currencies[4].upper()}</i></b>\n'
                         f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html',
                         reply_markup=markup)


def second_currency(message):
    for _ in dict_currencies:
        if message.text.lower() in dict_currencies[_]:
            Bot_DB.update_sell(user_id=message.chat.id, sell=_)
            Bot_DB.update_stage(user_id=message.chat.id, stage=22)
            bot.send_message(message.chat.id, f'Вы выбрали для <b>продажи <i>{dict_currencies[_].upper()}</i></b>'
                                              f'\nВведите сумму, которую хотите <b>приобрести</b>.',
                             parse_mode='html')


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
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!\n'
                                      f'Я проверяю курс обмена валют в соответствии с лучшими курсами с сайта '
                                      f'<b><i>myfin.by</i></b> '
                                      f'Беларусь.\nМожете сразу перейти по нужным вам пунктам меню, '
                                      f'введя данные команды:\n'
                                      f'Главное меню - /menu\nМеню курсов валют - /rates\n'
                                      f'Меню конвертера - /conv, /converter\nРассылка - /mailing',
                     reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /menu выводит ~
@bot.message_handler(commands=['menu'])
def menu(message):

    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=0)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_rates, button_converter, button_subscription)
    bot.send_message(message.chat.id, f'Вы перешли в <b><i>Главное меню</i></b>\n'
                                      f'Я проверяю курс обмена валют в соответствии с лучшими курсами с сайта'
                                      f'<b><i>myfin.by</i></b>',
                     parse_mode='html',
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
    bot.send_message(message.chat.id, 'Вы перешли в меню \U0001F4C8 <b><i>Курсы валют</i></b> \U0001F4C8\n'
                                      'Чтобы узнать курс выберите интересующую вас <b>валюту</b>.',
                     parse_mode='html',
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
    bot.send_message(message.chat.id, f'Вы перешли в меню \U0001F4B0 <b><i>Конвертации валют</i></b> \U0001F4B0\n'
                                      f'Выберите валюту из меню, которую желаете <b>приобрести</b>.',
                     parse_mode='html',
                     reply_markup=markup)

    check_user_db_status(message=message)


# При получении комманды /mailing
@bot.message_handler(commands=['mailing', 'mail'])
def subscription(message):
    check_message(message=message)

    Bot_DB.update_stage(user_id=message.chat.id, stage=60)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_sub_morning, button_sub_evening, button_unsubscribe)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, f'Вы перешли в меню \U0001F4EC <b><i>Рассылка "Курсы валют"</i></b> \U0001F4EC\n'
                                      f'Выберите варианты подписки на ежедневную рассылку, всё абсолютно '
                                      f'<b>бесплатно</b>, <b>без смс</b> и <b>регистрации</b>.',
                     parse_mode='html',
                     reply_markup=markup)

    check_user_db_status(message=message)


# функция отписки
@bot.message_handler(commands=['unsub', 'unsubscribe'])
def unsubscribe(message):
    check_message(message=message)
    Bot_DB.update_sub(user_id=message.chat.id, sub=0)
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, теперь вы отписаны от рассылки '
                                      f'<b><i>"Курсы валют"</i></b>\nЯ в вас разочарован...',
                     parse_mode='html')
    check_user_db_status(message=message)


@bot.message_handler(content_types=['sticker', 'photo', 'audio'])
def sticker(message):
    sticker_list = ((open('stickers\\stick_1_1.webp', 'rb'), open('stickers\\stick_1_2.webp', 'rb')),
                    (open('stickers\\stick_2_1.webp', 'rb'), open('stickers\\stick_2_2.webp', 'rb')),
                    (open('stickers\\stick_3_1.webp', 'rb'), open('stickers\\stick_3_2.webp', 'rb')),
                    (open('stickers\\stick_4_1.webp', 'rb'), open('stickers\\stick_4_2.webp', 'rb')))
    rand_sticker = random.choice(sticker_list)
    bot.send_sticker(message.chat.id, rand_sticker[0])
    sleep(2)
    bot.send_sticker(message.chat.id, rand_sticker[1])


# При получении текста проходится по условия и выполняет их
@bot.message_handler(content_types=['text'])
def bot_answer(message):
    try:
        check_message(message=message)
        check_user_db_status(message=message)

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
        elif message.text.lower() in ('\U0001F4ECрассылка', 'рассылка'):
            subscription(message)
        elif message.text.lower() in ('\U0001F3058 утра', '8 утра'):
            Bot_DB.update_sub(user_id=message.chat.id, sub=1)
            bot.send_message(message.chat.id, 'Вы подписались на рассылку <b><i>"Курсы валют"</i></b> на 8 утра.',
                             parse_mode='html')
        elif message.text.lower() in ('\U0001F3078 вечера', '8 вечера'):
            Bot_DB.update_sub(user_id=message.chat.id, sub=2)
            bot.send_message(message.chat.id, 'Вы подписались на рассылку <b><i>"Курсы валют"</i></b> на 8 вечера.',
                             parse_mode='html')
        elif message.text.lower() in ('\U0000274Cотписка', 'отписка'):
            unsubscribe(message=message)
        # кнопка возврата на начальное меню конвертера
        elif message.text.lower() in ('\U000021A9назад', 'назад', '/back'):
            if Bot_DB.get_stage(user_id=message.chat.id) in (21, 22):
                converter(message)
        # принимает сообщения только с указынными стадиями
        elif Bot_DB.get_stage(user_id=message.chat.id) in (10, 20, 21, 22):
            for i in dict_currencies:
                if message.text.lower() in dict_currencies[i]:
                    # приимает сообщение на стадии 20 (конвертер, выбор первой валюты)
                    if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                        first_currency(message=message)
                    # принимает сообщение на стадиях 20, 21 (конвертер, выбор второй валюты или изменение выбора)
                    elif Bot_DB.get_stage(user_id=message.chat.id) in (21, 22):
                        second_currency(message=message)
                    # принимает сообщение на стадии 10 (курсы валют, выбор валюты и перевыбор)
                    elif Bot_DB.get_stage(user_id=message.chat.id) == 10:
                        rates_list = Bot_currency.rates(delete_emoji(message).lower())
                        rates_answer = (f'Курсы указаны в соотвествии с <b>НБРБ</b>\n'
                                        f'Курс <b>покупки {dict_currencies[i].upper()}</b>: {rates_list[0]} '
                                        f'<b>{dict_currencies[4].upper()}</b>\n'
                                        f'Курс <b>продажи {dict_currencies[i].upper()}</b>: {rates_list[1]} '
                                        f'<b>{dict_currencies[4].upper()}</b>')
                        bot.send_message(message.chat.id, rates_answer,
                                         parse_mode='html')
                    else:
                        bot.send_message(message.chat.id, idk_answer)
            # приём сообщения на стадии 22 (конвертер, ввод конвертируемой суммы)
            if Bot_DB.get_stage(user_id=message.chat.id) == 22:
                message_no_emoji = delete_emoji(message=message)
                if message_no_emoji.replace(',', '').replace('.', '').isdigit():
                    value = float((re.findall(r'\d+(?:[^a-zA-Z-а-яА-ЯёЁ].?\d+|)?',
                                              message_no_emoji)[0].replace(',', '.')))
                    print(f'Пришло число для конвертации {value}')
                    # если валюта покупки != валюте продажи, число передаётся в конвертер, если равна, то выводит сообщ.
                    if Bot_DB.get_buy(user_id=message.chat.id) != Bot_DB.get_sell(user_id=message.chat.id):
                        answer_convert = (f'Вы можете приобрести <b>{value} '
                                          f'{dict_currencies[Bot_DB.get_buy(user_id=message.chat.id)].upper()}</b> за <b>'
                                          f'{Bot_currency.convert(value, user_id=message.chat.id)} '
                                          f'{dict_currencies[Bot_DB.get_sell(user_id=message.chat.id)].upper()}</b>')
                        bot.send_message(message.chat.id, answer_convert,
                                         parse_mode='html')
                    else:
                        bot.send_message(message.chat.id, f'Что-то вы напортачили, '
                                                          f'попробуйте выбрать другую <b>валюту</b>.',
                                         parse_mode='html')
        else:
            bot.send_message(message.chat.id, idk_answer)
    except IndexError:
        print(f"{'-' * 8}\nIndexError\n{'-' * 8}")
        bot.send_message(-607441191, 'IndexError')
    except ValueError:
        print(f"{'-' * 8}\nValueError\n{'-' * 8}")
        bot.send_message(-607441191, 'ValueError')

    except TypeError:
        bot.send_message(message.chat.id, f'Здравствуйте, <b>{message.from_user.first_name}</b>, вы ещё со мной не '
                                          f'общались, я вас не помню, чтобы я вас узнал, '
                                          f'напишите команду <b>/start</b>',
                         parse_mode='html')
        print(f"{'-' * 8}\nTypeError\n{'-' * 8}")
        bot.send_message(-607441191, 'TypeError')
    except sqlite3.InterfaceError:
        print('sqlite3.InterfaceError')
        # bot.send_message(message.chat.id, f'Воу, самая бысрая рука на диком западе, угомонись')
        bot.send_message(-607441191, 'sqlite3.InterfaceError')
    except sqlite3.ProgrammingError:
        print('sqlite3.ProgrammingError')
        bot.send_message(-607441191, 'sqlite3.ProgrammingError')
    finally:
        check_user_db_status(message=message)


if __name__ == '__main__':
        bot.polling(none_stop=True)
