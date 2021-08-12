import os

def spec_athlete(c):
    athlete = input('Enter athlete name (partial name for search): ')
    if athlete == '':
        return
    c.execute('select distinct name, sport from athlete where name like ?', ('%' + athlete + '%',))
    athletes = c.fetchall()
    athlete_cnt = len(athletes)
    if athlete_cnt > 20:
        print('Error: too many resulting athletes. Please be more specific.')
        spec_athlete(c)
    elif athlete_cnt == 0:
        print('No result found')
        return
    elif athlete_cnt > 1:
        os.system('cls||clear')
        print('Please input the athlete index or name from the below list of athletes')
        for i, athlete in enumerate(athletes):
            print(f'{i+1}.\t{athlete[0]} ({athlete[1]})')
        athlete = input('Enter athlete index or name: ')
        try:
            athlete = int(athlete)
            if athlete > len(athletes) or athlete < 1:
                print('Invalid input!')
                return
            athlete = athletes[athlete - 1][0]
        except:
            if athlete not in [a[0] for a in athletes]:
                print('Invalid input!')
                return
    athlete = '%' + athlete + '%'
    c.execute("""
        select name, sport, event, avg(height), avg(weight), gold, silver, bronze, non_medal
        from (
            select name, sport, event, height, weight, gold, silver, bronze, non_medal
            from (
                (
                    -- average weight and height
                    select name, sport, event, avg(height) height, avg(weight) weight
                    from athlete
                    where name like ?
                    group by name, sport, event
                ) stats
                left outer join
                (
                    select g_name, g_event, gold, silver, bronze, non_medal
                    from (
                            (
                                (
                                    (
                                        -- gold medals
                                        select name g_name, event g_event, count(medal) gold
                                        from athlete
                                        where medal == 'Gold' and name like ?
                                        group by name, event
                                    ) gold
                                    left outer join
                                    (    
                                        -- silver medals
                                        select name s_name, event s_event, count(medal) silver
                                        from athlete
                                        where medal == 'Silver' and name like ?
                                        group by name, event
                                    ) silver
                                    on gold.g_name = silver.s_name and gold.g_event = silver.s_event
                                ) medals_temp
                                left outer join
                                (
                                    -- bronze medals
                                    select name b_name, event b_event, count(medal) bronze
                                    from athlete
                                    where medal == 'Bronze' and name like ?
                                    group by name, event
                                ) bronze
                                on medals_temp.g_name = bronze.b_name and medals_temp.g_event = bronze.b_event
                            ) medals_temp
                            left outer join
                            (
                                -- non medals
                                select name n_name, event n_event, count(name) non_medal
                                from athlete
                                where medal is null and name like ?
                                group by name, event
                            ) non_medal
                            on medals_temp.g_name = non_medal.n_name and medals_temp.g_event = non_medal.n_event
                        )
                )medals 
                on medals.g_name = stats.name and medals.g_event = stats.event
            )
        )
        group by name, sport, event, gold, silver, bronze, non_medal
        """,(athlete, athlete, athlete, athlete, athlete))
    stats = c.fetchall()
    name = stats[0][0]
    sport = stats[0][1]
    weight = height = gold = silver = bronze = non_medal = 0
    max_event_len = 0
    for stat in stats:
        max_event_len = len(stat[2]) if len(stat[2]) > max_event_len else max_event_len
        weight += stat[3]
        height += stat[4]
        gold += 0 if stat[5] == None else stat[5]
        silver += 0 if stat[6] == None else stat[6]
        bronze += 0 if stat[7] == None else stat[7]
        non_medal += 0 if stat[8] == None else stat[8]

    weight /= len(stats)
    height /= len(stats)

    os.system('cls||clear')
    print('Athlete\n' + '-'*30)
    print(f'Name:\t\t{name}')
    print(f'Sport:\t\t{sport}')
    print(f'Avg. Weight:\t{weight}')
    print(f'Avg. Height:\t{height}')
    print(f'Gold:\t\t{gold}')
    print(f'Silver:\t\t{silver}')
    print(f'Bronze:\t\t{bronze}')
    print(f'Medals:\t\t{gold + silver + bronze}')
    print(f'Non-Medals:\t{non_medal}')
    print(f'Events:\t\t{gold + silver + bronze + non_medal}')
    response = input('\n\nShow more information? (Y/n) ')

    if response.lower() != 'n':
        print('\nEvent' + ' ' * (max_event_len - 5) + '\t', end='')
        print('Gold\tSilver\tBronze\tMedals\tNon-Medals  Events\n' + '-'*100)
        for stat in stats:
            e_gold = 0 if stat[5] == None else stat[5]
            e_silver = 0 if stat[6] == None else stat[6]
            e_bronze = 0 if stat[7] == None else stat[7]
            e_non_medal = 0 if stat[8] == None else stat[8]
            print(f'{stat[2]}', end='')
            print(' '* (max_event_len - len(stat[2])) + '\t',end='')
            print(f'{e_gold}\t{e_silver}\t{e_bronze}\t{e_gold + e_silver + e_bronze}\t{e_non_medal}\t    {e_gold + e_silver + e_bronze+e_non_medal}')
        print(f'Total', end='')
        print(' '* (max_event_len - 5) + '\t',end='')
        print(f'{gold}\t{silver}\t{bronze}\t{gold + silver + bronze}\t{non_medal}\t    {gold + silver + bronze+non_medal}')
        input()

    os.system('cls||clear')

