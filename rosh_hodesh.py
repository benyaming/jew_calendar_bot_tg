import calendar
import re
from io import BytesIO
from datetime import datetime

import requests
import pytz
from pyluach import dates

import localization as locale
import db_operations
from utils import get_tz_by_location
from picture_maker import RoshHodeshSender


URL = 'http://db.ou.org/zmanim/getHolidayCalData.php'


def get_chodesh_dict(hebrew_date, params):
    chodesh = requests.get(URL, params=params)
    chodesh_dicts = chodesh.json()
    month = hebrew_date[1]
    if month == 6:
        next_year = hebrew_date[0] + 1
        params = {'hebrewYear': next_year}
        molad_next_year = requests.get(URL, params=params)
        new_chodesh_dicts = molad_next_year.json()
        chodesh_dict = new_chodesh_dicts[6]
    elif len(chodesh_dicts) == 13:  # если год високосный
        if month < 13:  # если первые 12 месяцев
            chodesh_dict = chodesh_dicts[month]
        else:  # если адар II
            chodesh_dict = chodesh_dicts[0]  # выбираем в нем нисан
    else:  # если год не високосный — дальше так же
        if month < 12:
            chodesh_dict = chodesh_dicts[month]
        else:
            chodesh_dict = chodesh_dicts[0]
    return chodesh_dict


def get_month_name(chodesh_dict):
    # парсим название месяца
    month = re.findall(r'[a-zA-z]+', chodesh_dict['JewishMonth'])
    if len(month) == 2:
        month_str = f'{month[0]} {month[1]}'
    else:
        month_str = f'{month[0]}'
    return month_str


def get_rh_lenght(hebrew_date):
    # получаем длинну ТЕКУЩЕГО еврейского месяца чтоб определить длинну РХ
    month_days = dates.HebrewDate._month_length(hebrew_date[0], hebrew_date[1])
    if month_days == 30:
        return 2
    else:
        return 1


def get_rh_date_and_day(hebrew_date, lenght, lang):
    # определяем число дней в месяце:
    month_days = dates.HebrewDate._month_length(hebrew_date[0], hebrew_date[1])
    # определяем дату последнего дня месяца
    last_month_day = dates.HebrewDate(hebrew_date[0],
                                      hebrew_date[1],
                                      month_days
                                      ).to_greg().tuple()
    # определяем длинну рош ходеша
    if lenght == 2:
        # проверка на случай если два дня РХ в разных месяцах гр. календаря
        first_day = last_month_day[2]
        month_length = calendar.monthrange(last_month_day[0],
                                           last_month_day[1]
                                           )[1]
        if first_day == month_length:
            if last_month_day[1] == 12:  # проверка на случай если это декабрь
                rh_days = locale.RoshHodesh.two_days_in_different_years(
                    lang,
                    last_month_day[0],
                    last_month_day[0] + 1
                )
                # определяем день недели
                day_of_week_id = calendar.weekday(
                    last_month_day[0], 12, 31)
                day_of_week = locale.RoshHodesh.get_rh_day_of_week(
                    lang,
                    day_of_week_id,
                    day_of_week_id + 1
                )
            else:
                rh_days = locale.RoshHodesh.two_days_in_different_months(
                    lang,
                    first_day,
                    last_month_day[1],
                    last_month_day[1] + 1,
                    last_month_day[0]
                )
                # определяем день недели
                day_of_week_id = calendar.weekday(
                    last_month_day[0],
                    last_month_day[1],
                    first_day
                )
                day_of_week = locale.RoshHodesh.get_rh_day_of_week(
                    lang,
                    day_of_week_id,
                    day_of_week_id + 1
                )
        else:
            rh_days = locale.RoshHodesh.two_days(
                lang,
                first_day,
                first_day + 1,
                last_month_day[1],
                last_month_day[0]
            )
            # определяем день недели
            day_of_week_id = calendar.weekday(
                last_month_day[0],
                last_month_day[1],
                first_day
            )
            day_of_week = locale.RoshHodesh.get_rh_day_of_week(
                lang,
                day_of_week_id,
                day_of_week_id + 1
            )
    else:
        # проверка на то, является ли число перед рх последним днем гр месяца
        month_length = calendar.monthrange(
            last_month_day[0],
            last_month_day[1]
        )[1]
        if last_month_day[2] == month_length:
            # проверка, является ли это декабрь
            if last_month_day[1] == 12:
                rh_days = locale.RoshHodesh.one_day_first_day_of_jan(
                    lang,
                    last_month_day[0] + 1
                )
                # определяем день недели
                day_of_week_id = calendar.weekday(
                    last_month_day[0] + 1,
                    1,
                    1
                )
                day_of_week = locale.RoshHodesh.get_rh_day_of_week(
                    lang,
                    day_of_week_id
                )
            else:  # если первое число месяца
                rh_days = locale.RoshHodesh.one_day_first_day_of_month(
                    lang,
                    last_month_day[1] + 1,
                    last_month_day[0]
                )
                # определяем день недели
                day_of_week_id = calendar.weekday(
                    last_month_day[0],
                    last_month_day[1] + 1,
                    1
                )
                day_of_week = locale.RoshHodesh.get_rh_day_of_week(
                    lang,
                    day_of_week_id
                )
        else:  # обычный рх
            rh_days = locale.RoshHodesh.one_day(
                lang,
                last_month_day[2] + 1,
                last_month_day[1],
                last_month_day[0]
            )
            # определяем день недели
            day_of_week_id = calendar.weekday(
                last_month_day[0],
                last_month_day[1],
                last_month_day[2] + 1)
            day_of_week = locale.RoshHodesh.get_rh_day_of_week(
                lang,
                day_of_week_id
            )
    return f'{rh_days}, {day_of_week}'


