from datetime import datetime, timedelta
from aiogram import Router, F, html, Bot

from aiogram.filters import CommandStart
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType, \
    ReplyKeyboardRemove, CallbackQuery
import pytz

from app import kb, db, utils
from app.constants import SPAN
from config import PAYMENT_TOKEN, CHANNEL_ID, TIMEZONE

basic_router = Router()
PRICE = LabeledPrice(label='Sub month', amount=100 * 100) # копейки


@basic_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    has_subscription = await utils.check_subscription(message.from_user.id)

    if has_subscription:
        await message.answer(f'Здравствуйте, {html.bold(message.from_user.full_name)}! '
                             f'Здесь вы можете получить информацию о вашей текущей подписке!',
                             reply_markup=kb.get_subscription_info())
    else:
        await message.answer(f'Здравствуйте, {html.bold(message.from_user.full_name)}! '
                            f'Здесь вы можете получить подписку на закрытый клуб!', reply_markup=kb.subscribe())


@basic_router.message(F.text.lower() == 'подписаться')
async def subscribe_handler(message: Message, bot: Bot) -> None:
    has_subscription = await utils.check_subscription(message.from_user.id)

    if has_subscription:
        await message.answer('У вас уже есть подписка!', reply_markup=ReplyKeyboardRemove())
        raise Exception(f'У пользователя с Telegram ID - {message.from_user.id} уже есть активная подписка!')
    
    await bot.unban_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)    

    if PAYMENT_TOKEN.split(':')[1] == 'TEST':
        await message.answer('Это тестовая отправка!')
    
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Подписка на закрытый клуб',
        description='Активация подписки на канал на 1 месяц',
        payload='test_payload',
        currency='rub',
        prices=[PRICE],
        message_thread_id=None,
        provider_token=PAYMENT_TOKEN,
        start_parameter='one-month-subscription',
        is_flexible=False
    )


@basic_router.message(F.text.lower() == 'продлить')
async def prolong_handler(message: Message, bot: Bot) -> None:
    has_subscription = await utils.check_subscription(message.from_user.id)
    
    if not has_subscription:
        subscribe_handler(message=message, bot=bot)
    else:
        if PAYMENT_TOKEN.split(':')[1] == 'TEST':
            await message.answer('Это тестовая отправка!')
        
        await bot.send_invoice(
            chat_id=message.chat.id,
            title='Подписка на закрытый клуб',
            description='Продление подписки на канал на 1 месяц',
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
    has_subscription = await utils.check_subscription(message.from_user.id)

    user = message.from_user
    try:
        if has_subscription:
            await db.prolong_subscription(user.id)
            await message.answer('Ваша подписка успешна продлена на 1 месяц!')
        else:
            expiration_date = datetime.now() + timedelta(minutes=5)
            link = await bot.create_chat_invite_link(
                chat_id=CHANNEL_ID,
                name='Приглашение в закрытый клуб',
                expire_date=expiration_date,
                member_limit=1,
                creates_join_request=False
            )
            
            await message.answer(f'Ваше приглашение в закрытый клуб (действительно 5 минут):\n{link.invite_link}')
            await db.add_user(user, 1)
    except Exception:
        await message.answer('Возникла непредвиденная ошибка! Свяжитесь с администратором!')
        raise


@basic_router.callback_query(F.data == 'subscription')
async def subscription_info_handler(callback_query: CallbackQuery):
    sub_info = await db.check_user(callback_query.from_user.id)
    await callback_query.message.answer(
        f'{html.bold('Дата начала подписки')} - {sub_info[3].strftime('%d.%m.%Y')}, \n'
        f'{html.bold('Дата окончания подписки')} - {sub_info[4].strftime('%d.%m.%Y')}'
    )


@basic_router.message()
async def default_handler(message: Message) -> None:
    await message.answer('Мне не известна комманда, которую вы ввели. '
                         'Пожалуйста, попробуйте ещё раз!')