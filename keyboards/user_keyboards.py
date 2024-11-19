from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import logging


def keyboard_main() -> ReplyKeyboardMarkup:
    logging.info("keyboard_main_admin")
    button_1 = KeyboardButton(text='🔎 Поиск по артикулу')

    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1]], resize_keyboard=True)
    return keyboard
