import requests

import pytz

from datetime import datetime, timedelta

import utils as f
import localization as l


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_next_weekday(startdate, weekday):
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return (d + t).strftime('%Y-%m-%d')


def get_shabbos_string(loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    date_str = f'{now.year}-{now.month}-{now.day}'
    shabbat_date = get_next_weekday(date_str, 5)
    month = shabbat_date[5:7:]
    day = shabbat_date[8::]
    year = shabbat_date[:4:]
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': f'{month}/{day}/{year}',
        'lat': loc[0],
        'lng': loc[1]
    }
    shabbat = requests.get(URL, params=params)
    shabbat_dict = shabbat.json()

    if shabbat_dict['zmanim']['sunset'] == 'X:XX:XX':
        shabbat_str = l.Shabos.shabos_with_latitude_error(
            lang,
            shabbat_dict['parsha_shabbos']
        )
        return shabbat_str

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
        shabbat_str = l.Shabos.shabos_with_warning(
            lang,
            shabbat_dict['parsha_shabbos'],
            shabbat_dict['candle_lighting_shabbos'][:-3:],
            shabbat_dict['zmanim']['tzeis_850_degrees'][:-3]
        )
    else:
        shabbat_str = l.Shabos.shabos(
            lang,
            shabbat_dict['parsha_shabbos'],
            shabbat_dict['candle_lighting_shabbos'][:-3:],
            shabbat_dict['zmanim']['tzeis_850_degrees'][:-3]
        )

    if tz in ['Asia/Jerusalem', 'Asia/Tel_Aviv', 'Asia/Hebron']:
        sunset = datetime.strptime(shabbat_dict['zmanim']['sunset'],
                                   "%H:%M:%S")
        delta_18 = timedelta(minutes=18)
        delta_30 = timedelta(minutes=30)
        delta_40 = timedelta(minutes=40)
        candle_18 = str(datetime.time(sunset - delta_18))
        candle_30 = str(datetime.time(sunset - delta_30))
        candle_40 = str(datetime.time(sunset - delta_40))
        shabbat_str = l.Shabos.shabos_in_israel(
            lang,
            shabbat_dict['parsha_shabbos'],
            candle_18[:-3],
            candle_30[:-3],
            candle_40[:-3],
            shabbat_dict['zmanim']['tzeis_850_degrees'][:-3]
        )
    response = shabbat_str
    return response

if __name__ == '__main__':
    pass
