# -*- coding: utf-8 -*-
from io import BytesIO
from datetime import datetime, timedelta

import requests
import pytz
from pyluach import dates, hebrewcal

import data
import db_operations
import picture_maker
from localization import Holidays


URL_ZMANIM = 'http://db.ou.org/zmanim/getCalendarData.php'


# Получение текущих данных о пользователе (дата, локация, тайм-зона)
def get_current_year_month_day_tz(user_id: int) -> dict:
    location = db_operations.get_location_by_id(user_id)
    tz = db_operations.get_tz_by_id(user_id)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    year = now.year
    month = now.month
    day = now.day

    response = {
        'current_year': year,
        'current_month': month,
        'current_day': day,
        'current_time_zone': tz,
        'current_location': location
    }
    return response


# Получение данных о празднике (название, дата)
def get_holiday_dict(holiday_name: str, year: int, user_id: int) -> dict:
    begin_date = dates.HebrewDate(year=year, month=7, day=1).to_pydate()
    holiday_dict = {}
    diaspora = db_operations.get_diaspora_status(user_id)
    number_days_of_hebrew_year = 365
    for days in hebrewcal.Year(year).iterdays():
        number_days_of_hebrew_year = days

    def date_range(start_date, number_days):
        for n in range(number_days + 1):
            yield start_date + timedelta(n)

    for single_date in date_range(begin_date, number_days_of_hebrew_year):
        date_item = single_date.strftime("%Y/%m/%d").split('/')
        date = {
            'year': [date_item[0], ],
            'month': [date_item[1], ],
            'day': [date_item[2], ],
            'day_of_week': [str(single_date.weekday() + 1), ]
        }

        single_hebrew_date = dates.GregorianDate(
            year=int(date['year'][0]),
            month=int(date['month'][0]),
            day=int(date['day'][0])).to_heb()

        holidays_name = hebrewcal.holiday(
            single_hebrew_date, israel=not diaspora)

        if holidays_name is None:
            pass
        else:
            if holiday_dict.get(holidays_name):
                holiday_dict[holidays_name]['day'].append(date['day'][0])
                holiday_dict[holidays_name]['month'].append(date['month'][0])
                holiday_dict[holidays_name]['year'].append(date['year'][0])
                holiday_dict[holidays_name]['day_of_week'].append(
                    str(single_date.weekday() + 1))
            else:
                holiday_dict[holidays_name] = date

    for key, values in holiday_dict.items():
        holiday_month = sorted(list(set(values['month'])))
        holiday_year = sorted(list(set(values['year'])))

        date = {'year': holiday_year,
                'month': holiday_month,
                'day': values['day'],
                'day_of_week': values['day_of_week']
                }

        holiday_dict[key] = date

    if holiday_name in ['YomHaShoah', 'YomHaZikaron', 'YomHaAtzmaut',
                        'YomYerushalayim', 'HoshanaRabba']:
        def get_add_holidays(month: int, day: int) -> dict:
            add_holiday = dates.HebrewDate(
                year=year, month=month, day=day).to_pydate()
            day_of_week = str(add_holiday.weekday())
            add_holiday = str(add_holiday).split('-')
            values_add_holiday = {
                'name': holiday_name,
                'day': [add_holiday[2], ],
                'day_of_week': day_of_week,
                'month': [add_holiday[1], ],
                'year': [add_holiday[0], ]
            }
            return values_add_holiday

        if holiday_name == 'YomHaShoah':
            return get_add_holidays(1, 27)
        elif holiday_name == 'YomHaZikaron':
            return get_add_holidays(2, 3)
        elif holiday_name == 'YomHaAtzmaut':
            return get_add_holidays(2, 4)
        elif holiday_name == 'YomYerushalayim':
            return get_add_holidays(2, 28)
        elif holiday_name == 'HoshanaRabba':
            return get_add_holidays(7, 21)
    values_from_dict = holiday_dict[holiday_name]
    values_from_dict = {
        'name': holiday_name,
        'day': values_from_dict['day'],
        'day_of_week': values_from_dict['day_of_week'],
        'month': values_from_dict['month'],
        'year': values_from_dict['year']
    }
    if len(values_from_dict['day']) == 2:
        values_from_dict['day'] = [
            values_from_dict['day'][0], values_from_dict['day'][1]
        ]
        values_from_dict['day_of_week'] = [
            values_from_dict['day_of_week'][0],
            values_from_dict['day_of_week'][1]
        ]
    elif len(values_from_dict['day']) == 7:
        values_from_dict['day'] = [
            values_from_dict['day'][0], values_from_dict['day'][6]
        ]
        values_from_dict['day_of_week'] = [
            values_from_dict['day_of_week'][0],
            values_from_dict['day_of_week'][6]
        ]
    elif len(values_from_dict['day']) == 8:
        values_from_dict['day'] = [
            values_from_dict['day'][0], values_from_dict['day'][7]
        ]
        values_from_dict['day_of_week'] = [
            values_from_dict['day_of_week'][0],
            values_from_dict['day_of_week'][7]
        ]
    return values_from_dict


