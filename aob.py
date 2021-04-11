from artstation import AS
from telebot import types


def lengthCheck(textArr, target=1):
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
