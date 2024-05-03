import os

import telebot
from dotenv import load_dotenv

import initializers.database
import repo.peer
import service.peer
import sheet.sheet as sheet

API_KEY = os.getenv("API_KEY")
bot = telebot.TeleBot(API_KEY)

initializers.database.init()
load_dotenv()


def all_request(message):
    return message.text == "All"


@bot.message_handler(func=all_request)
def send_all(message):
    try:
        s = ""
        i = 0
        peers = service.peer.get_all_peers()
        for peer in peers:
            s += peer.show_string() + "\n----------------\n"
            i += 1
            if i % 20 == 0:
                bot.send_message(message.chat.id, s)
                s = ""
        if s != "":
            bot.send_message(message.chat.id, s)
    except Exception as err:
        bot.send_message(message.chat.id, type(err).__name__ + " " + str(err))


def reload_request(message):
    return message.text == "Reload"


@bot.message_handler(func=reload_request)
def send_max(message):
    try:

        sheet.main()
        bot.send_message(message.chat.id, "Reloaded!")
    except Exception as err:
        bot.send_message(message.chat.id, type(err).__name__ + " " + str(err))


def pause_request(message):
    if "Pause" in message.text:
        data = message.text.split(" ")
        if data[0] == "Pause" and repo.peer.is_name_exists(data[1]) and len(data) == 2:
            return True
    return False


@bot.message_handler(func=pause_request)
def send_pause(message):
    try:
        name = message.text.split(" ")[1]
        service.peer.pause_peer(name)
        sheet.main()
        bot.send_message(message.chat.id, "Paused!")
    except Exception as err:
        bot.send_message(message.chat.id, type(err).__name__ + " " + str(err))


def resume_request(message):
    if "Resume" in message.text:
        data = message.text.split(" ")
        if data[0] == "Resume" and repo.peer.is_name_exists(data[1]) and len(data) == 2:
            return True
    return False


@bot.message_handler(func=resume_request)
def send_resume(message):
    try:
        name = message.text.split(" ")[1]
        service.peer.resume_peer(name)
        sheet.main()
        bot.send_message(message.chat.id, "Resumed!")
    except Exception as err:
        bot.send_message(message.chat.id, type(err).__name__ + " " + str(err))


def reset_user(message):
    if "Reset" in message.text:
        data = message.text.split(" ")
        if data[0] == "Reset" and repo.peer.is_name_exists(data[1]) and len(data) == 2:
            return True
    return False


@bot.message_handler(func=reset_user)
def send_reset(message):
    try:
        name = message.text.split(" ")[1]
        service.peer.reset_peer(name)
        sheet.main()
        bot.send_message(message.chat.id, "Usage has been reset!")
    except Exception as err:
        bot.send_message(message.chat.id, type(err).__name__ + " " + str(err))


def user_request(message):
    return repo.peer.is_name_exists(message.text)


@bot.message_handler(func=user_request)
def send_user(message):
    cid = message.chat.id
    message_text = message.text
    try:
        peer = service.peer.get_peer(message_text)
        bot.send_message(cid, peer.show_string())
    except Exception as err:
        bot.send_message(message.chat.id, type(err).__name__ + " " + str(err))


sheet.main()
bot.polling()
