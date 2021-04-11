import telebot
from telebot import types
import os
import aob
#from artstation import AS


bot = telebot.TeleBot(os.environ['botToken'])


@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    bot.reply_to(message, f"Иди рисуй")


@bot.message_handler(commands=['last'])
def showLastWork(message):
    chatID = message.chat.id
    print("/last TRIGGERED")
    text = aob.logMsg(message)
    aob.correctLast(bot, chatID, text)


@bot.callback_query_handler(func=lambda call: True)
def callLastWork(callBack):
    print("gotcha,", callBack.data)
    callBack.message.text = "last " + str(callBack.data)
    showLastWork(callBack.message)


@bot.message_handler(commands=['a'])
def aa(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    button = types.InlineKeyboardButton(text="a", callback_data="a")
    markup.add(button)
    markup.add(button)
    markup.add(button)

    bot.send_message(message.chat.id, "hello there", reply_markup=markup)


print("Bot starting!!")
bot.polling(none_stop=True)
