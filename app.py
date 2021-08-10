import os

import telebot

from flask import Flask, request

all_content_types_except_video = ['text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'invoice', 'successful_payment', 'connected_website', 'poll', 'passport_data', 'proximity_alert_triggered', 'voice_chat_scheduled', 'voice_chat_started', 'voice_chat_ended', 'voice_chat_participants_invited', 'message_auto_delete_timer_changed']
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DEBUG = bool(int(os.environ.get('DEBUG', 0)))
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Отправь мне видео, всё остальное я расскажу потом")

@bot.message_handler(content_types=all_content_types_except_video)
def echo_all(message):
    bot.send_message(message.chat.id, "Моя твоя не понимать, лучше скинь видео")

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