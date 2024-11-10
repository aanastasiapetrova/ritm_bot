from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def subscribe() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Подписаться')]],
        resize_keyboard=True
    )