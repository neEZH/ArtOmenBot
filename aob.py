from artstation import AS
from telebot import types


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


def correctLast(bot, chatID, text):
    if msgLenCheck(text, 2):
        artist = AS(text[1])
        sendLastWork(bot, artist, chatID)
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