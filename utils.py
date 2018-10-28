# -*- coding: utf-8
import requests


def get_tz_by_location(loc):
    url = f'http://api.geonames.org/timezoneJSON'
    params = {
        'username': 'arlas',
        'lat': loc[0],
        'lng': loc[1]
    }
    tz_data = requests.get(url, params=params).json()
    tz = tz_data.get('timezoneId', '')
    return tz


if __name__ == '__main__':
    pass
