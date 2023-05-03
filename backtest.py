#%%
import pandas as pd
from seasonal_stats import *

#%%
rotations    = pd.read_csv('output/Rotations.csv', index_col = 0)
injuries     = pd.read_csv('output/Injury_Data.csv', index_col = 0)
schedule     = pd.read_csv('output/Schedule2223.csv', index_col = 0)
season_stats = pd.read_csv('output/Season_Stats.csv', index_col = 0)
advanced     = pd.read_csv('output/Advanced.csv', index_col = 0)
traditional  = pd.read_csv('output/Traditional.csv', index_col = 0)

day   = schedule[schedule['Date'] == '11/20/2022'].index
games = schedule[schedule['Date'] == '11/20/2022']
schedule = schedule.iloc[day[-1]+1:]
Hteams = list(games['Team'])
Ateams = list(games['Opponent'])
teams  = Hteams + Ateams
teams

#%%
#grab proper rotation for game
game_num = schedule['Team'].value_counts()['BKN'] + schedule['Opponent'].value_counts()['BKN']
rotation = rotations['BKN'].iloc[game_num-1]
     
#%%
test = pd.read_csv('output/Backtest_Stats.csv', index_col = 0)     
test
#%%
phx = test[test['Team'] == 'PHX']
phx[phx['Name'].str.contains('Bridges')]

#%%
phx = test[test['Team'] == 'PHX']
phx['Name'].str.contains('Bridges').any()
# %%
