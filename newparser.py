import urllib
import config
from bs4 import BeautifulSoup

prev_words = {} #chat_id : prev_word
idioms = []

def get_urls(word):
	word = word.strip()
	word = word.lower().replace(' ', '-')
	urls = []
	i=0
	while (i < 8):
		i+=1
		urls.append(config.url + word + '_' + str(i))
	return urls

def get_htmls(urls):
	htmls = []
	for url in urls:
		try:
			response = urllib.request.urlopen(url)
			respRead = response.read()
			htmls.append(respRead)
			
		except urllib.error.HTTPError as err:
			pass
			break
	return htmls

def find_part_of_speech(title):
	parts_of_speech = config.parts_of_speech
	part = ''
	for p in parts_of_speech:
		if p in title.text:
			return p
	return 'Explanation'
	
def make_lists(array):
	result = ''
	for a in array:
		for d in a:
			result+= d.strip() + '\n'
		result+= '\n'
	return result
	
def print_idioms(array):
	result = ''
	for a in array:
		a = a.replace('\n', '*\n')
		result+= '*' + a + '\n'
	return result
			
def parse(htmls, wrong):
	if len(htmls)!=0:
		many_defs = []
		for html in htmls:
			soup = BeautifulSoup(html, "html.parser")
			list = soup.find('div', class_='entry')
		
			for span in soup.find_all('span', 'idm-g'):
				span.extract()
								
			definitions = list.find_all('span', class_='def')
			defs = []
			title = soup.html.head.title
			defs.append('*' + find_part_of_speech(title).upper() + '*')
			for defin in definitions:
				text = defin.text
				text = text[0].upper() + text[1:]
				defs.append(text)
			many_defs.append(defs)
		return make_lists(many_defs)
	else:
		return wrong
		
def parse_idioms(htmls, wrong):
	idioms_list = []
	if len(htmls) != 0:
		for html in htmls:
			idioms_soup = BeautifulSoup(html, "html.parser")
			
			for span in idioms_soup.find_all('a', id='add-to-mywordlist-link'):
				span.extract()
			for span in idioms_soup.find_all('a', class_='responsive_display_inline_on_smartphone link-right'):
				span.extract()			
			for span in idioms_soup.find_all('span', class_='x'):
				#Убираем примеры. Убрать проще, чем выводить, и
				#Ибо бывает по несколько примеров на идиому. 
				#Хрен знает, как их сопоставить. Хотя... 
				#Если разобраться с id, то модет что-то получиться.
				span.extract()
			for idm in idioms_soup.find_all('span', 'idm-g'):
					idioms_list.append(idm.text)
		if not idioms_list:
			return wrong
		else:
			return print_idioms(idioms_list)
	else:
		return wrong

def search_idioms(word, wrong, chat_id):
	if ((word.strip() == '') and (prev_words[chat_id].strip() != '')):
		return parse_idioms(get_htmls(get_urls(prev_words[chat_id])),wrong)
	elif ((word.strip() == '') and (prev_words[chat_id].strip() == '')):
		return wrong
	else:
		return parse_idioms(get_htmls(get_urls(word)), wrong)	
	
def search(word, wrong, chat_id):
	result = parse(get_htmls(get_urls(word)), wrong)
	prev_words[chat_id] = word 
	return result
	
def get_word_of_the_day():
	response = urllib.request.urlopen('https://www.oxfordlearnersdictionaries.com')
	html = response.read()
	word_of_the_Day_soup = BeautifulSoup(html, "html.parser")
	result = []
	result.append(word_of_the_Day_soup.find('h2', class_='h').text)
	result.append(word_of_the_Day_soup.find('div', class_='d').text)
	return result
		
def print_word_of_the_day(array):
	result = '*{}*\n{}\n'.format(array[0], array[1])
	return result
