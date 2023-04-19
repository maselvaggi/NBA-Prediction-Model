#%%
import requests
import pandas as pd
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
#%%
link = 'https://www.espn.com/nba/game/_/gameId/'
first = 401468016 #game ID of first game of regular season
last  = 401469385 #game ID of last  game of regular season

#%% Get all game IDs for 2022-2023 regular season
#   Create .txt to save game IDs so no need to rerun    
game_ids = []

for i in tqdm(range(first, last+1)):
    if i == 401468924:
        i = 401526670
    game = str(i)
    url = ''.join([link, game])
    record = requests.get(url)
    if record.status_code == 200:
        game_ids.append(game)

    time.sleep(0.5) #Just being kind to ESPN
#%%
with open('GameIDs2223.txt', 'w') as outfile:
  outfile.write('\n'.join(str(i) for i in game_ids))
#%%
game_ids = open('GameIDs2223.txt')
game_ids = game_ids.read()
game_ids = game_ids.split('\n')
game_ids[768] = '401526670' #WSH and DET had a game postponed, this is the new game ID for that game.
game_ids

# %%
game_info = []
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
    time.sleep(0.5)
#%%
game_info
# %%
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

#%%
game_lines = pd.DataFrame(game_info, columns=['Date', 'Home', 'Away', 'Favorite', 'Spread', 'Attendance', 'Capacity'], index = None)
game_lines.to_csv('Caesars_Lines.csv')
#%%
caesars_lines = pd.read_csv('Caesars_Lines.csv', index_col= 0)
caesars_lines = caesars_lines[['Date', 'Home', 'Away', 'Favorite', 'Spread']]
caesars_lines[['Spread']] = caesars_lines[['Spread']].astype(float)
caesars_lines