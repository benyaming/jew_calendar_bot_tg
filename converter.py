from pyluach.dates import GregorianDate
from pyluach.hebrewcal import Month

import localization


def convert_greg_to_heb(date: tuple, lang: str):
    year = date[0]
    month = date[1]
    day = date[2]
    hebrew_date = GregorianDate(year, month, day).to_heb()
    hebrew_date = (
        hebrew_date.year,
        Month(hebrew_date.year, hebrew_date.month).name,
        hebrew_date.day
    )
    response = localization.Converter.convert_greg_to_heb(
        date,
        hebrew_date,
        lang
    )
    return response
