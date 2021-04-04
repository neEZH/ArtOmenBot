import telebot
import os
from artstation import AS


def logMsg(msg):
    log = "ChatID:" + str(msg.chat.id) + "\n"
    log += "MessageID:" + str(msg.message_id) + "\n"
    log += "From:" + str(msg.from_user.id) + " ["+str(msg.from_user.username) + "]" + "\n"
    log += "Text:" + str(msg.text.split(" ")) + "\n"
    print(log)
    return msg.text.split(" ")


bot = telebot.TeleBot(os.environ['botToken'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Hello there")


@bot.message_handler(commands=['last'])
def showLastWork(message):
    chatID = message.chat.id
    print("/last TRIGGERED")
    text = logMsg(message)
    if len(message.text.split(" ")) == 2:
        artist = AS(text[1])
        if artist.ifArtist:
            if artist.ifProjs:
                lastProjs = artist.lastArt
                projUrl = lastProjs['permalink']
                thumbUrl = lastProjs['cover']['small_square_url']
                print("thumbUrl: " + thumbUrl)
                bot.send_photo(chatID, str(thumbUrl), str(projUrl))
            else:
                bot.send_message(chatID, "There are no any project for this artist")
        else:
            answer = "There are no any <b>" + artist.name + "</b> artist on Artstation!\nMay be it is someone like:"
            for candidate in AS.findArtist(artist.name):
                answer += "\n" + candidate["username"]
            print("before sending")
            print(answer)
            bot.send_message(chatID, answer, parse_mode="HTML")
    else:
        bot.send_message(chatID, "command should be like /last <b>username</b>", parse_mode="HTML")


# @bot.message_handler(commands=['get'])
# def getMessageInfo(message):
#     chatID = message.chat.id
#
#     try:
#          artistName = message.text.split(" ")[1]
#          url = "https://www.artstation.com/users/" + artistName + "/projects.json"
#
#          rsp = json.loads(requests.get(url).text)
#
#          lastPubl = ""
#          lastId = 0
#          artId = 0
#          for artWork in rsp['data']:
#              if lastPubl < artWork['published_at']:
#                  lastPubl = artWork['published_at']
#                  lastId = artId
#              artId += 1
#          artUrl = rsp['data'][lastId]['permalink']
#          thumbUrl = rsp['data'][lastId]['cover']['thumb_url']
#
#          bot.send_photo(chatID, thumbUrl, artUrl)
#     except IndexError as exp:
#          bot.send_message(chatID, 'Добавь Ник художника: "/get ArtistName"')
#     except Exception as exp:
#          bot.send_message(chatID, "Error: " + str(exp))


print("Bot starting!!")
bot.polling(none_stop=True)
