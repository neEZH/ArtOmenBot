import telebot
# from telebot import types
import os
import aob
from artstation import AS
import schedule
import threading
import time

# from pg_database import createDB
# import DBWorker as DBw

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
    aob.discordBDay()


@bot.message_handler(commands=['idea'])
def sendIdea(message):
    text = aob.getIdea()
    chatID = message.chat.id
    bot.send_message(chatID, text)



'''
    Thread for scheduled actions
'''


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


'''
    SCHEDULED ACTIONS
'''


def birthdayReminder():
    aob.bDayGreetings(bot)


schedule.every().day.at("08:00").do(birthdayReminder)
stop_run_continuously = run_continuously()
'''
    Calling bot polling
'''

print("Bot starting!!")
# createDB()
bot.polling(none_stop=True)

'''
    Calling thread with scheduler
'''
time.sleep(10)
stop_run_continuously.set()
