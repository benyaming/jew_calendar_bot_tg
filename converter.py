from pyluach.dates import GregorianDate, HebrewDate
from pyluach.hebrewcal import Month

from datetime import datetime

import localization


def convert_greg_to_heb(date: tuple, lang: str) -> str:
    year = date[0]
    month = date[1]
    day = date[2]
    hebrew_date = GregorianDate(year, month, day).to_heb()
    hebrew_date = (
        hebrew_date.year,
        Month(hebrew_date.year, hebrew_date.month).name,
        hebrew_date.day
    )
    day_of_week = datetime(*date).weekday()
    response = localization.Converter.convert_greg_to_heb(
        date,
        day_of_week,
        hebrew_date,
        lang
    )
    return response


def convert_heb_to_greg(hebrew_date: tuple, lang: str) -> dict:
    year = hebrew_date[0]
    month = hebrew_date[1]
    day = hebrew_date[2]
    try:
        greg_date = HebrewDate(year, month, day).to_greg().tuple()
        day_of_week = datetime(*greg_date).weekday()
        response = dict()
        response['response'] = localization.Converter.convert_heb_to_greg(
            hebrew_date,
            day_of_week,
            greg_date,
            lang
        )
        response['date'] = greg_date
    except Exception as e:
        print(e)
        response = {}
    return response
