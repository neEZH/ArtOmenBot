import telebot
from telebot import types
import os
import aob
from artstation import AS
from pg_database import createDB
import DBWorker as DBw

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
    palette = aob.colormindPalette("default")
    hexPalette = aob.hexPalette(palette)
    aob.getPalette(bot, chatID, hexPalette)


@bot.message_handler(commands=['subs'])
def subscribe(message):
    chatID = message.chat.id
    print("/subs TRIGGERED")
    text = aob.logMsg(message)
    aob.correctSubs(bot, chatID, text, message.from_user, 1, 2)


@bot.message_handler(commands=['t'])
def artur_text(message):
    text = aob.logMsg(message)
    chatID = message.chat.id
    userID = message.from_user.id
    aob.ifArtur(aob.discordText, bot, chatID, userID, text)


@bot.message_handler(commands=['v'])
def artur_text(message):
    text = aob.logMsg(message)
    chatID = message.chat.id
    userID = message.from_user.id
    aob.ifArtur(aob.discordVid, bot, chatID, userID, text)


@bot.message_handler(commands=['a'])
def aa(message):
    DBw.test()


print("Bot starting!!")
createDB()
bot.polling(none_stop=True)