# Преобразование данных о празднике (название, дата)
def transform_holiday_dict(holiday_name: str, user_id: int) -> dict:
    year = get_current_year_month_day_tz(user_id)['current_year']
    month = get_current_year_month_day_tz(user_id)['current_month']
    day = get_current_year_month_day_tz(user_id)['current_day']

    hebrew_year = dates.GregorianDate(year=year, month=month, day=day).to_heb()
    hebrew_year = str(hebrew_year).split('-')
    holiday_dict = get_holiday_dict(holiday_name, int(hebrew_year[0]), user_id)
    if holiday_dict['name'] == '10 of Teves' and \
            holiday_dict['month'][0] == '01':
        if holiday_dict['month'][0] == '01' and \
                int(holiday_dict['day'][0]) < day and \
                year == int(holiday_dict['year'][0]) or \
                year > int(holiday_dict['year'][0]):

            holiday_dict = get_holiday_dict(
                holiday_name, int(hebrew_year[0]) + 1, user_id)

    elif holiday_dict['name'] == 'Chanuka' and \
            holiday_dict['month'][0] == '01':

        if holiday_dict['month'][0] == '01' and \
                int(holiday_dict['day'][1]) < day and \
                year == int(holiday_dict['year'][1]) or \
                year > int(holiday_dict['year'][1]):

            holiday_dict = get_holiday_dict(
                holiday_name,
                int(hebrew_year[0]) + 1,
                user_id
            )

    elif len(holiday_dict['day']) == 2 and len(holiday_dict['month']) != 2:
        if month > int(holiday_dict['month'][0]) and \
                year == int(holiday_dict['year'][0]) or \
                month == int(holiday_dict['month'][0]) and \
                int(holiday_dict['day'][1]) < day and \
                year == int(holiday_dict['year'][0]) or \
                year > int(holiday_dict['year'][0]):

            holiday_dict = get_holiday_dict(
                holiday_name, int(hebrew_year[0]) + 1, user_id)

    elif len(holiday_dict['day']) == 2 and len(holiday_dict['month']) == 2:

        if month > int(holiday_dict['month'][1]) and \
                year == int(holiday_dict['year'][0]) or \
                month == int(holiday_dict['month'][1]) and \
                int(holiday_dict['day'][1]) < day and \
                year == int(holiday_dict['year'][0])\
                or year > int(holiday_dict['year'][0]):

            holiday_dict = get_holiday_dict(
                holiday_name, int(hebrew_year[0]) + 1, user_id)
    else:

        if month > int(holiday_dict['month'][0]) and \
                year == int(holiday_dict['year'][0]) or \
                month == int(holiday_dict['month'][0]) and \
                int(holiday_dict['day'][0]) < day and \
                year == int(holiday_dict['year'][0]) or \
                year > int(holiday_dict['year'][0]):

            holiday_dict = get_holiday_dict(
                holiday_name, int(hebrew_year[0]) + 1, user_id)

    return holiday_dict


# Перевод названия праздника
def get_holiday_name(holiday_info: dict, lang: str) -> str:
    holiday_names = {
        'Russian': data.holidays_name[holiday_info['name']],
        'English': data.holidays_name_en[holiday_info['name']],
        'Hebrew': data.holidays_name_he[holiday_info['name']]
    }
    holiday_name = holiday_names.get(lang, '')
    return holiday_name


