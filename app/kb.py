from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def subscribe() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Подписаться',
                                               callback_data='subscribe')]],
        resize_keyboard=True
    )