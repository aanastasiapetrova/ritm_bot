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