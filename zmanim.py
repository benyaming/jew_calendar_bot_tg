# -*- coding: utf-8
from enum import Enum
from datetime import datetime, timedelta
from pyluach import dates
from pyluach.hebrewcal import Month

import re
import pytz, requests
import db_operations, data
from picture_maker import ZmanimSender

import localization

URL = 'http://db.ou.org/zmanim/getCalendarData.php'


class ZmanimList(Enum):
    alot_ma = 0
    talis_ma = 1
    sunrise = 2
    sof_zman_shema_ma = 3
    sof_zman_shema_gra = 4
    sof_zman_tefila_ma = 5
    sof_zman_tefila_gra = 6
    chatzos = 7
    mincha_gedola_ma = 8
    mincha_ketana_gra = 9
    plag_mincha = 10
    sunset = 11
    tzeis_595d = 12
    tzeis_850d = 13
    tzeis_42m = 14
    tzeis_rt = 15
    astronomical_hour_ma = 16
    astronomical_hour_gra = 17
    chatzos_laila = 18


def get_alot_ma(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['alos_ma'] == 'X:XX:XX':
        chazot = datetime.strptime(zmanim_dict['chatzos'], "%H:%M:%S")
        delta = timedelta(hours=12)
        zmanim_dict['alos_ma'] = str(datetime.time(chazot - delta))
    return zmanim_dict['alos_ma']


def get_talis_ma(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['talis_ma'] == 'X:XX:XX':
        chazot = datetime.strptime(zmanim_dict['chatzos'], "%H:%M:%S")
        delta = timedelta(hours=12)
        zmanim_dict['talis_ma'] = str(datetime.time(chazot - delta))
    return zmanim_dict['talis_ma']


def get_sunrise(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['sunrise']


def get_sof_zman_shema_ma(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['sof_zman_shema_ma'] == 'X:XX:XX':
        zmanim_dict['sof_zman_shema_ma'] = None
    return zmanim_dict['sof_zman_shema_ma']


def get_sof_zman_tefila_ma(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['sof_zman_tefila_ma'] == 'X:XX:XX':
        zmanim_dict['sof_zman_tefila_ma'] = None
    return zmanim_dict['sof_zman_tefila_ma']


def get_sof_zman_shema_gra(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['sof_zman_shema_gra']


def get_sof_zman_tefila_gra(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['sof_zman_tefila_gra']


def get_chatzos(zmanim_dict: dict, lang: str)-> str:
    if zmanim_dict['chatzos'] == 'X:XX:XX':
        zmanim_dict['chatzos'] = localization.Zmanim.get_polar_error(lang)
    return zmanim_dict['chatzos']


def get_mincha_gedola_ma(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['mincha_gedola_ma']


def get_mincha_ketana_gra(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['mincha_ketana_gra']


def get_plag_mincha_ma(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['plag_mincha_ma']


def get_sunset(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['sunset']


def get_tzeis_595_degrees(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['tzeis_595_degrees'] == 'X:XX:XX':
        zmanim_dict['tzeis_595_degrees'] = None
    return zmanim_dict['tzeis_595_degrees']


def get_tzeis_850_degrees(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['tzeis_850_degrees'] == 'X:XX:XX':
        zmanim_dict['tzeis_850_degrees'] = None
    return zmanim_dict['tzeis_850_degrees']


def get_tzeis_42_minutes(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['tzeis_42_minutes']


def get_tzeis_72_minutes(zmanim_dict: dict, lang: str) -> str:
    return zmanim_dict['tzeis_72_minutes']


def get_astronomical_hour_ma(zmanim_dict: dict, lang: str) -> str:
    if zmanim_dict['sof_zman_shema_ma'] != 'X:XX:XX' and \
            zmanim_dict['sof_zman_tefila_ma'] != 'X:XX:XX':
        begin_hour_ma = datetime.strptime(
            zmanim_dict['sof_zman_shema_ma'],
            "%H:%M:%S"
        )
        end_hour_ma = datetime.strptime(
            zmanim_dict['sof_zman_tefila_ma'],
            "%H:%M:%S"
        )
        astronomical_hour_ma = str(end_hour_ma - begin_hour_ma)

    else:
        astronomical_hour_ma = None
    return astronomical_hour_ma


def get_astronomical_hour_gra(zmanim_dict: dict, lang: str) -> str:
    begin_hour_gra = datetime.strptime(
        zmanim_dict['sof_zman_shema_gra'],
        "%H:%M:%S"
    )
    end_hour_gra = datetime.strptime(
        zmanim_dict['sof_zman_tefila_gra'],
        "%H:%M:%S"
    )
    astronomical_hour_gra = str(end_hour_gra - begin_hour_gra)
    return astronomical_hour_gra


def get_chazos_laila(zmanim_dict: dict, lang: str) -> str:
    chazot = datetime.strptime(zmanim_dict['chatzos'], "%H:%M:%S")
    delta = timedelta(hours=12)
    chazot_laila = str(datetime.time(chazot + delta))
    return chazot_laila


def collect_custom_zmanim(
        zmanim_dict: dict,
        user_zmanim_set: str,
        lang: str
) -> str:
    zmanim_funcs = {
        'alot_ma': get_alot_ma,
        'talis_ma': get_talis_ma,
        'sunrise': get_sunrise,
        'sof_zman_shema_ma': get_sof_zman_shema_ma,
        'sof_zman_shema_gra': get_sof_zman_shema_gra,
        'sof_zman_tefila_ma': get_sof_zman_tefila_ma,
        'sof_zman_tefila_gra': get_sof_zman_tefila_gra,
        'chatzos': get_chatzos,
        'mincha_gedola_ma': get_mincha_gedola_ma,
        'mincha_ketana_gra': get_mincha_ketana_gra,
        'plag_mincha': get_plag_mincha_ma,
        'sunset': get_sunset,
        'tzeis_595d': get_tzeis_595_degrees,
        'tzeis_850d': get_tzeis_850_degrees,
        'tzeis_42m': get_tzeis_42_minutes,
        'tzeis_rt': get_tzeis_72_minutes,
        'astronomical_hour_ma': get_astronomical_hour_ma,
        'astronomical_hour_gra': get_astronomical_hour_gra,
        'chatzos_laila': get_chazos_laila
    }
    user_zmanim_str = ''
    user_zmanim = user_zmanim_set
    first_zman_flag = True
    for i in range(len(user_zmanim)):
        zman = int(user_zmanim[i])
        if zman:
            zman_code = ZmanimList(i).name
            func = zmanim_funcs.get(zman_code, '')
            zman_names = {
                'Russian': data.zmanim_ru[zman_code],
                'English': data.zmanim_en[zman_code],
                'Hebrew': data.zmanim_he[zman_code]
            }
            zman_name = zman_names.get(lang,'')
            zman_string = f'{zman_name} —{func(zmanim_dict, lang)[:-3]}'
            if first_zman_flag:
                user_zmanim_str += f'{zman_string}'
                first_zman_flag = False
            else:
                user_zmanim_str += f'\n{zman_string}'
    return user_zmanim_str


def get_zmanim_dict(user: int, custom_date=None) -> dict:
    tz = db_operations.get_tz_by_id(user)
    loc = db_operations.get_location_by_id(user)
    if custom_date:
        custom_year = custom_date[0]
        custom_month = custom_date[1]
        custom_day = custom_date[2]
        if len(str(custom_year)) == 2:
            custom_year = f'00{custom_year}'
        elif len(str(custom_year)) == 3:
            custom_year = f'0{custom_year}'
        date_str = f'{custom_month}/{custom_day}/{custom_year}'
    else:
        tz_time = pytz.timezone(tz)
        now = datetime.now(tz_time)
        date_str = f'{now.month}/{now.day}/{now.year}'
    params = {
        'mode': 'day',
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
    return zmanim_dict


def get_date(user_id, lang: str, cusom_date=None) -> str:
    if not cusom_date:
        tz = db_operations.get_tz_by_id(user_id)
        tz_time = pytz.timezone(tz)
        now = datetime.now(tz_time)
    else:
        now = datetime(*cusom_date)
    gr_months_dict = {
        'Russian': data.gr_months_index[now.month],
        'English': data.gr_months_index_en[now.month],
        # todo hebrew
    }
    month = gr_months_dict.get(lang)
    greg_date_tuple = (
        now.timetuple()[0],
        now.timetuple()[1],
        now.timetuple()[2]
    )
    greg_date = f'{now.day} {month} {now.year}'

    heb_date = dates.GregorianDate(*greg_date_tuple).to_heb().tuple()
    heb_month_name = Month(heb_date[0], heb_date[1]).name
    he_months_dict = {
        'Russian': data.jewish_months_a[heb_month_name],
        'English': heb_month_name,
        # todo hebrew
    }
    heb_month = he_months_dict.get(lang)
    heb_date_str = f'{heb_date[2]} {heb_month} {heb_date[0]}'
    date = f'{greg_date}/{heb_date_str}'
    return date


def get_zmanim(user_id: int, lang: str, custom_date=None) -> dict:
    response = {'polar_error': False, 'zmanim_set_error': False}
    zmanim_dict = get_zmanim_dict(user_id, custom_date)
    if zmanim_dict['chatzos'] == 'X:XX:XX':
        response['polar_error'] = localization.Zmanim.get_polar_error(lang)
    else:
        user_zmanim_set = db_operations.get_zmanim_set(user_id)
        user_zmanim_str = collect_custom_zmanim(
            zmanim_dict,
            user_zmanim_set,
            lang
        )
        # check if user have enabled zmanim
        if user_zmanim_str:
            date = get_date(user_id, lang, custom_date)
            response['zmanim_pic'] = ZmanimSender(lang).get_zmanim_picture(
                date,
                user_zmanim_str
            )
        else:
            response['zmanim_set_error'] = \
                localization.Zmanim.get_zmanim_set_error(lang)
    return response
