import urllib
import config
from bs4 import BeautifulSoup

code=0
PREV_WORD = ''
wrong = 'Something has gone wrong'
idioms = []
successful_urls=0


def get_urls(word):
	global PREV_WORD
	word = word.strip()
	PREV_WORD = word
	word = word.lower().replace(' ', '-')
	print(word)
	urls = []
	i=0
	while (i < 8):
		i+=1
		urls.append(config.url + word + '_' + str(i))
	print(urls)
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
			print(url)
			successful_urls+=1
		except urllib.error.HTTPError as err:
			print(err.code)
			code = err.code
			break
	return htmls

def find_part_of_speech(title):
	parts_of_speech = config.parts_of_speech
	print(parts_of_speech)
	print(title)
	part = ''
	for p in parts_of_speech:
		print(p)
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
			
def parse(htmls):
	global code
	global successful_urls
	print(successful_urls)
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
			defs.append(find_part_of_speech(title).upper())
			for defin in definitions:
				text = defin.text
				text = text[0].upper() + text[1:]
				defs.append(text)
			many_defs.append(defs)
		print(many_defs)
		successful_urls = 0
		return make_lists(many_defs)
	else:
		code = 0
		return wrong
	
def search(word):
	return parse(get_htmls(get_urls(word)))
