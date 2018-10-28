import psycopg2

import settings

 
def check_state(user: int) -> dict:
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
        return state_dict


def set_state(user: int, state: str) -> None:
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


def delete_state(user: int) -> None:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        delete_time_query = f'DELETE FROM states WHERE states.user_id = {user}'
        cur.execute(delete_time_query)
        conn.commit()
