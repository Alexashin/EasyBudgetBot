# Обработчики событий

from aiogram import types, F
from misc import dp
from aiogram.types import Message
from aiogram.filters import Command


@dp.message(Command('start')) # Обработчик команды старт
async def processing_start_command(msg: Message):
    await msg.answer('') # TODO: Создание стартовой таблицы, приветственное сообщение с интсрукцией