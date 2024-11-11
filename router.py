from aiogram import Router, F, html, Bot

from aiogram.filters import CommandStart
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType

from app import kb
from config import PAYMENT_TOKEN

basic_router = Router()
PRICE = LabeledPrice(label='Sub month', amount=100 * 100) # копейки


@basic_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f'Здравствуйте, {html.bold(message.from_user.full_name)}! '
                         f'Здесь вы можете получить подписку на закрытый клуб!', reply_markup=kb.subscribe())


@basic_router.message(F.text.lower() == 'подписаться')
async def subscribe_handler(message: Message, bot: Bot) -> None:
    if PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await message.answer('Это тестовая отправка!')
    
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Подписка на закрытый клуб',
        description='Активация подпсики на канал на 1 месяц',
        payload='test_payload',
        currency='rub',
        prices=[PRICE],
        message_thread_id=None,
        provider_token=PAYMENT_TOKEN,
        start_parameter='one-month-subscription',
        is_flexible=False
    )


@basic_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot) -> None:
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@basic_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, bot: Bot):
    await message.answer('Успешный платеж!')


@basic_router.message()
async def default_handler(message: Message) -> None:
    await message.answer('Мне не известна комманда, которую вы ввели. '
                         'Пожалуйста, попробуйте ещё раз!')