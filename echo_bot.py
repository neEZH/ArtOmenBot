import telebot
from telebot import types
import os
import aob
from artstation import AS


def logMsg(msg):
    log = "ChatID:" + str(msg.chat.id) + "\n"
    log += "MessageID:" + str(msg.message_id) + "\n"
    log += "From:" + str(msg.from_user.id) + " [" + str(msg.from_user.username) + "]" + "\n"
    log += "Text:" + str(msg.text.split(" ")) + "\n"
    print(log)
    return msg.text.split(" ")


bot = telebot.TeleBot(os.environ['botToken'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Иди рисуй")


@bot.message_handler(commands=['last'])
def showLastWork(message):
    chatID = message.chat.id
    print("/last TRIGGERED")
    text = logMsg(message)
    if aob.lengthCheck(text, 2):
        artist = AS(text[1])
        if artist.ifArtist:
            lastArt = aob.getLastArt(artist)
            bot.send_photo(chatID, lastArt["thumbUrl"], lastArt["projUrl"])
        else:
            answer = "There are no any <b>" + artist.name + "</b> artist on Artstation!\nMay be you meant:"
            markup = aob.searchToKeyboard(artist.name)
            bot.send_message(chatID, answer, reply_markup=markup, parse_mode="HTML")
    else:
        bot.send_message(chatID, "command should be like /last <b>username</b>", parse_mode="HTML")


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
