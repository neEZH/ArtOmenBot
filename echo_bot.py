import telebot
import requests
import json
import os
from artstation import AS

bot = telebot.TeleBot(os.environ['botToken'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Hello there")


@bot.message_handler(commands=['get'])
def getMessageInfo(message):
    print("Message get")
    chatID = message.chat.id

    print("Chat ID: " + str(message.chat.id))

    print("message ID: " + str(message.message_id))

    print("from: " + str(message.from_user.username))

    print("text: " + str(message.text.split(" ")))
    try:
        artistName = message.text.split(" ")[1]
        url = "https://www.artstation.com/users/" + artistName + "/projects.json"

        rsp = json.loads(requests.get(url).text)

        lastPubl = ""
        lastId = 0
        artId = 0
        for artWork in rsp['data']:
            if lastPubl < artWork['published_at']:
                lastPubl = artWork['published_at']
                lastId = artId
            artId += 1
        artUrl = rsp['data'][lastId]['permalink']
        thumbUrl = rsp['data'][lastId]['cover']['thumb_url']

        bot.send_photo(chatID, thumbUrl, artUrl)
    except IndexError as exp:
        bot.send_message(chatID, 'Добавь Ник художника: "/get ArtistName"')
    except Exception as exp:
        bot.send_message(chatID, "Error: " + str(exp))


print("Bot starting!!")
bot.polling(none_stop=True)
