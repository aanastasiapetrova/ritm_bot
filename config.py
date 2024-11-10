from environs import Env

env = Env()

BOT_TOKEN=env.str('BOT_TOKEN', '')