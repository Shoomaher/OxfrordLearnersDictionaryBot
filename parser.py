import urllib
import config
from bs4 import BeautifulSoup
code=0

def get_url(word):
	word = word.lower()
	if word.find('-') != -1:
		word = word.replace(' ', '-')
		URL = config.url + word + '_1?q=' + word
	else:
		word = word.replace(' ', '-')
		URL = config.url + word + '_2?q=' + word
	return URL
	
def get_url_magic(url):
	if url.find('_1') != -1:
		url = url.replace('_1', '')
	else:
		url = url.replace('_2', '')
	return url

def get_html(url):
	global code
	try:
		response = urllib.request.urlopen(url)
		respRead = response.read()
	except urllib.error.HTTPError as err:
		try: 
			response = urllib.request.urlopen(get_url_magic(url))
			respRead = response.read()
		except urllib.error.HTTPError as err:
			print(err.code)
			code = err.code
			return 0
	return respRead

def parse(html):
	global code
	if code == 0:
		soup = BeautifulSoup(html, "html.parser")
		list = soup.find('div', class_='entry')
		for span in soup.findAll('span', 'idm-g'):
			span.extract()
		definitions = list.find_all('span', class_= 'def')
		defs = []
		for defin in definitions:
			defs.append(defin.text)
		definition = ' '
		i=1
		for d in defs:
			d = d.strip()
			d = d[0].upper() + d[1:]
			definition+= str(i) + '. ' + d +'\n'
			i+=1 
		return definition
	else:
		code=0
		return 'Что-то пошло не так!'
def search(WORD):
	return parse(get_html(get_url(WORD)))
