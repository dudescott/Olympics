import os
import sqlite3 as sql
import pandas as pd


def create_db():
    conn = sql.connect('./data/olympics.db')
    df = pd.read_csv('data/athlete_events.csv')
    df.to_sql('athlete', con=conn, if_exists='append')
    df = pd.read_csv('data/noc_regions.csv')
    df.to_sql('noc', con=conn, if_exists='append')
    conn.commit()
    conn.close()


def run_driver():
    


if __name__ == '__main__':
    if not os.path.exists('data/olympics.db'):
        create_db()
    run_driver()