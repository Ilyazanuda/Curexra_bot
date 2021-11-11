from config import TOKEN, Bot_DB, Bot_currency, EMOJI_PATTERN, check_chat
from telebot import types
from time import sleep
import random
import telebot
import time
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
# dict with currencies and flag emoji
dict_curr = {1: ('\U0001F1FA\U0001F1F8usd', 'usd'), 2: ('\U0001F1EA\U0001F1FAeur', 'eur'),
             3: ('\U0001F1F7\U0001F1FArub', 'rub'), 4: ('\U0001F1E7\U0001F1FEbyn', 'byn')}

idk_answer = 'Извините, я не понимаю, чего вы хотите.\nНапишите сообщение в рамках того меню, в котором находитесь.'
print('Bot launched.')


def check_request(message):
    print(f'{"/" + "-" * 90 + "/"}\nchat_id: {message.chat.id}, user_name: {message.from_user.first_name},'
          f' message: {message.text}, time: {time.strftime("%c")}')
    try:
        print(f'stage: {Bot_DB.get_stage(message.chat.id)}, sub: {Bot_DB.get_sub(message.chat.id)} '
              f'buy:{Bot_DB.get_buy(message.chat.id)}, sell: {Bot_DB.get_sell(message.chat.id)}')
    except TypeError:
        print('User was not found in the database.')


def delete_emoji(text):
    return re.sub(EMOJI_PATTERN, r'', text)


def first_currency(message):
    Bot_DB.update_stage(user_id=message.chat.id, stage=21)
    if message.text.lower() in dict_curr[1]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_eur, button_rub, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id, f'Вы выбрали для <b>приобретения <i>{dict_curr[1][0].upper()}</i></b>\n'
                                          f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html', reply_markup=markup)
    elif message.text.lower() in dict_curr[2]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_usd, button_rub, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id, f'Вы выбрали для <b>приобретения <i>{dict_curr[2][0].upper()}</i></b>\n'
                                          f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html', reply_markup=markup)
    elif message.text.lower() in dict_curr[3]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=3)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_usd, button_eur, button_byn)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id, f'Вы выбрали для <b>приобретения <i>{dict_curr[3][0].upper()}</i></b>\n'
                                          f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html', reply_markup=markup)
    elif message.text.lower() in dict_curr[4]:
        Bot_DB.update_buy(user_id=message.chat.id, buy=4)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(button_eur, button_rub, button_rub)
        markup.row(button_into_back)
        markup.row(button_into_menu)
        bot.send_message(message.chat.id, f'Вы выбрали для <b>приобретения <i>{dict_curr[4][0].upper()}</i></b>\n'
                                          f'Выберите валюту из меню для <b>продажи</b>.',
                         parse_mode='html', reply_markup=markup)


def second_currency(message):
    for _ in dict_curr:
        if message.text.lower() in dict_curr[_]:
            Bot_DB.update_sell(user_id=message.chat.id, sell=_)
            Bot_DB.update_stage(user_id=message.chat.id, stage=22)
            bot.send_message(message.chat.id, f'Вы выбрали для <b>продажи <i>{dict_curr[_][0].upper()}</i></b>'
                                              f'\nВведите сумму, которую хотите <b>приобрести</b>.',
                             parse_mode='html')


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.text == '/start':
        check_request(message=message)
    if not Bot_DB.user_exists(message.chat.id):
        print(f'User "{message.from_user.first_name}" was not found in the database, create a new record...')
        Bot_DB.add_user(message.chat.id)
    else:
        print(f'Record about user "{message.from_user.first_name}" is in the database.')
    Bot_DB.update_stage(user_id=message.chat.id, stage=0)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_rates, button_converter, button_subscription)
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}!\n'
                                      f'Я проверяю курс обмена валют в соответствии с лучшими курсами с сервиса '
                                      f'<b><i>myfin</i></b> '
                                      f'Беларусь.\nМожете сразу перейти по нужным вам пунктам меню, '
                                      f'введя данные команды:\n'
                                      f'Главное меню - /menu\nМеню курсов валют - /rates\n'
                                      f'Меню конвертера - /conv, /converter\nРассылка - /mailing',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    if message.text == '/menu':
        check_request(message=message)
    Bot_DB.update_stage(user_id=message.chat.id, stage=0)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_rates, button_converter, button_subscription)
    bot.send_message(message.chat.id, f'Вы перешли в <b><i>Главное меню</i></b>\n'
                                      f'Я проверяю курс обмена валют в соответствии с лучшими курсами с сервиса '
                                      f'<b><i>myfin</i></b>',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['rates'])
