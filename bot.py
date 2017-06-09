import config
import telebot
import urllib
import parser
bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	bot.send_message(message.chat.id, 'Привет! Пришли мне слово и я найду его тебе в словаре')

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	bot.send_message(message.chat.id, parser.search(message.text))

if __name__ == '__main__':
	bot.polling(none_stop=True)
