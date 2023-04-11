from unittest import result
from bs4 import BeautifulSoup as bs
import requests
import telebot
import os
import time
from book import book_get

# BOT HEADERS............

bot = telebot.TeleBot(os.environ['YOUR_BOT_TOKEN'])
results = 5
mainres = 25

# ////////////////
# BOT COMMANDS............\\\

@bot.message_handler(commands=["start"])
def starting(message):
    text = f"I am a simple book bot.\nI will help you to download books of your own choice\nOur syntax is easy just send\n/book<space><book name>\nWithout without bracket sign.\nEXAMPLE : /book abc\n\nSend /help to get help"
    bot.reply_to(message , text)


@bot.message_handler(commands=["help"])
def help(message):
    text = f"Commands:\n1.  /book <book_name>"
    bot.reply_to(message , text)


# @bot.message_handler(commands=["admin"])
# def admin_commands(message):
#     if message.from_user.username  == str(os.environ['OWNER_TELEGRAM_ID']):
#         text = f"Commands for admin are as follows:\n1. /res\n2. /mainres\nMainres can only be 25,50,100"
#         bot.reply_to(message  , text)

# @bot.message_handler(commands=["mainres"])
# def mainres_get(message):
#     global mainres
#     if message.from_user.username  == str(os.environ['OWNER_TELEGRAM_ID']):
#         try:
#             a = str(message.text)
#             mainres = a[9:]
#             mainres = int(mainres)
#             text = "Main results lenght changed to "+ str(mainres)
#             bot.reply_to(message , text)
#         except:
#             bot.reply_to(message , "Something Went wrong !")
#             mainres = 25


# @bot.message_handler(commands=["res"])
# def res_res(message):
#     global results
#     if message.from_user.username  == str(os.environ['OWNER_TELEGRAM_ID']):
#         try:
#             results = message.text
#             results = results[5:]
#             results = int(results)
#             text = "Results lenght changed to "+str(results)
#             bot.reply_to(message , text)
#         except:
#             bot.reply_to(message , "Something Went wrong !")
#             results = 5


@bot.message_handler(commands = ["book"])
def books_get(message):
    id = message.from_user.id
    given_name = message.text[6:]
    # response = requests.request("GET", url)
    # data_text = response.text
    # data = json.loads(data_text)
    data = book_get(given_name, mainres, results)
    # print(data)
    if data == "Error: emoji":
        bot.reply_to(message , "Error: emoji\nPlease do not use Emojis😂")
    elif data == "Error: no results found":
        bot.reply_to(message , "Error: no results found\nPlease try for another book.")
    elif data == "Error: enter name":
        bot.reply_to(message , "Error: enter name\nPlease provide the name of book you are looking for")
    elif data == "Error: Title Too Short":
        bot.reply_to(message , "Error: Title Too Short\nPlease provide full title for better results")
    else:
        counter = 0
        for i in data:
            if counter <= results:
                dn = f"[DOWNLOAD NOW]({i[5]})"
                caption_all = f"*Name* : {i[0]}\n*Author* : {i[1]}\n*Size* : {i[3]}\n*Format* : {i[4]}\n{dn}"
                bot.send_photo(id ,i[6] , caption = caption_all ,parse_mode ="Markdown" )
                counter+=1


while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue


# ////////////////