def rates(message):
    Bot_DB.update_stage(user_id=message.chat.id, stage=10)
    if message.text == '/rates':
        check_request(message=message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_usd, button_eur, button_rub)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, 'Вы перешли в меню \U0001F4C8 <b><i>Курсы валют</i></b> \U0001F4C8\n'
                                      'Чтобы узнать курс выберите интересующую вас <b>валюту</b>.',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['converter', 'conv'])
def converter(message):
    if message.text in ('/converter', '/conv'):
        check_request(message=message)
    Bot_DB.update_stage(user_id=message.chat.id, stage=20)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_usd, button_eur)
    markup.row(button_rub, button_byn)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, f'Вы перешли в меню \U0001F4B0 <b><i>Конвертации валют</i></b> \U0001F4B0\n'
                                      f'Выберите валюту из меню, которую желаете <b>приобрести</b>.',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['mailing', 'mail'])
def subscription(message):
    if message.text in ('/mailing', '/mail'):
        check_request(message=message)
    Bot_DB.update_stage(user_id=message.chat.id, stage=60)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(button_sub_morning, button_sub_evening, button_unsubscribe)
    markup.row(button_into_menu)
    bot.send_message(message.chat.id, f'Вы перешли в меню \U0001F4EC <b><i>Рассылка "Курсы валют"</i></b> \U0001F4EC\n'
                                      f'Выберите варианты подписки на ежедневную рассылку, всё абсолютно '
                                      f'<b>бесплатно</b>, <b>без смс</b> и <b>регистрации</b>.',
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['unsub', 'unsubscribe'])
def unsubscribe(message):
    if message.text in ('/unsub', '/unsubscribe'):
        check_request(message=message)
    Bot_DB.update_sub(user_id=message.chat.id, sub=0)
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, теперь вы отписаны от рассылки '
                                      f'<b><i>"Курсы валют"</i></b>\nЯ в вас разочарован...',
                     parse_mode='html')


@bot.message_handler(content_types=['sticker', 'photo', 'audio'])
def sticker(message):
    check_request(message=message)
    rand_sticker = random.choice(((open('stickers\\stick_1_1.webp', 'rb'), open('stickers\\stick_1_2.webp', 'rb')),
                                  (open('stickers\\stick_2_1.webp', 'rb'), open('stickers\\stick_2_2.webp', 'rb')),
                                  (open('stickers\\stick_3_1.webp', 'rb'), open('stickers\\stick_3_2.webp', 'rb')),
                                  (open('stickers\\stick_4_1.webp', 'rb'), open('stickers\\stick_4_2.webp', 'rb'))))
    bot.send_sticker(message.chat.id, rand_sticker[0])
    sleep(1.8)
    bot.send_sticker(message.chat.id, rand_sticker[1])


