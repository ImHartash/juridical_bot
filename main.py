import telebot
import config

from database import *


bot = telebot.TeleBot(config.bot_token)
db_messages = MessagesDatabase('MessagesDatabase.db')
db_users = UsersDatabase('UsersDatabase.db')


@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message):
    db_users.set_user_theme(message.from_user.id, 'ahahahhhaha')
    bot.send_message(message.from_user.id, db_users.get_user_theme(message.from_user.id))


print("Bot Enabled")
bot.infinity_polling()