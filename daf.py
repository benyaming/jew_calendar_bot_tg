from io import BytesIO
from datetime import datetime

import requests
import pytz

import utils
import db_operations
import localization
from picture_maker import DafYomiSender


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_daf(user_id: int, lang: str) -> BytesIO:
    loc = db_operations.get_location_by_id(user_id)
    tz = utils.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    params = {
        'mode': 'day',
        'timezone': tz,
        'dateBegin': f'{now.month}/{now.day}/{now.year}',
        'lat': loc[0],
        'lng': loc[1]
    }
    daf = requests.get(URL, params=params)
    daf_dict = daf.json()
    daf_str = localization.DafYomi.get_str(
        lang,
        daf_dict["dafYomi"]["masechta"],
        daf_dict["dafYomi"]["daf"]
    )
    daf_pic = DafYomiSender(lang).get_daf_picture(daf_str)
    return daf_pic
