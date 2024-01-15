#%%
import requests
import pandas as pd
import time
from tqdm import tqdm
from bs4 import BeautifulSoup

#%% Get all game IDs for 2022-2023 regular season
#   Create .txt to save game IDs so no need to rerun    
def get_game_ids(year: int = 0):
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
    elif year == 2023:
        game_ids = get_2023_game_ids(link, headers)
        return game_ids
    elif year == 2024:
        game_ids = get_2024_game_ids(link, headers)
        return game_ids
    elif year == 0:
        raise ValueError("Please enter a year to get game IDs: 2023 or 2024")
    else:
        return 'This data is not available yet.' 


def get_2023_game_ids(link, headers):

    game_ids = []
    for game in tqdm(range(401468016, 401469385+1)):
        if game == 401468924:
            game = 401526670 #WSH and DET had a game postponed, this is the new game ID.

        url = ''.join([link, str(game)])
        record = requests.get(url, headers = headers)
        if record.status_code == 200:
            game_ids.append(str(game))

        #Just being kind to ESPN since they are the one website to not give me a hassle
        time.sleep(0.5) 
    
    with open('output/2023/GameIDs2023.txt', 'w') as file:
        write_data = '\n'.join(game_ids)
        file.write(write_data)

    return game_ids    

def get_2024_game_ids(link, headers):

    game_ids = []
    for game_id in tqdm(range(401584689, 401585828+1)): #401585828+1
        row = []

        url = ''.join([link, str(game_id)])
        game_site = requests.get(url, headers = headers)
        if game_site.status_code == 200:

            soup = BeautifulSoup(game_site.content, "lxml")
            date = soup.find_all('div', attrs={'class':'n8 GameInfo__Meta'})
            date = str(date)
            date = date.replace('[<div class="n8 GameInfo__Meta"><span>', '').replace('<!-- -->, <!-- -->', '=').replace('</span><span>Coverage<!-- -->: <!-- -->', '=').replace('</span></div>]','')
            date = date.split('=')
            date = date[1]   

            date = date.replace('October','10').replace(', ', '/').replace(' ', '/')
            date = date.replace('November','11').replace(', ', '/').replace(' ', '/')
            date = date.replace('December','12').replace(', ', '/').replace(' ', '/')
            date = date.replace('January','01').replace(', ', '/').replace(' ', '/')
            date = date.replace('February','02').replace(', ', '/').replace(' ', '/')
            date = date.replace('March','03').replace(', ', '/').replace(' ', '/')
            date = date.replace('April','04').replace(', ', '/').replace(' ', '/') 

            date = date.split('/')
            date = '{year}-{month}-{day}'.format(year = date[2], month = date[0], day = date[1])

            row.append(date)
            row.append(game_id)

            game_ids.append(row)

        else:
            pass


        #Just being kind to ESPN since they are the one website to not give me a hassle
        time.sleep(0.5) 

    game_ids = pd.DataFrame(game_ids, columns = ['Date', "Game ID"])
    with open('output/2024/GameIDs2024.txt', 'a') as f:
        game_ids_string = game_ids['Game ID'].to_string(header = False, index = False)
        f.write(game_ids_string)
    game_ids.to_csv('output/2024/GameIDs2024.csv')

    # with open('output/2024/GameIDs2024.txt', 'w') as file:
    #     write_data = '\n'.join(game_ids)
    #     file.write(write_data)    

    return game_ids  

def get_game_info(year):
    '''
    This function uses the saved game_ids to get the: line, spread, date, 
    attendance, capacity, home/away team information for each game.

    Next, it cleans the dates in order to be uniform with the dates in all
    other files.

    Last, it creates a dataframe and .csv file.
    '''
    game_info = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.111 Safari/537.36'}

    if year == 2023:
        game_ids = open('output/{num}/GameIDs{num}.txt'.format(num = year))
        game_ids = game_ids.read()
        game_ids = game_ids.split('\n')
        game_ids[768] = '401526670'
    else:
        game_ids = open('output/{num}/GameIDs{num}.txt'.format(num = year))
        game_ids = game_ids.read()
        game_ids = game_ids.split('\n')

    for i in tqdm(range(0, 471)): #len(game_ids)
        page = requests.get('https://www.espn.com/nba/game/_/gameId/{ID}'.format(ID = game_ids[i]), headers = headers)
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

    game_lines = pd.DataFrame(game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'O/U','Attendance', 'Capacity', 'Game ID'], index = None)
    game_lines = game_lines.replace('WSH', 'WAS').replace('SA','SAS').replace('SA<','SAS').replace('NY','NYK').replace('NY<','NYK').replace('NO','NOP').replace('NO<','NOP').replace('GS','GSW').replace('GS<','GSW').replace('UTAH','UTA')
    game_lines.to_csv('output/{num}/Caesars_Lines{num}.csv'.format(num = year))  

    return game_lines

#%%
if __name__ == "__main__":
    get_game_ids()
    get_game_info()