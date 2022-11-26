#!/bin/env python3
from psycopg2 import connect
from sys import argv
import random
from datetime import datetime as dt
from psycopg2.errors import DataException

def generate_sql_for_availability():
    startdate_lower = dt(2022,11,26)
    startdate_upper = dt(2024,1,1)
    startdate_timestamp = random.randint(startdate_lower.timestamp(), startdate_upper.timestamp())
    duration = random.randint(1, 12*60*60)
    enddate_timestamp = startdate_timestamp + duration

    artist_id = random.randint(1,4)
   
    sql_template = """
        INSERT INTO artist_available VALUES (
            DEFAULT,
            %(artist_id)s,
            tstzrange(%(startdate)s, %(enddate)s)
            )
        ON CONFLICT DO NOTHING
    """
    return (sql_template, dict(
        artist_id=artist_id,
        startdate=dt.fromtimestamp(startdate_timestamp),
        enddate=dt.fromtimestamp(enddate_timestamp)
        )
    )


def make_records(howmany):
    with connect('postgresql:///boyband') as conn:
        cur = conn.cursor()
        for i in range(howmany):
            template, arguments = generate_sql_for_availability()
            try:
                cur.execute(template, arguments)
                conn.commit()
            except DataException:
                print(template, arguments)
                raise

if __name__ == '__main__':
    try:
        make_records(int(argv[1]))
    except (ValueError, IndexError):
        exit(f'Wrong invocation.\nUsage: "{argv[0]} number-of-records" where number-of-records is a positive integer.\nBye bye.')