# Получение даты праздника
def get_holiday_date(holiday_info: dict, lang: str) -> str:
    # Проверка на длину праздника
    if len(holiday_info['day']) >= 2:
        if len(holiday_info['month']) == 2:
            date = {
                'day_begin': holiday_info['day'][0],
                'day_end': holiday_info['day'][1],
                'day_of_week_begin': holiday_info['day_of_week'][0],
                'day_of_week_end': holiday_info['day_of_week'][1],
                'month_begin': holiday_info['month'][0],
                'month_end': holiday_info['month'][1],
                'year': holiday_info['year'][0]
            }
        else:
            date = {
                'day_begin': holiday_info['day'][0],
                'day_end': holiday_info['day'][1],
                'day_of_week_begin': holiday_info['day_of_week'][0],
                'day_of_week_end': holiday_info['day_of_week'][1],
                'month_begin': holiday_info['month'][0],
                'month_end': holiday_info['month'][0],
                'year': holiday_info['year'][0]
            }

        # Длинные праздники (Пейсах, Ханука; Суккот),
        # даты которых приходят на 1 григорианский месяц
        if holiday_info['name'] == 'Chanuka' and\
                len(holiday_info['year']) == 2:
            holiday_date = Holidays.long_holiday_two_months_two_years(
                lang, date['day_begin'], date['month_begin'],
                holiday_info['year'][0], date['day_end'], date['month_end'],
                holiday_info['year'][1], date['day_of_week_begin'],
                date['day_of_week_end']
            )
        elif holiday_info['name'] in ['Pesach', 'Chanuka', 'Succos'] and \
                len(holiday_info['month']) == 2:
            holiday_date = Holidays.long_holiday_two_months(
                lang, date['day_begin'], date['month_begin'],
                date['day_end'], date['month_end'], date['year'],
                date['day_of_week_begin'], date['day_of_week_end']
            )
        elif holiday_info['name'] in ['Pesach', 'Chanuka', 'Succos'] and \
                len(holiday_info['month']) == 1:
            holiday_date = Holidays.long_holiday_one_month(
                lang, date['day_begin'], date['day_end'], date['month_begin'],
                date['year'], date['day_of_week_begin'],
                date['day_of_week_end']
            )
        else:
            # Двухдневные праздники, даты которых
            #  приходят на 1 григорианский месяц
            if date['month_begin'] == date['month_end']:
                holiday_date = Holidays.two_days_holiday_one_month(
                    lang, date['day_begin'], date['day_end'],
                    date['month_begin'], date['year'],
                    date['day_of_week_begin'], date['day_of_week_end']
                )
            # Двухдневные праздники, даты которых
            #  приходят на 2 григорианских месяца
            else:
                holiday_date = Holidays.two_days_holiday_two_months(
                    lang, date['day_begin'], date['month_begin'],
                    date['day_end'], date['month_end'], date['year'],
                    date['day_of_week_begin'], date['day_of_week_end']
                )
    else:
        # Однодневные праздники
        date = {
            'day_of_week': holiday_info['day_of_week'][0],
            'month': holiday_info['month'][0],
            'day': holiday_info['day'][0],
            'year': holiday_info['year'][0]
        }
        holiday_date = Holidays.one_day_holiday(
            lang, date['day'], date['month'], date['year'], date['day_of_week']
        )
        if holiday_info['name'] == 'HoshanaRabba':
            holiday_date = Holidays.one_day_holiday_hoshana_rabba(
                lang, date['day'], date['month'], date['year'],
                date['day_of_week']
            )

    return holiday_date


