ru_strings = {
'wrong' : 'Что-то пошло не так 🙁',
'help' : 'Пришли мне слово и я найду для него определения.',
'yandex' : '>>> Переведено сервисом [Яндекс.Переводчик](http://translate.yandex.com/)',
'entry' : 'Полная статья 📚',
'translate' : 'Что мне перевести?',
'rate' : 'Если тебе понравился бот и ты желаешь подержать разработчика, пожалуйста, поставьте оценку [тут](https://storebot.me/bot/oxf_dict_bot) ⭐️⭐️⭐️⭐️⭐️',
'lang' : 'На каком языке перевести?',
'saved': 'Сохранено!',
'error' : 'Ошибка'
}
en_strings = {
'wrong' : 'Something has gone wrong 🙁',
'help' : "Send me the word and I'll find the definition",
'yandex' : '>>> Translated using [Yandex.Translator](http://translate.yandex.com/)',
'entry' : 'See entry 📚',
'translate' : 'What I need to translate?',
'rate' : 'If you like this bot and you want to support the developer, please rate it [there](https://storebot.me/bot/oxf_dict_bot) ⭐️⭐️⭐️⭐️⭐️',
'lang' : 'What language I need to translate on?',
'saved' : 'Saved!',
'error': 'Error'
}
uk_strings = {
'wrong' : 'Щось пішло не так 🙁',
'help' : "Відправ мені слово, і я надішлю тобі його визначення",
'yandex' : '>>> Перекладено використовуючи [Яндекс.Перекладач](http://translate.yandex.com/)',
'entry' : 'Повна стаття 📚',
'translate' : 'Що мені перекласти?',
'rate' : 'Якщо тобі сподобався бот і ти бажаєш підтримати розробника, будь ласка, оціни його [тут](https://storebot.me/bot/oxf_dict_bot) ⭐️⭐️⭐️⭐️⭐️',
'lang' : 'Якою мовою мені перекласти?',
'saved' : 'Збережено!',
'error' : 'Помилка'
}

def get_string(lang, string):
	if lang == 'ru':
		return ru_strings[string]
	elif lang == 'en':
		return en_strings[string]
	elif lang == 'uk':
		return uk_strings[string]
	else:
		return en_strings[wrong]
