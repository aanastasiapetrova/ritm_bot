from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN', default='')
PAYMENT_TOKEN = env.str('PAYMENT_TOKEN', default='')
CHANNEL_ID = env.str('CHANNEL_ID', default='')