import os
import uuid

import telebot
from telebot import TeleBot, types
from flask import Flask, request

from video_convertor import convert_video, ConversionType

all_content_types_except_video = ['text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message', 'invoice', 'successful_payment', 'connected_website', 'poll', 'passport_data', 'proximity_alert_triggered', 'voice_chat_scheduled', 'voice_chat_started', 'voice_chat_ended', 'voice_chat_participants_invited', 'message_auto_delete_timer_changed']
videos = {}
COMPRESS_VIDEO = 'compress'
CREATE_VIDEO_NOTE = 'create_note'
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
DEBUG = bool(int(os.environ.get('DEBUG', 0)))
bot = TeleBot(TOKEN)
bot.SESSION_TIME_TO_LIVE = 5 * 60
server = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Отправь мне видео, всё остальное я расскажу потом")

@bot.message_handler(content_types=['video'])
def process_video(message):
    video_id = str(message.video.file_id)
    short_id = str(uuid.uuid4())
    videos[short_id] = video_id

    markup = types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton('сжать видео', callback_data=f"{ConversionType.SMALL_SIZE.value}:{short_id}")
    itembtn2 = types.InlineKeyboardButton('прислать video note', callback_data=f"{ConversionType.NOTE_SIZE.value}:{short_id}")
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Получил видео, что с ним сделать?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def command_callback(call):
    command, file_id = call.data.split(':')
    bot.send_message(call.from_user.id, "Разбираюсь")
    bot.delete_message(call.from_user.id, call.message.message_id)
    chat_action, send_method = ('record_video_note', bot.send_video_note) if command == ConversionType.NOTE_SIZE.value else ('upload_video', bot.send_video)
    create_video(videos[file_id], call.from_user, command, chat_action, send_method)
    try:
        os.remove(f'videos/{videos[file_id]}.mp4')
        os.remove(f'videos/converted/{videos[file_id]}.mp4')
    except PermissionError as e:
        print(e)

def save_file_by_id(file_id):
    file_url = bot.get_file_url(file_id)
    file_data = bot.download_file('videos/' + file_url.split('/')[-1])

    video_file = open(f"videos/{file_id}.mp4", "ab")
    video_file.write(file_data)
    video_file.close()

    del file_data

def create_video(file_id, user, conversion_type, chat_action, send_method):
    save_file_by_id(file_id)
    convert_video(file_id, conversion_type)
    bot.send_chat_action(user.id, chat_action, timeout=5)
    try:
        with open(f'videos/converted/{file_id}.mp4', "rb") as file_object:
            data = file_object.read()
            send_method(user.id, data)
            del data
    except EnvironmentError as e:
        print(e)

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