def get_molad(chodesh_dict, lang):
    # парсим название месяца
    molad_month = re.search(r'[a-zA-z]+', chodesh_dict['EnglishDate']).group(0)
    # парсим число молада
    molad_day = int(re.search(r'\d+', chodesh_dict['EnglishDate']).group(0))
    # парсим числа для молада — часы, минуты, части
    molad_numbers = re.findall(r'\d+', chodesh_dict['Molad'])
    # парсим день недели молада
    day_of_week = re.search(r'[a-zA-z]+', chodesh_dict['DayOfWeek']).group(0)

    molad = locale.RoshHodesh.get_molad_str(
        lang,
        molad_day,
        molad_month,
        day_of_week,
        int(molad_numbers[0]),
        molad_numbers[0],
        int(molad_numbers[1]),
        # molad_numbers[1],
        int(molad_numbers[2]),
        molad_numbers[2]
    )
    return molad


def get_rh(user_id: int, lang, date=None) -> BytesIO:
    loc = db_operations.get_location_by_id(user_id)
    tz = get_tz_by_location(loc)

    if not date:
        tz_time = pytz.timezone(tz)
        now = datetime.now(tz_time)
        hebrew_date = dates.GregorianDate(
            now.year,
            now.month,
            now.day
        ).to_heb().tuple()
    else:
        hebrew_date = dates.GregorianDate(
            date[0],
            date[1],
            date[2]
        ).to_heb().tuple()
    # проверка на то что сегодня не рош ходеш
    if hebrew_date[2] == 30:
        hebrew_date = (
            hebrew_date[0],
            hebrew_date[1],
            29
        )
    elif hebrew_date[2] == 1:
        hebrew_date = (
            hebrew_date[0],
            hebrew_date[1] - 1,
            29
        )
    # проверка на рош ашану
    if hebrew_date[1] == 6:
        hebrew_date = (
            hebrew_date[0],
            hebrew_date[1] + 1,
            hebrew_date[2]
        )
    params = {'hebrewYear': hebrew_date[0]}
    chodesh_dict = get_chodesh_dict(hebrew_date, params)
    length_of_rh = get_rh_lenght(hebrew_date)
    rh_string = locale.RoshHodesh.get_rh_str(
        lang,
        get_month_name(chodesh_dict),
        length_of_rh,
        get_rh_date_and_day(hebrew_date, length_of_rh, lang),
        get_molad(chodesh_dict, lang)
    )
    rh_pic = RoshHodeshSender(lang).get_rh_picture(rh_string)
    return rh_pic
