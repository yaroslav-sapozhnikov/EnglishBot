from telebot import types
import json

def default_keyboard():

    keyboard = types.ReplyKeyboardMarkup()
    button_random = types.KeyboardButton(text='Рандом')
    keyboard.add(button_random)

    return keyboard


def inline_word_keyboard(word):
    yes_json = json.dumps({"type": "yes", "word": word['word'], "yes": word['yes'], "no": str(word['no'])})
    no_json = json.dumps({"type": "no", "word": word['word'], "yes": word['yes'], "no": str(word['no'])})

    keyboard = types.InlineKeyboardMarkup()

    key_yes = types.InlineKeyboardButton(text='Да', callback_data=yes_json)
    keyboard.add(key_yes)

    key_no = types.InlineKeyboardButton(text='Нет', callback_data=no_json)
    keyboard.add(key_no)

    return keyboard

