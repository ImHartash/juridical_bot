import telebot
import config

from database import *


bot = telebot.TeleBot(config.bot_token)
db_messages = MessagesDatabase('Database.db')
db_users = UsersDatabase('Database.db')


@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    bot.send_message(message.from_user.id, '')


print("Bot Enabled")
bot.infinity_polling()