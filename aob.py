from artstation import AS
from telebot import types
import os
import requests
import json
import DBWorker

'''
SOME ADDDITIONAL METHODS
'''


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


'''
DISCORD WEBHOOKS
'''


def urNotArtur(bot, chatID):
    bot.send_message(chatID, "Ты не Артур. Ухади.")


def ifArtur(func, bot, chatID, userID, text):
    okUsersArr = os.environ['artur'].split(",")
    okUsersArr = [int(i) for i in okUsersArr]
    print(type(okUsersArr), okUsersArr)
    if userID in okUsersArr:
        func(bot, chatID, text)
    else:
        urNotArtur(bot, chatID)


def discordText(bot, chatID, text):
    if msgLenCheck(text, 2):
        raw_data = {"content": str(text[1])}
        url = os.environ['discord_webhook_text']
        requests.post(url, data=raw_data)
    else:
        bot.send_message(chatID, "command should be like /t <b>https://yoursite.net</b>", parse_mode="HTML")


def discordVid(bot, chatID, text):
    if msgLenCheck(text, 2):
        raw_data = {"content": str(text[1])}
        url = os.environ['discord_webhook_vid']
        requests.post(url, data=raw_data)
    else:
        bot.send_message(chatID, "command should be like /v <b>https://yoursite.net</b>", parse_mode="HTML")


'''
LAST ART METHODS
'''


def getLastArt(artist):
    # takes artist[AS] and returns its object with last art project
    lastProjs = artist.lastArt
    projUrl = lastProjs['permalink']
    thumbUrl = lastProjs['cover']['small_square_url']
    postDate = lastProjs['published_at']
    print("projUrl: " + projUrl)
    print("thumbUrl: " + thumbUrl)
    return {"projUrl": projUrl, "thumbUrl": thumbUrl, "postDate": postDate}


def searchToKeyboard(name):
    # takes name[STRING] and gets from AS-object array of results of search. and converts array to TG InlineKeyboardMarkup then returns this
    markup = types.InlineKeyboardMarkup(row_width=1)

    for candidate in AS.findArtist(name):
        name = candidate["username"]
        markup.add(types.InlineKeyboardButton(text=name, callback_data=name))
    return markup


def correctLast(bot, chatID, text, nameI=0, textLen=1):
    # cheks if /last command was correct. if false -> send info message
    if msgLenCheck(text, textLen):
        artist = AS(text[nameI])
        sendLastWork(bot, chatID, artist)
    else:
        bot.send_message(chatID, "command should be like /last <b>username</b>", parse_mode="HTML")


def sendLastWork(bot, chatID, artist):
    # check if there artist with exactly username. if false -> proposing search results
    if artist.ifArtist:
        lastArt = getLastArt(artist)
        bot.send_photo(chatID, lastArt["thumbUrl"], lastArt["projUrl"])
    else:
        answer = "There are no any <b>" + artist.name + "</b> artist on Artstation!\nMay be you meant:"
        markup = searchToKeyboard(artist.name)
        bot.send_message(chatID, answer, reply_markup=markup, parse_mode="HTML")


'''
SUBSCRIBE METHODS GOES HERE
'''


def correctSubs(bot, chatID, text, user, nameI=0, textLen=1):
    # cheks if /subs command was correct. if false -> send info message
    if msgLenCheck(text, textLen):
        DBWorker.logUser(user.id, user.username, user.first_name, user.last_name)
        artist = AS(text[nameI])
        artData = subsArtData(artist)
        DBWorker.logArtist(artData["name"], artData["lastWork"], artData["lastThumb"], artData["lastDate"])
        bot.send_message(chatID, "Subscribtion on " + text[nameI] + " done Successful\nSubscribes left:")
    else:
        bot.send_message(chatID, "command should be like /subs <b>username</b>", parse_mode="HTML")


def subsArtData(artist):
    if artist.ifArtist:
        lastArt = getLastArt(artist)
        return {"name": artist.name, "lastWork": lastArt["projUrl"], "lastThumb": lastArt["thumbUrl"],
                "lastDate": lastArt["postDate"]}
    else:
        answer = "There are no any <b>" + artist.name + "</b> artist on Artstation!"


'''
PALETTE  METHODS STARTS HERE
'''


def colormindPalette(model):
    # returns array of "colormind" random palette
    url = "http://colormind.io/api/"
    raw_data = '{"model":"' + model + '"}'
    response = requests.get(url, data=raw_data)
    return json.loads(response.text)["result"]


def hexPalette(arr):
    # gets RGB colors[ARRAY[STRING]]. returns array of HEX colors
    palette = []
    for color in arr:
        palette.append(''.join([hex(part)[2:] for part in color]))
    return palette


def sciPic(hcode):
    # gets hexcode of color[STRING]. returns url[STRING] of "singlecolorimage" service
    url = "https://singlecolorimage.com/get/" + hcode + "/100x100"
    return url


def getPalette(bot, chatID, palette):
    # sends message with palette
    imgs = [types.InputMediaPhoto(sciPic(color), color) for color in palette]
    bot.send_media_group(chatID, imgs)
