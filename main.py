from bs4 import BeautifulSoup as bs
import requests
import telebot
import os

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


@bot.message_handler(commands=["admin"])
def admin_commands(message):
    if message.from_user.username  == str(os.environ['OWNER_TELEGRAM_ID']):
        text = f"Commands for admin are as follows:\n1. /res\n2. /mainres\nMainres can only be 25,50,100"
        bot.reply_to(message  , text)

@bot.message_handler(commands=["mainres"])
def mainres_get(message):
    global mainres
    if message.from_user.username  == str(os.environ['OWNER_TELEGRAM_ID']):
        try:
            a = str(message.text)
            mainres = a[9:]
            mainres = int(mainres)
            text = "Main results lenght changed to "+ str(mainres)
            bot.reply_to(message , text)
        except:
            bot.reply_to(message , "Something Went wrong !")
            mainres = 25


@bot.message_handler(commands=["res"])
def res_res(message):
    global results
    if message.from_user.username  == str(os.environ['OWNER_TELEGRAM_ID']):
        try:
            results = message.text
            results = results[5:]
            results = int(results)
            text = "Results lenght changed to "+str(results)
            bot.reply_to(message , text)
        except:
            bot.reply_to(message , "Something Went wrong !")
            results = 5


@bot.message_handler(commands = ["book"])
def books_get(message):
    BOOKS = []
    done = "yes"
    try:
        given_name = message.text[6:]
    except:
        bot.reply_to(message , "Unable to process your request.")
        return
    bot.reply_to(message , "Getting your book please be patient")
    id = message.from_user.id
    try:
        url_1 = "http://libgen.is/search.php?req="
        url_2 = "&lg_topic=libgen&open=0&view=simple&res="
        url_3 = "&phrase=1&column=def"
        given_name = given_name.replace(" " , "+")
        url = url_1 + given_name + url_2 + str(mainres) + url_3
        response = requests.get(url)
        bs_html = bs(response.text , "html.parser")
    except:
        done = "no"
    if done == "no":
        bot.reply_to(message , "Unable to process your request.")
        return
    else:
        try:
            table = bs_html.find_all("table")
            table = table[2]
            table_rows = table.find_all("tr")
            a = len(table_rows)
            if a < 1 or a == 1 :
                bot.reply_to(message , "Unable to process your request.")
                return
            else:
                for i in range (-1 , -a , -1 ):
                    link_list = []
                    link_line = table_rows[i]
                    tds = link_line.find_all("td")
                    book_name = tds[2].get_text()
                    author = tds[1].get_text()
                    link_row = tds[9]
                    a = link_row.find("a" , href = True)
                    link = a.get("href")
                    b = tds[7]
                    c = tds[8]
                    size = b.get_text()
                    type_ofit = c.get_text()
                    link_list.append(book_name)
                    link_list.append(author)
                    link_list.append(size)
                    link_list.append(type_ofit)
                    link_list.append(link)
                    BOOKS.append(link_list)

            images = []
            linkss = []
            book_links = []
            for i in range(len(BOOKS)):
                a = BOOKS[i]
                linkss.append(a[4])
            if len(linkss) > results:
                for i in range(results):
                    response = requests.get(linkss[i])
                    th_html = bs(response.text , "html.parser")
                    b = th_html.find_all("td" ,id ="info")
                    b = b[0]
                    aa = b.find("a")
                    link = aa.get("href")
                    div = b.find("div")
                    img_link = b.find("img" ,alt="cover")
                    img_link = img_link.get("src")
                    m = "http://library.lol/"
                    img_link = m + img_link
                    images.append(img_link)
                    book_links.append(link)
            else:
                for i in range(len(linkss)):
                    response = requests.get(linkss[i])
                    th_html = bs(response.text , "html.parser")
                    b = th_html.find_all("td",id ="info")
                    b = b[0]
                    aa = b.find("a")
                    link = aa.get("href")
                    div = b.find("div")
                    img_link = b.find("img" ,alt="cover")
                    img_link = img_link.get("src")
                    m = "http://library.lol/"
                    img_link = m + img_link
                    images.append(img_link)
                    book_links.append(link)

            for i in range(len(book_links)):
                b = BOOKS[i]
                name = b[0]
                author = b[1]
                size = b[2]
                formata = b[3] 
                dn = f"[DOWNLOAD NOW]({book_links[i]})"
                caption_all = f"*Name* : {name}\n*Author* : {author}\n*Size* : {size}\n*Format* : {formata}\n{dn}"
                bot.send_photo(id ,images[i] , caption = caption_all ,parse_mode ="Markdown" )

        except:
            bot.reply_to(message , "Unable to process your request.`")






while True:
    print("Started.....")     
    bot.polling()


# ////////////////
