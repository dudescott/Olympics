def spec_athlete(c):
    athlete = input('Enter athlete name (partial name for search): ')
    if athlete == '':
        return
    c.execute('select distinct name from athlete where name like ?', ('%' + athlete + '%',))
    athletes = [athlete[0] for athlete in c.fetchall()]
    athlete_cnt = len(athletes)
    if athlete_cnt > 20:
        print('Error: too many resulting athletes. Please be more specific.')
        spec_athlete(c)
    elif athlete_cnt == 0:
        print('No result found')
    elif athlete_cnt > 1:
        print('Please input the athlete index or name from the below list of athletes')
        for i, athlete in enumerate(athletes):
            print(f'{i+1}.\t{athlete}')
        athlete = input('Enter athlete index or name: ')
        try:
            athlete = int(athlete)
            if athlete > len(athletes) or athlete < 1:
                print('Invalid input!')
                return
            athlete = athletes[athlete - 1]
        except:
            if athlete not in athlete:
                print('Invalid input!')
                return
        
        c.execute("select * from athlete where name like ?", ('%' + athlete + '%',))
        print(c.fetchall())
        
    print(athletes)


def spec_country(c):
    pass

def medal_athlete(c):
    pass

def medal_country(c):
    pass