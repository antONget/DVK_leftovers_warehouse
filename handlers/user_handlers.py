

from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup

from database import requests as rq
from config_data.config import Config, load_config
from utils.error_handling import error_handler
from keyboards import user_keyboards as kb

from openpyxl import load_workbook
import logging
import requests

config: Config = load_config()
router = Router()
router.message.filter(F.chat.type == "private")


class User(StatesGroup):
    article = State()


@router.message(CommandStart())
@error_handler
async def start(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Запуск бота
    :param message:
    :param state:
    :param bot:
    :return:
    """
    logging.info('start')
    tg_id = message.chat.id
    await state.set_state(state=None)
    user = await rq.get_user(tg_id=tg_id)
    if not user:
        if message.from_user.username:
            username = message.from_user.username
        else:
            username = "useraname"
        data = {"tg_id": tg_id, "username": username}
        await rq.add_user(tg_id=tg_id, data=data)
    await message.answer_photo(photo='AgACAgIAAxkBAAMCZzzHbJTLg_V6cHFsgot9O1CszfQAAqLtMRvVT-hJ2sU--LfaV_gBAAMCAAN4AAM2BA',
                               caption='Добро пожаловать! Вас приветствует виртуальный помощник Ирина.\n'
                                       'Для получения остатка товаров отправьте его артикул из каталога товара'
                                       ' (например, 4991210)')
    await state.set_state(User.article)


@router.message(StateFilter(User.article))
async def get_article(message: Message, state: FSMContext, bot: Bot):
    logging.info('get_article')
    await message.answer(text='Я уже побежала на склад проверять наличие товара по вашему запросу, минутку... ⏳')
    if message.text:
        wb_spb = load_workbook('SPb.xlsx')
        wb_msk = load_workbook('Msk.xlsx')
        sheet_spb = wb_spb.active
        sheet_msk = wb_msk.active
        text = '<b>Количество товара на складах:</b>\n\n'
        flag = 0
        for row_num in range(1, sheet_spb.max_row):
            article = sheet_spb.cell(row=row_num, column=1).value
            if str(article).lower() == message.text.lower():
                leftovers_spb = sheet_spb.cell(row=row_num, column=10).value
                if leftovers_spb == 10:
                    text += f'<b>СПб:</b>\n' \
                            f'артикул - <i>{article}</i>\n' \
                            f'наименование - <i><u>{sheet_spb.cell(row=row_num, column=3).value}</u></i>\n' \
                            f'количество - более 10 шт, РРЦ {sheet_spb.cell(row=row_num, column=9).value} ₽.\n\n'
                else:
                    text += f'<b>СПб:</b>\n' \
                            f'артикул - <i>{article}</i>\n' \
                            f'наименование - <i><u>{sheet_spb.cell(row=row_num, column=3).value}</u></i>\n' \
                            f'количество - {leftovers_spb} шт, РРЦ {sheet_spb.cell(row=row_num, column=9).value} ₽.\n\n'
                flag = 1
                break
        for row_num in range(1, sheet_msk.max_row):
            article = sheet_msk.cell(row=row_num, column=1).value
            if str(article).lower() == message.text.lower():
                leftovers_msk = sheet_msk.cell(row=row_num, column=10).value
                if leftovers_msk == 10:
                    text += f'<b>Мск:</b>\n' \
                            f'артикул - <i>{article}</i>\n' \
                            f'наименование - <i><u>{sheet_msk.cell(row=row_num, column=4).value}</u></i>\n' \
                            f'количество - более 10 шт, РРЦ {sheet_msk.cell(row=row_num, column=9).value} ₽.\n\n'
                else:
                    text += f'<b>Мск:</b>\n' \
                            f'артикул - <i>{article}</i>\n' \
                            f'наименование - <i><u>{sheet_msk.cell(row=row_num, column=4).value}</u></i>\n' \
                            f'количество - {leftovers_msk} шт, РРЦ {sheet_msk.cell(row=row_num, column=9).value} ₽.\n\n'
                flag = 1
                break
        if flag:
            await message.answer(text=text)
        else:
            await message.answer(text=f'Артикул не найден')
    else:
        await message.answer(text='Некорректный номер артикула, повторите ввод')


async def updating_data():
    logging.info('updating_data')
    dls = "https://omoikiri.ru/ostatki/Ostatki_Omoikiri_SPb%20(XLSX).xlsx"
    resp = requests.get(dls)
    output = open('SPb.xlsx', 'wb')
    output.write(resp.content)
    output.close()

    dls = "https://omoikiri.ru/ostatki/Ostatki_Omoikiri_Msk%20(XLSX).xlsx"
    resp = requests.get(dls)
    output = open('Msk.xlsx', 'wb')
    output.write(resp.content)
    output.close()
