import telebot

bot = telebot.TeleBot("9174056572:AAEeBf1rTpbkHo1HnM2DNsTcSphIt9f6_84")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой бот, запущенный на Render!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