@bot.message_handler(content_types=['text'])
def bot_answer(message):
    try:
        check_request(message=message)
        message.text = delete_emoji(text=message.text)
        if message.text.lower() in ('курсы валют', 'курсы'):
            rates(message)
        elif message.text.lower() in ('конвертер валют', 'конвертер'):
            converter(message)
        elif message.text.lower() == 'к главному меню':
            menu(message)
        elif message.text.lower() == 'рассылка':
            subscription(message)
        elif message.text.lower() == '8 утра':
            Bot_DB.update_sub(user_id=message.chat.id, sub=1)
            bot.send_message(message.chat.id, 'Вы подписались на ежедневную рассылку <b><i>"Курсы валют"</i></b>, '
                                              'которая будет производится в 8 утра.',
                             parse_mode='html')
        elif message.text.lower() == '8 вечера':
            Bot_DB.update_sub(user_id=message.chat.id, sub=2)
            bot.send_message(message.chat.id, 'Вы подписались на рассылку <b><i>"Курсы валют"</i></b>, '
                                              'которая будет производится в 8 вечера.',
                             parse_mode='html')
        elif message.text.lower() in ('отписка', 'unub'):
            unsubscribe(message=message)
        elif message.text.lower() in ('назад', '/back'):
            if Bot_DB.get_stage(user_id=message.chat.id) in (21, 22):
                converter(message)
        elif Bot_DB.get_stage(user_id=message.chat.id) in (10, 20, 21, 22):
            for i in dict_curr:
                if message.text.lower() in dict_curr[i]:
                    if Bot_DB.get_stage(user_id=message.chat.id) == 20:
                        first_currency(message=message)
                        break
                    elif Bot_DB.get_stage(user_id=message.chat.id) in (21, 22):
                        second_currency(message=message)
                        break
                    elif Bot_DB.get_stage(user_id=message.chat.id) == 10:
                        rates_list = Bot_currency.rates(delete_emoji(text=message.text).lower())
                        rates_answer = (f'Курсы указаны в соотвествии с лучшими курсами <i><b>myfin</b></i>\n'
                                        f'Курс <b>покупки {dict_curr[i][0].upper()}</b>: {rates_list[0]} '
                                        f'<b>{dict_curr[4][0].upper()}</b>\n'
                                        f'Курс <b>продажи {dict_curr[i][0].upper()}</b>: {rates_list[1]} '
                                        f'<b>{dict_curr[4][0].upper()}</b>')
                        bot.send_message(message.chat.id, rates_answer, parse_mode='html')
                        break
                elif Bot_DB.get_stage(user_id=message.chat.id) == 22 and \
                        message.text.replace(',', '').replace('.', '').replace(' ', '').isdigit():
                    value = float((re.findall(r'\d+(?:[^a-zA-Z-а-яА-ЯёЁ].?\d+|)?',
                                              message.text)[0].replace(',', '.')))
                    print(f'The number "{value}" has come and ready for exchange.')
                    if Bot_DB.get_buy(user_id=message.chat.id) != Bot_DB.get_sell(user_id=message.chat.id):
                        answer_convert = (f'Вы можете приобрести <b>{value} '
                                          f'{dict_curr[Bot_DB.get_buy(user_id=message.chat.id)][0].upper()}</b> за '
                                          f'<b>{Bot_currency.convert(value, user_id=message.chat.id)} '
                                          f'{dict_curr[Bot_DB.get_sell(user_id=message.chat.id)][0].upper()}</b>')
                        bot.send_message(message.chat.id, answer_convert, parse_mode='html')
                        break
                    else:
                        bot.send_message(message.chat.id, f'Что-то вы напортачили, '
                                                          f'попробуйте выбрать другую <b>валюту</b>.',
                                         parse_mode='html')
                        break
            else:
                bot.send_message(message.chat.id, idk_answer)
        else:
            bot.send_message(message.chat.id, idk_answer)
    except IndexError:
        print(f"{'-' * 8}\nIndexError\n{'-' * 8}")
        bot.send_message(check_chat, 'IndexError')
        bot.send_message(message.chat.id, idk_answer)
    except ValueError:
        print(f"{'-' * 8}\nValueError\n{'-' * 8}")
        bot.send_message(check_chat, 'ValueError')
        bot.send_message(message.chat.id, idk_answer)
    except TypeError:
        bot.send_message(message.chat.id, f'Здравствуйте, <b>{message.from_user.first_name}</b>, вы ещё со мной не '
                                          f'общались, я вас не помню, чтобы я вас записал в книжку, '
                                          f'напишите команду <b>/start</b>',
                         parse_mode='html')
        print(f"{'-' * 8}\nTypeError\n{'-' * 8}")
        bot.send_message(check_chat, 'TypeError')


if __name__ == '__main__':
    bot.polling(none_stop=True)
