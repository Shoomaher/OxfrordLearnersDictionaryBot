import requests
import config
import strings
apiKey = config.yandex_translate_key
	
def translate(req):
	text = req[1]
	lang = req[2]
	setup = {'key' : apiKey, 'text' : text, 'lang' : lang, 'format' : 'plain', 'callback' : 'call'}
	r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params = setup)
	codePos = r.text.index('"code') + 7
	code = r.text[codePos : codePos + 3]
	code = int(code)
	if code == 200:
		posText = (r.text).index('"text"') + 9
		result = '{}\n\n{}'.format(r.text[posText : -4], strings.get_string(lang,'yandex'))
		return result
	else:
		return '{} {} 😨'.format(strings.get_string(lang,'error'),code)
	
