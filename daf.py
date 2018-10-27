import requests
import pytz
import localization
import utils as f
from datetime import datetime


URL = 'http://db.ou.org/zmanim/getCalendarData.php'


def get_daf(loc, lang):
    tz = f.get_tz_by_location(loc)
    tz_time = pytz.timezone(tz)
    now = datetime.now(tz_time)
    params = {'mode': 'day',
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
    return daf_str
