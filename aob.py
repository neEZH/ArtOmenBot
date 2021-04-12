from artstation import AS
from telebot import types
import requests
import json


def logMsg(msg):
    log = "ChatID:" + str(msg.chat.id) + "\n"
    log += "MessageID:" + str(msg.message_id) + "\n"
    log += "From:" + str(msg.from_user.id) + " [" + str(msg.from_user.username) + "]" + "\n"
    log += "Text:" + str(msg.text.split(" "))
    print(log)
    return msg.text.split(" ")


def msgLenCheck(textArr, target=1):
    if len(textArr) >= target:
        return True
    else:
        return False


def getLastArt(artist):
    lastProjs = artist.lastArt
    projUrl = lastProjs['permalink']
    thumbUrl = lastProjs['cover']['small_square_url']
    print("projUrl: " + projUrl)
    print("thumbUrl: " + thumbUrl)
    return {"projUrl": projUrl, "thumbUrl": thumbUrl}


def searchToKeyboard(name):
    markup = types.InlineKeyboardMarkup(row_width=1)

    for candidate in AS.findArtist(name):
        name = candidate["username"]
        markup.add(types.InlineKeyboardButton(text=name, callback_data=name))
    return markup


def correctLast(bot, chatID, text, nameI=0, textLen=1):
    if msgLenCheck(text, textLen):
        artist = AS(text[nameI])
        sendLastWork(bot, chatID, artist )
    else:
        bot.send_message(chatID, "command should be like /last <b>username</b>", parse_mode="HTML")


def sendLastWork(bot, chatID, artist):
    if artist.ifArtist:
        lastArt = getLastArt(artist)
        bot.send_photo(chatID, lastArt["thumbUrl"], lastArt["projUrl"])
    else:
        answer = "There are no any <b>" + artist.name + "</b> artist on Artstation!\nMay be you meant:"
        markup = searchToKeyboard(artist.name)
        bot.send_message(chatID, answer, reply_markup=markup, parse_mode="HTML")


def colormindPalete(model):
    url = "http://colormind.io/api/"
    raw_data = '{"model":"'+model+'"}'
    response = requests.get(url, data=raw_data)
    return json.loads(response.text)["result"]


def getPalette(bot, chatID, palette):
    msg = "Your palette (RGB):\n"
    for color in palette:
        msg += str(color) + "\n"
    bot.send_message(chatID, msg)
