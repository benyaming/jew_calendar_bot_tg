# -*- coding: utf-8
import re
import requests

import pytz

from datetime import datetime, timedelta

import db_operations

import localization as l


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_zmanim(user, lang):
    tz = db_operations.get_tz_by_id(user)
    loc = db_operations.get_location_by_id(user)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': f'{now.month}/{now.day}/{now.year}',
        'lat': loc[0],
        'lng': loc[1]
    }
    zmanim = requests.get(URL, params=params)
    zmanim_dict = zmanim.json()
    month = re.search(r'[a-zA-z]+', zmanim_dict['hebDateString']) \
        .group(0)
    year_day = re.findall(r'\d+', zmanim_dict['hebDateString'])

    if zmanim_dict['zmanim']['sunset'] == 'X:XX:XX':
        zmanim_str = l.Zmanim.get_polar_error(lang)
        return zmanim_str
    elif zmanim_dict['zmanim']['tzeis_595_degrees'] == 'X:XX:XX':
        chazot_time = datetime.strptime(zmanim_dict['zmanim']['chatzos'],
                                        "%H:%M:%S")
        chazot_delta = timedelta(hours=12)
        # высчитываем полночь, прибавляя 12 часов
        d6 = chazot_time + chazot_delta
        chazot_laila = str(datetime.time(d6))

        alot_delta = chazot_time - chazot_delta
        alot_chazot_time = str(datetime.time(alot_delta))

        zmanim_dict['zmanim']['alos_ma'] = alot_chazot_time
        zmanim_dict['zmanim']['talis_ma'] = alot_chazot_time
        zmanim_dict['zmanim']['tzeis_595_degrees'] = chazot_laila
    elif zmanim_dict['zmanim']['alos_ma'] == 'X:XX:XX'\
            and zmanim_dict['zmanim']['talis_ma'] == 'X:XX:XX':
        chazot_time = datetime.strptime(zmanim_dict['zmanim']['chatzos'],
                                        "%H:%M:%S")
        chazot_delta = timedelta(hours=12)
        alot_delta = chazot_time - chazot_delta
        alot_chazot_time = str(datetime.time(alot_delta))
        zmanim_dict['zmanim']['alos_ma'] = alot_chazot_time
        zmanim_dict['zmanim']['talis_ma'] = alot_chazot_time
    elif zmanim_dict['zmanim']['alos_ma'] == 'X:XX:XX':
        chazot_time = datetime.strptime(zmanim_dict['zmanim']['chatzos'],
                                        "%H:%M:%S")
        chazot_delta = timedelta(hours=12)
        alot_delta = chazot_time - chazot_delta
        alot_chazot_time = str(datetime.time(alot_delta))
        zmanim_dict['zmanim']['alos_ma'] = alot_chazot_time

    zmanim_str = l.Zmanim.get_regular_zmanim(
        lang,
        int(year_day[0]),
        month,
        int(year_day[1]),
        zmanim_dict['zmanim']['alos_ma'][:-3],
        zmanim_dict['zmanim']['talis_ma'][:-3],
        zmanim_dict['zmanim']['sunrise'][:-3],
        zmanim_dict['zmanim']['sof_zman_shema_gra'][:-3],
        zmanim_dict['zmanim']['sof_zman_tefila_gra'][:-3],
        zmanim_dict['zmanim']['chatzos'][:-3],
        zmanim_dict['zmanim']['mincha_gedola_ma'][:-3],
        zmanim_dict['zmanim']['sunset'][:-3],
        zmanim_dict['zmanim']['tzeis_595_degrees'][:-3]
    )
    return zmanim_str


def get_ext_zmanim(
        user,
        lang,
        custom_day=None,
        custom_month=None,
        custom_year=None
):
    tz = db_operations.get_tz_by_id(user)
    loc = db_operations.get_location_by_id(user)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    if custom_day and custom_month and custom_year:
        if len(str(custom_year)) == 2:
            custom_year = f'00{custom_year}'
        elif len(str(custom_year)) == 3:
            custom_year = f'0{custom_year}'
        date_str = f'{custom_month}/{custom_day}/{custom_year}'
    else:
        date_str = f'{now.month}/{now.day}/{now.year}'
    params = {'mode': 'day',
              'timezone': tz,
              'dateBegin': date_str,
              'lat': loc[0],
              'lng': loc[1]
              }
    zmanim = requests.get(URL, params=params)
    zmanim_dict = zmanim.json()
    month = re.search(r'[a-zA-z]+', zmanim_dict['hebDateString']).group(0)
    year_day = re.findall(r'\d+', zmanim_dict['hebDateString'])
    zmanim_dict = zmanim_dict['zmanim']
    zmanim_dict['day'] = year_day[0]
    zmanim_dict['month'] = month
    zmanim_dict['year'] = year_day[1]
    if zmanim_dict['chatzos'] == 'X:XX:XX':
        zmanim_str = l.Zmanim.get_polar_error(lang)
        return zmanim_str

    d1 = datetime.strptime(zmanim_dict['sof_zman_shema_gra'], "%H:%M:%S")
    d2 = datetime.strptime(zmanim_dict['sof_zman_tefila_gra'], "%H:%M:%S")

    if zmanim_dict['alos_ma'] == 'X:XX:XX':
        zmanim_dict['alos_ma'] = str(datetime.time(datetime.strptime(
            zmanim_dict['chatzos'],
            "%H:%M:%S") - timedelta(hours=12)))
        if zmanim_dict['talis_ma'] == 'X:XX:XX':
            zmanim_dict['talis_ma'] = str(datetime.time(datetime.strptime(
                zmanim_dict['zmanim']['chatzos'],
                "%H:%M:%S") - timedelta(hours=12)))
    if zmanim_dict['tzeis_595_degrees'] == 'X:XX:XX':
        zmanim_dict['tzeis_595_degrees'] = None
    if zmanim_dict['tzeis_850_degrees'] == 'X:XX:XX':
        zmanim_dict['tzeis_850_degrees'] = None
    if zmanim_dict['sof_zman_shema_ma'] == 'X:XX:XX' or \
       zmanim_dict['sof_zman_tefila_ma'] == 'X:XX:XX':
        zmanim_dict['sof_zman_shema_ma'] = None
        zmanim_dict['sof_zman_tefila_ma'] = None
        zmanim_dict['ma_hour'] = None
    else:
        d1 = datetime.strptime(zmanim_dict['sof_zman_shema_ma'], "%H:%M:%S")
        d2 = datetime.strptime(zmanim_dict['sof_zman_tefila_ma'], "%H:%M:%S")
        zmanim_dict['ma_hour'] = str(d2 - d1)

    zmanim_dict['chazot_laila'] = str(datetime.time(datetime.strptime(
        zmanim_dict['chatzos'], "%H:%M:%S") + timedelta(hours=12)))
    zmanim_dict['gra_hour'] = str(d2 - d1)
    zmanim_str = l.Zmanim.get_extended_zmanim(lang, zmanim_dict)

    return zmanim_str


if __name__ == '__main__':
    pass
