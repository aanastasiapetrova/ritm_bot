from datetime import datetime, timedelta
import psycopg2

conn = psycopg2.connect('postgres://postgres:postgres@postgres:5432/ritm_db')
cursor = conn.cursor()

async def db_start() -> None:
    """
    Инициируется таблица с клиентской базой с атрибутивным составом:
        - user_id - telegram_id пользователя
        - name - параметр full_name пользователя
        - sub_start - дата начала подписки
        - sub_end - дата окончания подписки
        - is_sub_active - признак действительности подписки
    """
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, name TEXT, '
                   'sub_start TIMESTAMP, sub_end TIMESTAMP, is_sub_active BOOLEAN);')
    conn.commit()


async def add_user(user, span) -> None:
    sub_start = datetime.now()
    cursor.execute(f'INSERT INTO users VALUES ({user.id}, \'{user.full_name}\', \'{sub_start}\', '
                   f'\'{sub_start + timedelta(weeks=4 * span)}\', true);')
    conn.commit()


async def check_user(user_id):
    cursor.execute(f'SELECT * FROM users WHERE user_id = {user_id} LIMIT 1')
    return cursor.fetchone()