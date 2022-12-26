import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

bot = telebot.TeleBot("5868878555:AAEetjhGk43IZ2LasbIa9vKbzTNCQ92slrs")

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать курс валюты")
    markup.add(item1)
    msg = bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>\nБот, который способен на все.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(msg, main)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == 'Узнать курс валюты':
     msg = bot.send_message(message.chat.id, 'Мы пока можем показать эти валюты:\n'
                                            'США - 1\nЕвро - 2\nКитай - 3\nАрмения - 4\nАвстралия - 5\nАзербайджан - 6.\n\n'
                                            'Введите номер валюты курс которой хотите узнать')
     bot.register_next_step_handler(msg, currency_show)


def currency_show(message):
    msg  = int(message.text)
    url = 'https://www.sravni.ru/valjuty/moskva/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    data = soup.find(class_="Table_row__H8plF Table_row-hover__cShKF")
    string = str(soup.find_all(class_="Table_row__H8plF Table_row-hover__cShKF")[msg-1])
    result = string[string.find('3Dj3x">') + 7:string.find('<!-- -->'):] 
    bot.send_message(message.chat.id, result + ' рубля(ей)')
    bot.send_message(message.chat.id, 'Если хотите узнать курс другой валюты используйте команду /start')


bot.polling(none_stop=True)