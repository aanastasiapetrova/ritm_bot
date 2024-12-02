from datetime import datetime, timedelta
import logging
import psycopg2
import pytz

from app.constants import SPAN
from config import TIMEZONE

conn = psycopg2.connect('postgres://postgres:postgres@postgres:5432/ritm_db')
cursor = conn.cursor()

logger = logging.getLogger(__name__)

async def db_start() -> None:
    """
    Инициируется таблица с клиентской базой с атрибутивным составом:
        - user_id - telegram_id пользователя
        - name - параметр full_name пользователя
        - user_name - username пользовтеля
        - sub_start - дата начала подписки
        - sub_end - дата окончания подписки
        - is_sub_active - признак действительности подписки
    """
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, name TEXT, username TEXT, '
                   'sub_start TIMESTAMP, sub_end TIMESTAMP, is_sub_active BOOLEAN);')
    conn.commit()


async def add_user(user, span) -> None:
    sub_start = datetime.now()
    cursor.execute(f'INSERT INTO users VALUES ({user.id}, \'{user.full_name}\', \'{user.username}\',  \'{sub_start}\', '
                   f'\'{sub_start + timedelta(weeks=4 * SPAN)}\', true);')
    conn.commit()


async def check_user(user_id):
    cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id} AND is_sub_active = true;')
    return cursor.fetchone()


async def check_sub_expiration():
    try:
        cursor.execute('SELECT user_id, name, username FROM users WHERE (sub_end - now()) <= make_interval(days => 0);')
        to_remove = cursor.fetchall()
        
        ids_to_remove = [usr[0] for usr in to_remove]
        if ids_to_remove:
            cursor.execute(f'UPDATE users SET is_sub_active = false WHERE user_id IN ({', '.join(map(str, ids_to_remove))});')
            conn.commit()
        
        cursor.execute('SELECT user_id, sub_end FROM users WHERE ((sub_end - now()) > make_interval(days => 0)) AND ((sub_end - now()) < make_interval(days => 3));')
        to_remind = cursor.fetchall()
            
        return to_remove, to_remind
    except Exception:
        cursor.execute('ROLLBACK')
        conn.commit()
        raise


async def prolong_subscription(user_id):
    cursor.execute(f'SELECT sub_end FROM users WHERE user_id = {user_id};')
    sub_end = cursor.fetchone()[0]
    
    prolonged_sub_end = sub_end + timedelta(weeks=4 * SPAN)
    cursor.execute(f'UPDATE users SET sub_end = \'{prolonged_sub_end}\', is_sub_active = true WHERE user_id = {user_id};')
    conn.commit()