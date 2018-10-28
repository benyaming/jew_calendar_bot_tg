from pyluach.dates import GregorianDate, HebrewDate
from pyluach.hebrewcal import Month, Year

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
    year_is_leap = Year(year).leap
    response = dict()
    try:
        if year_is_leap:  # если високосный год
            if month == 12:  # просят адар (или адар 1) выводим и для адара 2

                adar = True
                hebrew_date_1 = (
                    hebrew_date[0],
                    13,  # чтобы вывело "адар 1"
                    hebrew_date[2]
                )
                greg_date_1 = HebrewDate(year, 12, day).to_greg().tuple()
                day_of_week_1 = datetime(*greg_date_1).weekday()
                greg_date_2 = HebrewDate(year, 13, day).to_greg().tuple()
                day_of_week_2 = datetime(*greg_date_2).weekday()
                response['response'] = \
                    localization.Converter.convert_heb_to_greg_two(
                    hebrew_date_1,
                    day_of_week_1, day_of_week_2,
                    greg_date_1, greg_date_2,
                    lang
                )
                response['date'] = [greg_date_1, greg_date_2]
                return response
            elif month == 13:
                # спросили чётко про адар 2
                hebrew_date = (
                    hebrew_date[0],
                    14,  # чтобы вывело "адар 2"
                    hebrew_date[2]
                )
        greg_date = HebrewDate(year, month, day).to_greg().tuple()
        day_of_week = datetime(*greg_date).weekday()
        response['response'] = localization.Converter.convert_heb_to_greg(
            hebrew_date,
            day_of_week,
            greg_date,
            lang
        )
        response['date'] = greg_date
        return response
    except Exception:
        return {}
