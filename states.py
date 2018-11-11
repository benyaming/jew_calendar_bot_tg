import psycopg2

import settings

from utils import get_tz_by_location
from utils import log


def check_state(user: int) -> dict:
    log(f'Database\tcheck_state\tSTART\t{user}')
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        check_query = f'SELECT state FROM states ' \
                      f'WHERE states.user_id = {user}'
        cur.execute(check_query)
        user_has_state = cur.fetchone()
        state_dict = {
            'ok': False
        }
        if user_has_state:
            state_dict = {
                'ok': True,
                'state': user_has_state[0]
            }
        log(f'Database\tcheck_state\tEND\t{user}')
        return state_dict


def set_state(user: int, state: str) -> None:
    log(f'Database\tset_state\tSTART\t{user}')
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        check_query = f'SELECT * FROM states WHERE user_id = {user}'
        cur.execute(check_query)
        user_in_db = cur.fetchone()
        if not user_in_db:
            set_time_query = f'INSERT INTO states ' \
                             f'VALUES ({user}, \'{state}\')'
            cur.execute(set_time_query)
            conn.commit()
        log(f'Database\tset_state\tEND\t{user}')


def delete_state(user: int) -> None:
    log(f'Database\tdelete_state\tSTART\t{user}')
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        delete_time_query = f'DELETE FROM states WHERE states.user_id = {user}'
        cur.execute(delete_time_query)
        conn.commit()
    log(f'Database\tdelete_state\tEND\t{user}')