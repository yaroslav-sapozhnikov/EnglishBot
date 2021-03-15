from DataBase import DataBase
from Bot import bot
from Keyboards import default_keyboard, inline_word_keyboard
import translators as ts
import json

db = DataBase()


@bot.message_handler(content_types=['text'])
def msg_handling(event):

    if event.text == '/start':
        bot.send_message(event.chat.id, 'Привет, выбери режим:', reply_markup=default_keyboard())

    if event.text == '/parse':
        added_count = db.parse_words()
        bot.send_message(event.chat.id, f'Добавлено {added_count} новых слов')

    if event.text == 'Рандом':
        word = db.get_random()
        keyboard = inline_word_keyboard(word)
        bot.send_message(event.chat.id, f'Слово: {word["word"]}\nЗнаете: {word["yes"]}\nНе знаете: {word["no"]}',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def inline_word_handler(call):
    data = json.loads(call.data)

    if data['type'] == "yes":
        db.update_yes(data)
        translated = ts.google(data['word'], to_language='ru')
        bot.send_message(call.message.chat.id, f'Вы знаете слово {data["word"]}.\nПеревод: {translated}\nНажмте "Рандом", чтобы получить еще одно слово')

    elif data['type'] == "no":
        db.update_no(data)
        translated = ts.google(data['word'], to_language='ru')
        bot.send_message(call.message.chat.id, f'Вы не знаете слово {data["word"]}.\nПеревод: {translated}')


bot.polling()
