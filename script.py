from datetime import datetime
from math import ceil
from time import time
from aiogram import Bot, html
import pytz

from app import db, kb
from config import CHANNEL_ID, TIMEZONE


async def track_subs(bot: Bot) -> None:
    admins = await bot.get_chat_administrators(chat_id=CHANNEL_ID)
    to_remove, to_remind = await db.check_sub_expiration()
    
    for user_id, name, username in to_remove:
        await bot.ban_chat_member(chat_id=CHANNEL_ID, user_id=user_id, until_date=int(ceil(time())) + 30)
        await bot.send_message(user_id,
                               'Вы были исключены из закрытого клуба, поскольку срок вашей подпсики истек! \n\n'
                               'Вы можете оформить новую подписку по кнопке ниже.',
                               reply_markup=kb.subscribe())
        
        for admin in admins:
            if not admin.user.is_bot:
                await bot.send_message(admin.user.id,
                                       f'Пользователь {html.bold(name)} (@{username}, id: {user_id}) '
                                       f'удален из канала после истечения подписки.')
    
    for user_id, sub_end in to_remind:
        delta = (sub_end - datetime.now())
        before_expire_msg = f'{delta.seconds // 3600} час(-а/-ов)' if not delta.days else f'{delta.days} день(-я/-ей)'
        sub_end = sub_end.strftime('%d.%m.%Y')

        await bot.send_message(user_id,
                               f'До истечения срока вашей подписки осталось {html.bold(before_expire_msg)} ({sub_end}). '
                               f'В случае непродления вы будете исключены из закрытого канала. \n\n'
                               f'Вы можете продлить подписку по кнопке ниже.',
                               reply_markup=kb.restore())