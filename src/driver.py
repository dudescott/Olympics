import os
import sqlite3 as sql
import pandas as pd
import queries
import warnings
warnings.filterwarnings("ignore") # turn off warning due to spaces in pandas df headers in to_sql

def create_db():
    conn = sql.connect('../data/olympics.db')
    df_athletes = pd.read_csv('../data/athlete_events.csv')
    df_noc = pd.read_csv('../data/noc_regions.csv')
    df_population = pd.read_csv('../data/population.csv')
    df_gdp = pd.read_csv('../data/gdp.csv')
    df_gdp.drop(df_gdp[['INDICATOR','SUBJECT','MEASURE','FREQUENCY','Flag Codes']], axis=1, inplace=True)
    df_gdp.rename(columns={'Location': 'Location', 'TIME': 'Year','Value': 'GDP'}, inplace=True)

    df_athletes.to_sql('athlete', con=conn, if_exists='append')
    df_noc.to_sql('noc', con=conn, if_exists='append')
    df_population.to_sql('population', con=conn, if_exists='append')
    df_gdp.to_sql('gdp', con=conn, if_exists='append')
    conn.commit()
    conn.close()


def run_driver():
    os.system('cls||clear')
    conn = sql.connect('../data/olympics.db')
    c = conn.cursor()
    option = ''
    while option != 'q':
        option = input('Choose from the below menu:\n' \
            + '  (1) Search a specific althete\n' \
            + '  (2) Search a specific country\n' \
            + '  (3) Show top medaling athletes\n' \
            + '  (4) Show top medaling countries\n' \
            + '  (0) Exit\n'\
            + 'Option: '
            )
        try:
            option = int(option)
        except:
            print('Invalid Input!')
        
        os.system('cls||clear')
        if option == 0:
            return
        elif option == 1:
            queries.spec_athlete(c)
        elif option == 2:
            queries.spec_country(c)
        elif option == 3:
            queries.medal_athlete(c)
        elif option == 4:
            queries.medal_country(c)
        else:
            print('Invalid Input!')

if __name__ == '__main__':
    if not os.path.exists('../data/olympics.db'):
        create_db()
    run_driver()