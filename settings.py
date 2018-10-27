# -*- coding: utf-8 -*-
from os import environ

IS_SERVER = environ.get('IS_SERVER')

TOKEN = environ.get('TOKEN')  # bot's token
TIMEZONE_DB_API_KEY = environ.get('TIMEZONE_DB_API_KEY')

BOT_HOST = environ.get('BOT_HOST')  # sever's ip (not localhost!)
BOT_PORT = environ.get('BOT_PORT')  # server's port

CHATBASE_TOKEN = environ.get('CHATBASE_TOKEN')

# db settings
dbname = environ.get('dbname')
user = environ.get('user')
password = environ.get('password')
port = environ.get('port')
host = environ.get('host')  # localhost

db_parameters_string = f'dbname={dbname} ' \
                       f'user={user} ' \
                       f'password={password} ' \
                       f'host={host} ' \
                       f'port={port}'

r_host = environ.get('redis_host')
r_port = environ.get('redis_port')
logs_path = environ.get('logs_path')