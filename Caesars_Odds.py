#%%
import requests
import pandas as pd
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
#%%
link = 'https://www.espn.com/nba/game/_/gameId/'
first_game = 401468016 #game ID of first game of 2022-2023 regular season
last_game  = 401469385 #game ID of last  game of 2022-2023 regular season

#%% Get all game IDs for 2022-2023 regular season
#   Create .txt to save game IDs so no need to rerun    
def get_game_ids(first_game, last_game):
    '''
    There are 1230 games in a NBA regular season. Each game ID corresponds
    to a regular season game on ESPN.go.com.  The range of game ids from the
    first to last game of the regular season is larger than 1230.  So we 
    need to figure out which game ids are valid-  this function checks the 
    validity by way of comparing request status codes.
    '''
    game_ids = []
    for i in tqdm(range(first_game, last_game+1)):
        if i == 401468924:
            i = 401526670 #WSH and DET had a game postponed, this is the new game ID.
        game = str(i)
        url = ''.join([link, game])
        record = requests.get(url)
        if record.status_code == 200:
            game_ids.append(game)

        #Just being kind to ESPN since they are the one website to not give me a hassle
        time.sleep(0.5) 
    
    return game_ids
#%%
game_ids = get_game_ids(401468016, 401469385)
# game_ids = get_game_ids(401468016, 401469385)
# with open('GameIDs2223.txt', 'w') as outfile:
#   outfile.write('\n'.join(str(i) for i in game_ids))
# #%%
# game_ids = open('GameIDs2223.txt')
# game_ids = game_ids.read()
# game_ids = game_ids.split('\n')

# %%
def get_game_info():
    '''
    This function uses the saved game_ids to get the: line, spread, date, 
    attendance, capacity, home/away team information for each game.

    Next, it cleans the dates in order to be uniform with the dates in all
    other files.

    Last, it creates a dataframe and .csv file.
     '''
    link = 'https://www.espn.com/nba/game/_/gameId/'
    game_info = []
    game_ids = open('output/GameIDs2223.txt')
    game_ids = game_ids.read()
    game_ids = game_ids.split('\n')
    game_ids[768] = '401526670'

    for i in tqdm(range(0, len(game_ids))):
        url = ''.join([link, game_ids[i]])
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "lxml")

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

        teams = soup.find_all('div', attrs='BarLine__Item__Label')
        teams = str(teams)
        teams = teams.replace('<div class="BarLine__Item__Label">','').replace('</div>','').replace('[','').replace(']','')
        teams = teams.split(', ')

        away_team = teams[0]
        home_team = teams[1]

        info = '='.join([date, home_team, away_team, favorite, spread, attendance, capacity])
        info = info.split('=')  

        game_info.append(info)

        #I will be kind to your website, if you let me scrape easily :)
        time.sleep(5)

    for i in range(len(game_info)):
        if 'October' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('October','10')
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')
        elif 'November' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('November','11')
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')
        elif 'December' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('December','12')
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')
        elif 'January' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('January','01')
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')
        elif 'February' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('February','02')
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')
        elif 'March' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('March','03')
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')
        elif 'April' in game_info[i][0]:
            game_info[i][0] = game_info[i][0].replace('April','04')                                                
            game_info[i][0] = game_info[i][0].replace(', ', '/')
            game_info[i][0] = game_info[i][0].replace(' ', '/')

    game_lines = pd.DataFrame(game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'Attendance', 'Capacity'], index = None)
    game_lines = game_lines.replace(to_replace='WSH', value='WAS').replace(to_replace='SA', value = 'SAS').replace(to_replace='NY', value='NYK').replace(to_replace='NO', value='NOP').replace(to_replace='GS', value='GSW').replace(to_replace='UTAH', value='UTA')
    game_lines.to_csv('output/Caesars_Lines.csv')  

    return game_lines
#%%
game_info = get_game_info()
game_info

# #%%
# caesars_lines = pd.read_csv('Caesars_Lines.csv', index_col= 0)
# caesars_lines = caesars_lines[['Date', 'Home', 'Away', 'Favorite', 'Spread']]
# caesars_lines[['Spread']] = caesars_lines[['Spread']].astype(float)
# caesars_lines

#%%
if __name__ == "__main__":
    get_game_ids()
    get_game_info()