# Получение зманим для поста
def get_fast_time(holiday_info: dict, user_id: int, lang: str) -> str:
    location = get_current_year_month_day_tz(user_id)['current_location']
    tz = get_current_year_month_day_tz(user_id)['current_time_zone']

    date = {
        'month': holiday_info['month'][0],
        'day': holiday_info['day'][0],
        'year': holiday_info['year'][0]
    }
    # Парсим зманим на текущий день
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': date['month'] + '/' + date['day'] + '/' + date['year'],
        'lat': location[0],
        'lng': location[1],
    }
    fast_time = requests.get(URL_ZMANIM, params=params).json()['zmanim']

    # Обработка мест, где невозможно определить зманим
    if fast_time['chatzos'] == 'X:XX:XX':
        return Holidays.polar_area(lang)

    # Расчет дополнительных мнений выхода поста
    sunset = datetime.strptime(fast_time['sunset'], "%H:%M:%S")
    ben_ashmashot = (sunset + timedelta(minutes=31)).strftime("%H:%M:%S")
    nevareshet = (sunset + timedelta(minutes=28)).strftime("%H:%M:%S")
    shmirat_shabat = (sunset + timedelta(minutes=25)).strftime("%H:%M:%S")

    # Обработчик для летних зманим
    if fast_time['alos_ma'] == 'X:XX:XX':
        chazot = datetime.strptime(fast_time['chatzos'], "%H:%M:%S")
        renew_alos_ma = str(datetime.time(chazot - timedelta(hours=12)))
        fast_time['alos_ma'] = renew_alos_ma

    # Обработчик для 9 Ава
    if holiday_info['name'] in ['9 of Av', 'Yom Kippur']:
        current_date = datetime.strptime(params['dateBegin'], '%m/%d/%Y')

        one_day_before = str(
            datetime.date(current_date - timedelta(days=1))).split('-')

        date_day_before = {
            'month': one_day_before[1],
            'day': one_day_before[2],
            'year': one_day_before[0]
        }
        # Парсим зманим на предыдущий день
        params = {
            'mode': 'day',
            'timezone': tz,
            'dateBegin': date_day_before['month'] + '/'
                    + date_day_before['day'] + '/' + date_day_before['year'],
            'lat': location[0],
            'lng': location[1],
        }

        fast_time = requests.get(URL_ZMANIM, params=params).json()["zmanim"]

        # Время начала и окончания поста 9 Ава
        if holiday_info['name'] == '9 of Av':
            fast_time = Holidays.tisha_av_fast(
                lang, date_day_before['day'], date_day_before['month'],
                fast_time["sunset"], fast_time["chatzos"], date['day'],
                date['month'], fast_time["tzeis_595_degrees"],
                ben_ashmashot, nevareshet, shmirat_shabat
            )
        # Время зажигания и Авдолы Йом-Кипура
        elif holiday_info['name'] == 'Yom Kippur':
            sunset = datetime.strptime(fast_time['sunset'], "%H:%M:%S")
            delta_18_minutes = timedelta(minutes=18)
            fast_time = Holidays.fast_yom_kippur(
                lang, date_day_before['day'], date_day_before['month'],
                str(datetime.time(sunset - delta_18_minutes)),
                date['day'], date['month'], fast_time["tzeis_850_degrees"])
    else:
        fast_time = Holidays.single_fast(
            lang, date['day'], date['month'], fast_time["alos_ma"],
            fast_time["tzeis_595_degrees"], ben_ashmashot, nevareshet,
            shmirat_shabat
        )

    return fast_time


