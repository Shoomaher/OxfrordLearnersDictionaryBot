import config
import telebot
import urllib
import newparser

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	bot.send_message(message.chat.id, 'Hi! Send me the word and I\'ll find the definition')

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	bot.send_message(message.chat.id, newparser.search(message.text))

if __name__ == '__main__':
	bot.polling(none_stop=True)
