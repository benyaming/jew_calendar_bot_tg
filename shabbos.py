from datetime import datetime, timedelta
from io import BytesIO

import requests
import pytz

import localization
import db_operations
import utils
from picture_maker import ShabbosSender


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_next_weekday(startdate, weekday):
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return (d + t).strftime('%Y-%m-%d')


def get_shabbos(lang, user) -> BytesIO:
    loc = db_operations.get_location_by_id(user)
    tz = utils.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    date_str = f'{now.year}-{now.month}-{now.day}'
    shabbat_date = get_next_weekday(date_str, 5)
    month = shabbat_date[5:7:]
    day = shabbat_date[8::]
    year = shabbat_date[:4:]
    diaspora = db_operations.get_diaspora_status(user)
    candle_offset = db_operations.get_candle_offset(user)
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': f'{month}/{day}/{year}',
        'lat': loc[0],
        'lng': loc[1],
        'candles_offset': candle_offset
    }
    if not diaspora:
        params['israel_holidays'] = True
    shabbat = requests.get(URL, params=params)
    shabbat_dict = shabbat.json()
    if shabbat_dict['zmanim']['sunset'] == 'X:XX:XX':
        shabbat_str = localization.Shabos.shabos_with_latitude_error(
            lang,
            shabbat_dict['parsha_shabbos']
        )
    else:
        if shabbat_dict['zmanim']['tzeis_850_degrees'] == 'X:XX:XX':
            # высчитываем полночь, прибавляя 12 часов
            chazot_time = datetime.strptime(
                shabbat_dict['zmanim']['chatzos'],
                "%H:%M:%S"
            )
            chazot_delta = timedelta(hours=12)
            chazot_laila = str(datetime.time(chazot_time + chazot_delta))
            shabbat_dict['zmanim']['tzeis_850_degrees'] = chazot_laila

        if shabbat_dict['zmanim']['alos_ma'] == 'X:XX:XX':
            shabbat_str = localization.Shabos.shabos_with_warning(
                lang,
                shabbat_dict['parsha_shabbos'],
                shabbat_dict['candle_lighting_shabbos'][:-3:],
                shabbat_dict['zmanim']['tzeis_850_degrees'][:-3],
                candle_offset
            )
        else:
            shabbat_str = localization.Shabos.shabos(
                lang,
                shabbat_dict['parsha_shabbos'],
                shabbat_dict['candle_lighting_shabbos'][:-3:],
                shabbat_dict['zmanim']['tzeis_850_degrees'][:-3],
                candle_offset
            )
    response_pic = ShabbosSender(lang).get_shabbos_picture(shabbat_str)
    return response_pic
