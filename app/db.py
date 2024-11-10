import psycopg2

conn = psycopg2.connect('postgres://postgres:postgres@postgres:5432/ritm_db')
cursor = conn.cursor()

async def db_start() -> None:
    cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id SERIAL PRIMARY KEY, name TEXT, '
                   'sub_start TIMESTAMP, sub_end TIMESTAMP, is_sub_active BOOLEAN);')
    conn.commit()