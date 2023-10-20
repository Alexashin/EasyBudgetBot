# Обработчики событий
from aiogram.fsm.context import FSMContext
from aiogram import types, F
from misc import dp
from aiogram.types import Message
from aiogram.filters import Command

from resources import states


# Обработка команды /start
@dp.message(Command("start"))
async def processing_start_command(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        "Стартовое сообщение"
    )  # TODO: Создание стартовой таблицы, приветственное сообщение с инструкцией


# Обработка фотографий без состояния
@dp.message(F.photo)
async def processing_photo(msg: Message) -> None:
    await msg.answer("Я принял фотографию")
