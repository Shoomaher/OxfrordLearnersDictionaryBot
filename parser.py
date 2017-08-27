import urllib
import config
from bs4 import BeautifulSoup

code=0
PREV_WORD = ''
wrong = ''
idioms = []
successful_urls=0

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
	global code
	global successful_urls
	htmls = []
	for url in urls:
		try:
			response = urllib.request.urlopen(url)
			respRead = response.read()
			htmls.append(respRead)
			successful_urls+=1
			
		except urllib.error.HTTPError as err:
			code = err.code
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
			
def parse(htmls):
	global code
	global successful_urls
	if successful_urls !=0:
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
		successful_urls = 0
		return make_lists(many_defs)
	else:
		code = 0
		return wrong
		
def parse_idioms(htmls):
	global code
	global successful_urls
	idioms_list = []
	if successful_urls !=0:
		for html in htmls:
			idioms_soup = BeautifulSoup(html, "html.parser")
			
			for span in idioms_soup.find_all('a', id='add-to-mywordlist-link'):
				span.extract()
			for span in idioms_soup.find_all('a', class_='responsive_display_inline_on_smartphone link-right'):
				span.extract()			
			for span in idioms_soup.find_all('span', class_='x'):
				span.extract()
			for idm in idioms_soup.find_all('span', 'idm-g'):
					idioms_list.append(idm.text)
		if not idioms_list:
			return wrong
		else:
			successful_urls = 0
			return print_idioms(idioms_list)
	else:
		code = 0
		return wrong

def search_idioms(word,str_wrong):
	global wrong
	wrong = str_wrong
	if ((word == '' or word == ' ') and (PREV_WORD != '' or PREV_WORD != ' ')):
		return parse_idioms(get_htmls(get_urls(PREV_WORD)))
	elif ((word == '' or word == ' ') and (PREV_WORD == '' or PREV_WORD == ' ')):
		return wrong
	else:
		return parse_idioms(get_htmls(get_urls(word)))	
	
def search(word, str_wrong):
	global PREV_WORD
	global wrong
	wrong = str_wrong
	result = parse(get_htmls(get_urls(word)))
	PREV_WORD = word
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
