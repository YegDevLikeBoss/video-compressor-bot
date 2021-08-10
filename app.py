import telebot

bot = telebot.TeleBot("1907381812:AAH4Ftxnz1DQlD7JX_KPSoL4MHk-JhBH9zc")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling()