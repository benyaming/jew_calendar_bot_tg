# -*- coding: utf-8
import requests

import logging
from logging.handlers import RotatingFileHandler
from os import path, stat
from settings import logs_path


def get_tz_by_location(loc):
    url = f'http://api.geonames.org/timezoneJSON'
    params = {
        'username': 'arlas',
        'lat': loc[0],
        'lng': loc[1]
    }
    tz_data = requests.get(url, params=params).json()
    tz = tz_data.get('timezoneId', '')
    return tz


def set_logger():
    logger = logging.getLogger('bot_logger')
    logger.setLevel(logging.INFO)
    log_file_path = path.join(logs_path, 'jcb_logfile.log')

    handler = RotatingFileHandler(
        log_file_path,
        maxBytes=1024 * 1024 * 3,
        backupCount=20
    )
    formatter = logging.Formatter(
        fmt='%(levelname)s\t'
            '%(asctime)s\t'
            '%(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if stat(log_file_path).st_size == 0:
        f = open(log_file_path, 'w')
        f.write(f'INFO\tTIME\tACTION\tDETAILS\tSTATE\tUSER\n')
        f.close()

def log(mes):
    logger = logging.getLogger('bot_logger')
    logger.info(mes)