def spec_country(c):
    country = input('Enter country name (partial name for search): ')
    if country == '':
        return
    c.execute('select distinct noc, region from noc where noc like ? or region like ?', ('%' + country + '%','%' + country + '%'))
    countries = c.fetchall()
    country_cnt = len(countries)
    if country_cnt > 20:
        print('Error: too many resulting countries. Please be more specific.')
        spec_athlete(c)
    elif country_cnt == 0:
        print('No result found')
        return
    elif country_cnt > 1:
        os.system('cls||clear')
        print('Please input the country index or name from the below list of countries')
        for i, country in enumerate(countries):
            print(f'{i+1}.\t{country[0]} ({country[1]})')
        country = input('Enter country index or name: ')
        try:
            country = int(country)
            if country > len(countries) or country < 1:
                print('Invalid input!')
                return
            country = countries[country - 1][0]
        except:
            if country not in countries:
                print('Invalid input!')
                return
    c.execute('select distinct noc from noc where region like ?', ('%' + country + '%',))
    noc = c.fetchone()[0]
    c.execute("""
        select g_noc noc, g_sport sport, gold, silver, bronze, non_medal
        from (
                (
                    (
                        (
                            -- gold medals
                            select noc g_noc, sport g_sport, count(medal) gold
                            from athlete
                            where medal == 'Gold' and noc like ?
                            group by sport, sport
                        ) gold
                        left outer join
                        (    
                            -- silver medals
                            select noc s_noc, sport s_sport, count(medal) silver
                            from athlete
                            where medal == 'Silver' and noc like ?
                            group by noc, sport
                        ) silver
                        on gold.g_noc = silver.s_noc and gold.g_sport = silver.s_sport
                    ) medals_temp
                    left outer join
                    (
                        -- bronze medals
                        select noc b_noc, sport b_sport, count(medal) bronze
                        from athlete
                        where medal == 'Bronze' and noc like ?
                        group by noc, sport
                    ) bronze
                    on medals_temp.g_noc = bronze.b_noc and medals_temp.g_sport = bronze.b_sport
                ) medals_temp
                left outer join
                (
                    -- non medals
                    select noc n_noc, sport n_sport, count(noc) non_medal
                    from athlete
                    where medal is null and noc like ?
                    group by noc, sport
                ) non_medal
                on medals_temp.g_noc = non_medal.n_noc and medals_temp.g_sport = non_medal.n_sport
        )
    group by noc, sport
    """,(noc, noc, noc, noc))
    print(c.fetchall())
        
def medal_athlete(c):
    pass

def medal_country(c):
    pass    