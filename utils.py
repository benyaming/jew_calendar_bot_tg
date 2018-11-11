# -*- coding: utf-8
import requests

import logging
from logging.handlers import RotatingFileHandler
from os import path
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
    handler = RotatingFileHandler(
        path.join(
            logs_path,
            'jcb_logfile.log'
        ),
        maxBytes=1024 * 1024 * 3,
        backupCount=20
    )
    formatter = logging.Formatter(
        fmt='%(filename)s\t[LINE:%(lineno)d]\t%(levelname)-8s'
            '[%(asctime)s]\t'
            '%(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log(mes):
    logger = logging.getLogger('bot_logger')
    logger.info(mes)
