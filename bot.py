### ------ Libraries ------ ###
import telebot
from telebot import types
import urllib
import csv
from datetime import datetime
from botanio import botan
### ------ Other files ------ ###
import config
import newparser
import translate
import strings

bot = telebot.TeleBot(config.token)

languages_db = {}
requests = []


def create_request(chat_id):
	for req in requests:
		if req[0] == chat_id:
			requests.remove(req)
	req = [chat_id, ' ', ' ', True]
	requests.append(req)
	
def add_text(chat_id, text):
	for req in requests:
		if req[0] == chat_id:
			req[1] = text
	
def add_lang(chat_id, lang):
	for req in requests:
		if req[0] == chat_id:
			req[2] = lang
			return req
	return strings.get_string(languages_db[str(message.chat.id)], 'wrong')
	
def turn_working(chat_id):
	for req in requests:
		if req[0] == chat_id:
			req[3] = not req[3]
	
def isWorking(chat_id):
	for req in requests:
		if req[0] == chat_id:
			return req[3]

########################################################################
###			 S E T T I N G S    S T O R A G E	     ###
def read_db():
	with open('languages_db.csv', "r") as db_file:
		db_reader = csv.reader(db_file)
		for row in db_reader:
			row = str(row)
			row = row.replace('[','').replace(']','').replace('"','').replace('\'','')
			index = row.find(':')
			languages_db[row[:index]] = row[index+1:]
# Using CSV is quite strange idea, but it works !!!		
def save_db():
	with open('languages_db.csv', "w") as db_file:
		db_writer = csv.writer(db_file, delimiter=':')
		for chat_id in languages_db.keys():
			db_writer.writerow([chat_id,languages_db[chat_id]])
###                                                                  ###
########################################################################

@bot.message_handler(commands=['start', 'settings'])
def handle_start(message, restart=False):
	keyboard = types.InlineKeyboardMarkup()
	ru_button = types.InlineKeyboardButton(text="Русский 🇷🇺", callback_data="ru")
	keyboard.add(ru_button)
	uk_button = types.InlineKeyboardButton(text="Українська 🇺🇦", callback_data="uk")
	keyboard.add(uk_button)
	en_button = types.InlineKeyboardButton(text="English 🇬🇧", callback_data="en")
	keyboard.add(en_button)
	#de_button = types.InlineKeyboardButton(text="Deutsch 🇩🇪", callback_data="de")
	#keyboard.add(de_button)
	if restart:
		bot.send_message(message.chat.id, 'Select your language and send your previous message again, please', reply_markup=keyboard)
	elif message.text == '/start':
		bot.send_message(message.chat.id, 'Hi! Select your language:', reply_markup=keyboard)
	elif message.text == '/settings':
		bot.send_message(message.chat.id, 'Select your language:', reply_markup=keyboard)
	
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
	if call.data == "entry":
		array = newparser.get_word_of_the_day()
		bot.send_message(call.message.chat.id, newparser.search(array[0],strings.get_string(languages_db[str(call.message.chat.id)], 'wrong')), parse_mode='Markdown')
	else:
		chat_id = call.message.chat.id
		languages_db[str(chat_id)] = call.data
		bot.send_message(chat_id, strings.get_string(languages_db[str(call.message.chat.id)], 'saved'))
	
@bot.message_handler(commands=['help'])
def handle_help(message):
	if str(message.chat.id) in languages_db.keys():
		bot.send_message(message.chat.id, strings.get_string(languages_db[str(message.chat.id)], 'help'))
	else:
		handle_start(message, True)
		
@bot.message_handler(commands=['idioms'])
def handle_idioms(message):
	if str(message.chat.id) in languages_db.keys():
		text = message.text			
		text = text[7:]
		botan.track(config.botan_key, message.chat.id, message.text, 'Идиомы')
		bot.send_message(message.chat.id, newparser.search_idioms(text, strings.get_string(languages_db[str(message.chat.id)],'wrong'), message.chat.id), parse_mode='Markdown')
	else:
		handle_start(message, True)

@bot.message_handler(commands=['translate'])
def handle_translate(message):
	if str(message.chat.id) in languages_db.keys():
		msg1 = bot.reply_to(message, strings.get_string(languages_db[str(message.chat.id)],'translate'), parse_mode='Markdown')
		create_request(message.chat.id)
		bot.register_next_step_handler(msg1, process_word_step)
	else:
		handle_start(message, True)
	
def process_word_step(message):
	text = message.text.strip()
	add_text(message.chat.id, text)
	bot.reply_to(message, translate.translate(add_lang(message.chat.id, languages_db[str(message.chat.id)])), parse_mode='Markdown')
	turn_working(message.chat.id)
	
@bot.message_handler(commands=['ilikethisbot'])
def handle_ilikethisbot(message):
	if str(message.chat.id) in languages_db.keys():
		bot.send_message(message.chat.id, strings.get_string(languages_db[str(message.chat.id)], 'rate'), parse_mode='Markdown')
	else:
		handle_start(message, True)

@bot.message_handler(commands=['wordoftheday'])
def handle_wordoftheday(message):
	if str(message.chat.id) in languages_db.keys():
		keyboard = types.InlineKeyboardMarkup()
		callback_button = types.InlineKeyboardButton(strings.get_string(languages_db[str(message.chat.id)], 'entry'), callback_data="entry")
		keyboard.add(callback_button)
		bot.send_message(message.chat.id, newparser.print_word_of_the_day(newparser.get_word_of_the_day()), parse_mode='Markdown', reply_markup=keyboard)
		# Callback is above
	else:
		handle_start(message, True)
	
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	if str(message.chat.id) in languages_db.keys():
		if isWorking(message.chat.id):
			pass
		else:
			botan.track(config.botan_key, message.chat.id, message.text, 'Запрос')
			bot.send_message(message.chat.id, newparser.search(message.text, strings.get_string(languages_db[str(message.chat.id)], 'wrong'), message.chat.id), parse_mode='Markdown')
	else:
		handle_start(message, True)

@bot.edited_message_handler(func=lambda message: True)
def edit_message(message):
	if '/translate' in message.text:
		bot.edit_message_text(chat_id = message.chat.id, text = translate.translate(message.text[10:]), message_id = message.message_id + 1, parse_mode='Markdown')
	elif '/idioms' in message.text:
		bot.edit_message_text(chat_id = message.chat.id, text = newparser.search_idioms(message.text[7:], strings.get_string(languages_db[str(message.chat.id)], 'wrong')), message_id = message.message_id + 1, parse_mode='Markdown')
	elif '/ilikethisbot' in message.text:
		bot.edit_message_text(chat_id = message.chat.id, text = strings.get_string(languages_db[str(message.chat.id)], 'rate'), message_id = message.message_id +1, parse_mode='Markdown')
	elif '/wordoftheday' in message.text:
		handle_wordoftheday(message)
	elif '/' in message.text:
		bot.edit_message_text(chat_id = message.chat.id, text = strings.get_string(languages_db[str(message.chat.id)], 'wrong'), message_id = message.message_id + 1, parse_mode='Markdown')
	else:
		bot.edit_message_text(chat_id=message.chat.id, text = newparser.search(message.text), message_id = message.message_id + 1, parse_mode='Markdown')
	
if __name__ == '__main__':
	read_db()
	bot.polling(none_stop=True)
