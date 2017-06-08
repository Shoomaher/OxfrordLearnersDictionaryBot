import urllib.request
import config
from bs4 import BeautifulSoup

def get_url(word):
	word = word.lower()
	URL = config.url + word + '_1?q=' + word
	return URL

def get_html(url):
	response = urllib.request.urlopen(url)
	return response.read()

def parse(html):
	soup = BeautifulSoup(html, "html.parser")
	list = soup.find('div', class_='entry')
	for span in soup.findAll('span', 'idm-g'):
		span.extract()
	definitions = list.find_all('span', class_= 'def')
	defs = []
	for defin in definitions:
		defs.append(defin.text)
	return defs
def search(WORD):
	return parse(get_html(get_url(WORD)))
