import os

import telebot

from flask import Flask, request

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DEBUG = bool(int(os.environ.get('DEBUG', 0)))
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Отправь мне видео, всё остальное я расскажу потом")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://video-compressor-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    if DEBUG == True:
        bot.remove_webhook()
        bot.polling()
    else:
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))