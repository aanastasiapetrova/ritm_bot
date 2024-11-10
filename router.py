from aiogram import Router, html

from aiogram.filters import CommandStart
from aiogram.types import Message

basic_router = Router()

@basic_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Здравствуйте, {html.bold(message.from_user.full_name)}! '
                         f'Здесь вы можете получить подписку на закрытый клуб!')


@basic_router.message()
async def default_handler(message: Message) -> None:
    await message.answer('Мне не известна комманда, которую вы ввели. '
                         'Пожалуйста, попробуйте ещё раз!')