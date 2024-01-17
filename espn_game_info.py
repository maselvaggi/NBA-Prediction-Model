#%%
import requests
import os.path
import pandas as pd
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

#%% Get all game IDs for 2022-2023 regular season
#   Create .txt to save game IDs so no need to rerun    
def update_espn_game_info(year, get_all_espn_game_info):
    '''
    There are 1230 games in a NBA regular season. Each game ID corresponds
    to a regular season game on ESPN.go.com.  The range of game ids from the
    first to last game of the regular season is larger than 1230.  So we 
    need to figure out which game ids are valid-  this function checks the 
    validity by way of comparing request status codes.

    2023 Game ID range: 401468016 - 401469385
    2024 Game ID range: 401584689 - 401585828
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.111 Safari/537.36'}

    link = 'https://www.espn.com/nba/game/_/gameId/'
    if type(year) != int:
        raise ValueError("Please enter input in the form of an integer.")
    elif type(get_all_espn_game_info) is not bool:
        raise ValueError('Please enter boolean value for this variable.')
    elif year == 2023:
        message = get_2023_game_ids(link, headers, get_all_espn_game_info)
        return message
    elif year == 2024:
        message = get_2024_game_ids(link, headers, get_all_espn_game_info)
        return message
    elif year == 0:
        return "ESPN game information will not be updated."
    else:
        return 'This data is not available yet.' 


def get_2023_game_ids(link, headers, get_all_espn_game_info):
    new_game_info = []
    if get_all_espn_game_info is False and os.path.exists('output/2023/ESPN_game_info2023.csv') is True:
        collected_game_ids = pd.read_csv('output/2023/ESPN_game_info2023.csv')
        max_game_id = collected_game_ids['Game ID'].max()

        if max_game_id != 401469385:
            for game in range(max_game_id+1, 401469385+1):
                if game != 401468924:
                    url = ''.join([link, str(game)])
                    record = requests.get(url, headers = headers)
                    if record.status_code == 200:
                        new_game_info.append(get_game_info(game)) 
                else:
                    game = 401526670 #WSH and DET had a game postponed, this is the new game ID. 
                    url = ''.join([link, str(game)])
                    record = requests.get(url, headers = headers)
                    if record.status_code == 200:
                        new_game_info.append(get_game_info(game))
        else:
            return "There is no 2023 game information to collect. The file is up to date."

        new_game_info = pd.DataFrame(new_game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'O/U','Attendance', 'Capacity', 'Game ID'], index = None)
        new_game_info = new_game_info.replace('WSH', 'WAS').replace('SA','SAS').replace('SA<','SAS').replace('NY','NYK').replace('NY<','NYK').replace('NO','NOP').replace('NO<','NOP').replace('GS','GSW').replace('GS<','GSW').replace('UTAH','UTA')
        all_game_info = pd.concat([collected_game_ids, new_game_info], ignore_index=True, sort = False)
        all_game_info = all_game_info.drop_duplicates()
        all_game_info.to_csv('output/2023/ESPN_game_info2023.csv')  
        entries_added = len(all_game_info) - len(collected_game_ids)
        return "All available 2023 game info was collected. \n {num} entries were collected.".format(num = entries_added)
    else:
        for game in tqdm(range(401468016, 401469385+1)):
            if game == 401468924:
                game = 401526670 #WSH and DET had a game postponed, this is the new game ID.

            url = ''.join([link, str(game)])
            record = requests.get(url, headers = headers)
            if record.status_code == 200:
                new_game_info.append(get_game_info(game))

        new_game_info = pd.DataFrame(new_game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'O/U','Attendance', 'Capacity', 'Game ID'], index = None)
        new_game_info = new_game_info.replace('WSH', 'WAS').replace('SA','SAS').replace('SA<','SAS').replace('NY','NYK').replace('NY<','NYK').replace('NO','NOP').replace('NO<','NOP').replace('GS','GSW').replace('GS<','GSW').replace('UTAH','UTA')
        new_game_info.to_csv('output/2023/ESPN_game_info2023.csv') 

        return "All available 2023 game information was collected.\n{num} entries were collected".format(num = len(new_game_info))   

def get_2024_game_ids(link, headers, get_all_espn_game_info):
    new_game_info = []
    if get_all_espn_game_info is False and os.path.exists('output/2024/ESPN_game_info2024.csv') is True:
        collected_game_ids = pd.read_csv('output/2024/ESPN_game_info2024.csv')
        max_game_id = collected_game_ids['Game ID'].max()

        if max_game_id != 401469385:
            for game in range(max_game_id+1, 401469385+1):
                url = ''.join([link, str(game)])
                record = requests.get(url, headers = headers)
                if record.status_code == 200:
                    try:
                        new_game_info.append(get_game_info(game))
                    except IndexError:
                        entries_added = (game-1) - max_game_id
                        if entries_added > 1:
                            print('There was information gathered for {num} games.'.format(num = entries_added))
                        elif entries_added == 1:
                            print('There was information gathered for 1 game.')
                        else:
                            return "There is no 2024 game information to collect. The file is up to date."
                        break
            if len(new_game_info) > 0:
                new_game_info = pd.DataFrame(new_game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'O/U','Attendance', 'Capacity', 'Game ID'], index = None)
                new_game_info = new_game_info.replace('WSH', 'WAS').replace('SA','SAS').replace('SA<','SAS').replace('NY','NYK').replace('NY<','NYK').replace('NO','NOP').replace('NO<','NOP').replace('GS','GSW').replace('GS<','GSW').replace('UTAH','UTA')
                all_game_info = pd.concat([collected_game_ids, new_game_info], ignore_index=True, sort = False)
                all_game_info = all_game_info.drop_duplicates()
                all_game_info.to_csv('output/2024/ESPN_game_info2024.csv')  
                entries_added = len(all_game_info) - len(collected_game_ids)

                return all_game_info, "All available game info was collected.\n{num} entries were collected.".format(num = entries_added)

        else:
            return [], "No game to add to the 2024 season schedule."
    else:
        for game in tqdm(range(401584689, 401585828+1)):
            url = ''.join([link, str(game)])
            record = requests.get(url, headers = headers)
            if record.status_code == 200:
                try:
                    new_game_info.append(get_game_info(game))
                except IndexError:
                    entries_added = (game-1) - max_game_id
                    if entries_added > 1:
                        print('There was information gathered for {num} games.'.format(num = entries_added))
                    elif entries_added == 1:
                        print('There was information gathered for 1 game.')
                    else:
                        return [], "There was no game information collected. The file is up to date."
                    break

        new_game_info = pd.DataFrame(new_game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'O/U','Attendance', 'Capacity', 'Game ID'], index = None)
        new_game_info = new_game_info.replace('WSH', 'WAS').replace('SA','SAS').replace('SA<','SAS').replace('NY','NYK').replace('NY<','NYK').replace('NO','NOP').replace('NO<','NOP').replace('GS','GSW').replace('GS<','GSW').replace('UTAH','UTA')
        new_game_info.to_csv('output/2024/ESPN_game_info2024.csv') 
        
        return new_game_info, "All available game information was successfully collected.\n{num} entries were collected.".format(num = len(new_game_info))

def get_game_info(game_id):
    '''
    This function uses the saved game_ids to get the: line, spread, date, 
    attendance, capacity, home/away team information for each game.

    Next, it cleans the dates in order to be uniform with the dates in all
    other files.

    Last, it creates a dataframe and .csv file.
    '''
    game_info = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.111 Safari/537.36'}

    page = requests.get('https://www.espn.com/nba/game/_/gameId/{ID}'.format(ID = game_id), headers = headers)
    soup = BeautifulSoup(page.content, "lxml")
    
    #line, o/u, date, attendance, capacity from Game Information Table
    line = soup.find_all('div', attrs={'class':'n8 GameInfo__BettingItem flex-expand line'})
    line = str(line)
    line = line.replace('[<div class="n8 GameInfo__BettingItem flex-expand line">Line<!-- -->: <!-- -->','').replace('</div>]', '')
    line = line.split(' ')
    if len(line) == 2:
        favorite = line[0]
        spread   = line[1]
    else:
        favorite = 'EVEN'
        spread   = '0'

    over_under = soup.find_all('div', attrs={'class':'n8 GameInfo__BettingItem flex-expand ou'})
    over_under = str(over_under)
    over_under = over_under.replace('[<div class="n8 GameInfo__BettingItem flex-expand ou">Over/Under<!-- -->: <!-- -->','').replace('</div>]', '')
    over_under = over_under.replace(' ', '')

    date = soup.find_all('div', attrs={'class':'n8 GameInfo__Meta'})
    date = str(date)
    date = date.replace('[<div class="n8 GameInfo__Meta"><span>', '').replace('<!-- -->, <!-- -->', '=').replace('</span><span>Coverage<!-- -->: <!-- -->', '=').replace('</span></div>]','')
    date = date.split('=')
    date = date[1]   

    attendance = soup.find_all('div', attrs={'class':'Attendance__Numbers'})
    attendance = str(attendance)
    attendance = attendance.replace('[<div class="Attendance__Numbers">Attendance<!-- -->: <!-- -->','').replace('</div>]','').replace(',','')

    capacity = soup.find_all('div', attrs={'class':'Attendance__Capacity h10'})
    capacity = str(capacity)
    capacity = capacity.replace('[<div class="Attendance__Capacity h10">Capacity<!-- -->: <!-- -->','').replace('</div>]','').replace(',','')
    
    #team stats table
    teams = soup.find_all('div', attrs='Kiog TSds lEHQ Pxea FOeP nbAE')
    teams = str(teams)

    teams = teams.replace('<div class="Kiog TSds lEHQ Pxea FOeP nbAE">','').replace('</div>','').replace('[','').replace(']','')
    teams = teams.split('/><span class="">')

    away_team = teams[1][0:3]
    home_team = teams[2][0:3]

    info = '='.join([date, away_team, home_team, favorite, spread, over_under, attendance, capacity, game_ids[i]])
    info = info.split('=')  

    game_info.append(info)


    #I will be kind to your website, if you let me scrape easily :)
    time.sleep(1)

    for i in range(len(game_info)):
        game_info[i][0] = game_info[i][0].replace('October','10').replace(', ', '/').replace(' ', '/')
        game_info[i][0] = game_info[i][0].replace('November','11').replace(', ', '/').replace(' ', '/')
        game_info[i][0] = game_info[i][0].replace('December','12').replace(', ', '/').replace(' ', '/')
        game_info[i][0] = game_info[i][0].replace('January','01').replace(', ', '/').replace(' ', '/')
        game_info[i][0] = game_info[i][0].replace('February','02').replace(', ', '/').replace(' ', '/')
        game_info[i][0] = game_info[i][0].replace('March','03').replace(', ', '/').replace(' ', '/')
        game_info[i][0] = game_info[i][0].replace('April','04').replace(', ', '/').replace(' ', '/') 

    return game_info

#%%
if __name__ == "__main__":
    get_all_espn_game_info()