# Получение зманим для праздников
def get_holiday_time(holiday_info: dict, user_id: int, lang: str,
                     last_days_pesach: bool) -> str:
    location = get_current_year_month_day_tz(user_id)['current_location']
    tz = get_current_year_month_day_tz(user_id)['current_time_zone']
    diaspora = db_operations.get_diaspora_status(user_id)

    date = {
        'day_of_week': holiday_info['day_of_week'][0],
        'month': holiday_info['month'][0],
        'day': holiday_info['day'][0],
        'year': holiday_info['year'][0]
    }
    if last_days_pesach and len(holiday_info['month']) != 2:
        date['day'] = holiday_info['day'][1]
    elif last_days_pesach and len(holiday_info['month']) == 2:
        date['day'] = holiday_info['day'][1]
        date['month'] = holiday_info['month'][1]

    # Парсим зманим на текущий день
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': date['month'] + '/' + date['day'] + '/' + date['year'],
        'lat': location[0],
        'lng': location[1],
        'havdala_offset': '72'
    }

    current_time = requests.get(URL_ZMANIM, params=params).json()['zmanim']

    # Обработка мест, где невозможно определить зманим
    if current_time['chatzos'] == 'X:XX:XX':
        return Holidays.polar_area(lang)

    delta_18_minutes = timedelta(minutes=18)
    delta_one_day = timedelta(days=1)
    delta_two_days = timedelta(days=2)

    # Расчет соседних дней праздника
    current_date = datetime.strptime(params['dateBegin'], '%m/%d/%Y')
    date_plus_1_day = (current_date + delta_one_day).strftime('%m/%d/%Y')
    date_minus_1_day = (current_date - delta_one_day).strftime('%m/%d/%Y')
    date_plus_2_day = (current_date + delta_two_days).strftime('%m/%d/%Y')
    date_minus_2_day = (current_date - delta_two_days).strftime('%m/%d/%Y')

    params = {
        'mode': 'day', 'timezone': tz, 'dateBegin': date_plus_1_day,
        'lat': location[0], 'lng': location[1], 'havdala_offset': '72'
    }
    time_plus_1_day = requests.get(URL_ZMANIM, params=params).json()['zmanim']

    params = {
        'mode': 'day', 'timezone': tz, 'dateBegin': date_minus_1_day,
        'lat': location[0], 'lng': location[1], 'havdala_offset': '72'
    }
    time_minus_1_day = requests.get(URL_ZMANIM, params=params).json()['zmanim']

    params = {
        'mode': 'day', 'timezone': tz, 'dateBegin': date_plus_2_day,
        'lat': location[0], 'lng': location[1], 'havdala_offset': '72'
    }
    time_plus_2_day = requests.get(URL_ZMANIM, params=params).json()['zmanim']

    params = {
        'mode': 'day', 'timezone': tz, 'dateBegin': date_minus_2_day,
        'lat': location[0], 'lng': location[1], 'havdala_offset': '72'
    }
    time_minus_2_day = requests.get(URL_ZMANIM, params=params).json()['zmanim']

    if 'X:XX:XX' in [time_plus_1_day['chatzos'], time_minus_1_day['chatzos'],
                     time_plus_2_day['chatzos']]:
        return Holidays.polar_area(lang)

    sunset_current_date = datetime.strptime(
        current_time['sunset'], "%H:%M:%S"
    )
    sunset_plus_1_day = datetime.strptime(
        time_plus_1_day['sunset'], "%H:%M:%S"
    )
    sunset_plus_2_day = datetime.strptime(
        time_plus_2_day['sunset'], "%H:%M:%S"
    )
    sunset_minus_1_day = datetime.strptime(
        time_minus_1_day['sunset'], "%H:%M:%S"
    )
    sunset_minus_2_days = datetime.strptime(
        time_minus_2_day['sunset'],  "%H:%M:%S"
    )

    # Создание словарей для обозначения разных дней/месяцев
    date_plus_1_day = date_plus_1_day.split('/')
    date_minus_1_day = date_minus_1_day.split('/')
    date_plus_2_day = date_plus_2_day.split('/')
    date_minus_2_day = date_minus_2_day.split('/')
    current_date = current_date.strftime('%m/%d/%Y').split('/')

    current_date = {
        'day': current_date[1], 'month': current_date[0]
    }
    date_plus_1_day = {
        'day': date_plus_1_day[1], 'month': date_plus_1_day[0]
    }
    date_minus_1_day = {
        'day': date_minus_1_day[1], 'month': date_minus_1_day[0],
    }
    date_plus_2_days = {
        'day': date_plus_2_day[1], 'month': date_plus_2_day[0]
    }
    date_minus_2_days = {
        'day': date_minus_2_day[1], 'month': date_minus_2_day[0]
    }

    # Проверка на диаспору
    if diaspora:
        if date['day_of_week'][0] == '4' and last_days_pesach:
            holiday_string = Holidays.lighting_double(
                lang,
                # date_minus_2_days['day'],
                # date_minus_2_days['month'],
                # (sunset_minus_2_days - delta_18_minutes).strftime("%H:%M:%S"),
                date_minus_2_days['day'],
                date_minus_2_days['month'],
                (sunset_minus_2_days - delta_18_minutes).strftime("%H:%M:%S"),
                date_minus_1_day['day'],
                date_minus_1_day['month'],
                time_minus_1_day["tzeis_850_degrees"],
                current_date['day'],
                current_date['month'],
                current_time["tzeis_850_degrees"]
            )
        elif date['day_of_week'][0] == '5':
            holiday_string = Holidays.lighting_shabbat(
                lang=lang,
                light_day=date_minus_1_day['day'],
                light_month=date_minus_1_day['month'],
                light_time=(sunset_minus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                light_shab_day=current_date['day'],
                light_shab_month=current_date['month'],
                light_shab_time=(sunset_plus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                avdala_day=date_plus_1_day['day'],
                avdala_month=date_plus_1_day['month'],
                avdala_time=time_plus_2_day["tzeis_850_degrees"],
                # date_plus_2_days['day'],
                # date_plus_2_days['month'],
                # time_plus_2_day["tzeis_850_degrees"]
            )
        elif date['day_of_week'][0] == '7' or \
                date['day_of_week'] == '7' and last_days_pesach:
            holiday_string = Holidays.shabbat_before_holiday_diaspora(
                lang, date_minus_2_days['day'], date_minus_2_days['month'],
                (sunset_minus_2_days - delta_18_minutes).strftime("%H:%M:%S"),
                date_minus_1_day['day'], date_minus_1_day['month'],
                time_minus_1_day["tzeis_850_degrees"], current_date['day'],
                current_date['month'], current_time["tzeis_850_degrees"],
                date_plus_1_day['day'], date_plus_1_day['month'],
                time_plus_1_day["tzeis_850_degrees"]
            )
        elif last_days_pesach:
            holiday_string = Holidays.lighting_double(
                lang, date_minus_2_days['day'], date_minus_2_days['month'],
                (sunset_minus_2_days - delta_18_minutes).strftime("%H:%M:%S"),
                date_minus_1_day['day'], date_minus_1_day['month'],
                (sunset_minus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                current_date['day'], current_date['month'],
                current_time["tzeis_850_degrees"]
            )
        elif date['day_of_week'][0] == '6':
            holiday_string = Holidays.shabbat_include(
                lang, date_minus_1_day['day'], date_minus_1_day['month'],
                (sunset_minus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                current_date['day'], current_date['month'],
                current_time["tzeis_850_degrees"], date_plus_1_day['day'],
                date_plus_1_day['month'],
                time_plus_1_day["tzeis_850_degrees"]
            )
        else:
            holiday_string = Holidays.lighting_double(
                lang, date_minus_1_day['day'], date_minus_1_day['month'],
                (sunset_minus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                current_date['day'], current_date['month'],
                current_time["tzeis_850_degrees"], date_plus_1_day['day'],
                date_plus_1_day['month'],
                time_plus_1_day["tzeis_850_degrees"]
            )
    else:
        if last_days_pesach:
            holiday_string = Holidays.lighting(
                lang=lang,
                light_day=date_minus_1_day['day'],
                light_month=date_minus_1_day['month'],
                light_time=(sunset_current_date - delta_18_minutes).strftime('%H:%M:%S'),
                avdala_day=current_date['day'],
                avdala_month=current_date['month'],
                avdala_time=current_time['tzeis_850_degrees']
            )
            # holiday_string = Holidays.lighting(
            #     lang, current_date['day'], current_date['month'],
            #     (sunset_current_date - delta_18_minutes).strftime(
            #         "%H:%M:%S"),  date_plus_1_day['day'],
            #     date_plus_1_day['month'],  time_plus_1_day["tzeis_850_degrees"]
            # )
        elif date['day_of_week'] == '7':
            holiday_string = Holidays.one_day_shabbat_before(
                lang, date_minus_2_days['day'], date_minus_2_days['month'],
                (sunset_minus_2_days - delta_18_minutes).strftime("%H:%M:%S"),
                date_minus_1_day['day'], date_minus_1_day['month'],
                time_plus_1_day["tzeis_850_degrees"], current_date['day'],
                current_date['month'], current_time["tzeis_850_degrees"]
            )
        elif date['day_of_week'] == '5':
            holiday_string = Holidays.lighting_shabbat(
                lang, date_minus_1_day['day'], date_minus_1_day['month'],
                (sunset_minus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                current_date['day'], current_date['month'],
                (sunset_current_date - delta_18_minutes).strftime(
                    "%H:%M:%S"), date_plus_1_day['day'],
                date_plus_1_day['month'], time_plus_1_day["tzeis_850_degrees"]
            )
        elif holiday_info['name'] == 'Rosh Hashana':
            # One time fix for Rosh hashana 2020 only!
            holiday_string = Holidays.shabbat_include(
                lang=lang,
                light_1_day=date_minus_1_day['day'],
                light_1_month=date_minus_1_day['month'],
                light_1_time=(sunset_minus_1_day - delta_18_minutes).strftime('%H:%M:%S'),
                light_2_day=current_date['day'],
                light_2_month=current_date['month'],
                light_2_time=current_time['tzeis_850_degrees'],
                avdala_day=date_plus_1_day['day'],
                avdala_month=date_plus_1_day['month'],
                avdala_time=time_plus_1_day['tzeis_850_degrees']
            )
        else:
            holiday_string = Holidays.lighting(
                lang, date_minus_1_day['day'], date_minus_1_day['month'],
                (sunset_minus_1_day - delta_18_minutes).strftime("%H:%M:%S"),
                current_date['day'], current_date['month'],
                current_time["tzeis_850_degrees"]
            )

    return holiday_string


# Собираем строку для праздника
def get_holiday_str(holiday_name: str, user_id: int, lang: str) -> str:
    diaspora = db_operations.get_diaspora_status(user_id)
    holiday_string = ''

    if holiday_name in 'israel_holidays':
        for israel_name in ['YomHaShoah', 'YomHaZikaron', 'YomHaAtzmaut',
                            'YomYerushalayim']:
            holiday_dict = transform_holiday_dict(israel_name, user_id)
            holiday_dict['day_of_week'] = str(int(holiday_dict['day_of_week']) + 1)
            holiday_name = get_holiday_name(holiday_dict, lang)
            holiday_date = get_holiday_date(holiday_dict, lang)
            if israel_name == 'YomYerushalayim':
                holiday = f'{holiday_name}%{holiday_date}'
            else:
                holiday = f'{holiday_name}%{holiday_date}\n'
            holiday_string += holiday
        return holiday_string

    holiday_dict = transform_holiday_dict(holiday_name, user_id)
    holiday_name = get_holiday_name(holiday_dict, lang)
    holiday_date = get_holiday_date(holiday_dict, lang)

    holiday_string = holiday_date

    if holiday_dict['name'] in ['Taanis Esther', '17 of Tamuz', 'Yom Kippur',
                                '9 of Av', 'Tzom Gedalia', '10 of Teves']:
        fast_time = get_fast_time(holiday_dict, user_id, lang)
        holiday_string = f'{holiday_name}\n\n{holiday_date}\n{fast_time}'

    holiday_time = get_holiday_time(holiday_dict, user_id, lang, False)

    if holiday_dict['name'] in ['Rosh Hashana', 'Shavuos']:
        holiday_string = f'{holiday_date}\n{holiday_time}'

    if holiday_dict['name'] == 'Succos':
        hoshana_rabba_dict = transform_holiday_dict('HoshanaRabba', user_id)
        hoshana_rabba_name = get_holiday_name(hoshana_rabba_dict, lang)
        hoshana_rabba_date = get_holiday_date(hoshana_rabba_dict, lang)
        holiday_string = f'{holiday_date}\n{holiday_time}\n' \
                         f'{hoshana_rabba_name}: |{hoshana_rabba_date}'

    elif holiday_dict['name'] == 'Pesach':
        holiday_time_last_days = get_holiday_time(
            holiday_dict, user_id, lang, True)
        holiday_string = f'{holiday_date}\n' \
                         f'{holiday_time}\n' \
                         f'!{holiday_time_last_days}'

    elif holiday_dict['name'] == 'Shmini Atzeres':
        if diaspora:
            holiday_dates = {
                'Russian': 'Дата: |21-22 Октября 2019,^Понедельник-Вторник',
                'English': 'Date: |21-22 October 2019,^Monday-Tuesday',
                # TODO hebrew
            }
            holiday_date = holiday_dates.get(lang, '')
        holiday_string = f'{holiday_date}\n{holiday_time}'

    return holiday_string


def get_holiday_pic(holiday_name: str, user_id: int, lang: str) -> BytesIO:
    text = get_holiday_str(holiday_name, user_id, lang)
    pic_renders = {
        'Taanis Esther': picture_maker.FastSender,
        '17 of Tamuz': picture_maker.FastSender,
        '9 of Av': picture_maker.FastSender,
        'Tzom Gedalia': picture_maker.FastSender,
        '10 of Teves': picture_maker.FastSender,
        'Tu B\'shvat': picture_maker.TuBiShvatSender,
        'Lag Ba\'omer': picture_maker.LagBaomerSender,
        'israel_holidays': picture_maker.IsraelHolidaysSender,
        'Purim': picture_maker.PurimSender,
        'Yom Kippur': picture_maker.YomKippurSender,
        'Chanuka': picture_maker.ChanukaSender,
        'Succos': picture_maker.SucosSender,
        'Pesach': picture_maker.PesahSender,
        'Rosh Hashana': picture_maker.RoshHashanaSender,
        'Shavuos': picture_maker.ShavuotSender,
        'Shmini Atzeres': picture_maker.ShminiAtzeretSender
    }
    pic = pic_renders.get(holiday_name)(lang).get_image(text)
    return pic
