import telebot
from telebot import types
import os
import aob
from artstation import AS
import pg_database as pgdb


bot = telebot.TeleBot(os.environ['botToken'])


@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    bot.reply_to(message, f"Иди рисуй")


@bot.message_handler(commands=['last'])
def showLastWork(message):
    chatID = message.chat.id
    print("/last TRIGGERED")
    text = aob.logMsg(message)
    aob.correctLast(bot, chatID, text, nameI=1, textLen=2)


@bot.callback_query_handler(func=lambda call: True)
def callBackLastWork(callBack):
    print("gotcha,", callBack.data)
    artist = AS(callBack.data)
    chatID = callBack.message.chat.id
    aob.sendLastWork(bot, chatID, artist)


@bot.message_handler(commands=['palet'])
def sendPalette(message):
    chatID = message.chat.id
    print("/palet TRIGGERED")
    aob.logMsg(message)
    palette =  aob.colormindPalette("default")
    hexPalette = aob.hexPalette(palette)
    aob.getPalette(bot, chatID, hexPalette)


@bot.message_handler(commands=['a'])
def aa(message):
    answ = ""
    answ += "ChatID: " + str(message.chat.id) + "\n"
    answ += "ChatType: " + str(message.chat.type) + "\n"
    answ += "ChatTitle: " + str(message.chat.title) + "\n"
    # answ += "SenderChatID: " + str(message.sender_chat.id)
    bot.send_message(message.chat.id, answ)


print("Bot starting!!")
# pgdb.createDB()
bot.polling(none_stop=True)
