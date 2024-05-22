import telebot
import config

from database import Database


bot = telebot.TeleBot(config.bot_token)
db = Database('data.db')


@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    pass


print("Bot Enabled")
bot.infinity_polling()