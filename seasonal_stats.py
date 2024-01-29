#%%
import pandas as pd
import numpy as np
from tqdm import tqdm

# %%
def seasonal_stats(year):
    '''
    This functions creates the season stats for each playey in the form of a 
    dataframe and also creates a .csv file in your directory.  The function combines
    stats from the Traditional and Advanced .csv files.  
    
    There is one issue with the accuracy of labeling the corect team of the player.  
    If the player played for one team, then got traded to another but did not play a 
    game for that team due to injury- his old team will still be listed, ex. Khem Birch. 

    The 'Team' column is based on the last team for which a player played in a game.  Birch is on the
    San Antonio Spurs, but his stats are listed under Toronto. He was traded while injured in Toronto
    and did not appear in any games while a member of SAS. This will be cleaned up eventually.
    '''
    traditional = pd.read_csv(f"output/{year}/Traditional{year}.csv", index_col = 0)
    advanced = pd.read_csv(f"output/{year}/Advanced{year}.csv", index_col = 0)
    players = traditional['Name'].unique()
    
    for i in range(len(players)):
        guy = traditional[traditional['Name'] == players[i]]
        guy_a = advanced[advanced['Name'] == players[i]]
        #calculate ratios of mins/total mins to properly weight stats such as OFFRTG, DEFRTG
        tot_mins = guy_a['Mins'].sum()
        mins = guy_a['Mins'].to_numpy()
        ratios = mins/tot_mins

        season = []
        GP = len(guy['Name'])

        season.append(guy['Name'].iloc[0])
        season.append(guy['Team'].iloc[0])
        season.append(year)
        season.append(GP)
        season.append((len(guy[guy['Result']=='W'])/GP)*100) #Win %
        season.append((guy['Mins'].sum()/GP))
        season.append((guy['Points'].sum()/GP))
        season.append((guy['Points'].sum()/guy['Mins'].sum())) #PPM
        season.append((guy['FGM'].sum()/GP))
        season.append((guy['FGA'].sum()/GP))
        season.append((guy['FGM'].sum()/guy['FGA'].sum())*100) #FG%
        season.append((guy['3PM'].sum()/GP))
        season.append((guy['3PA'].sum()/GP))
        season.append((guy['3PM'].sum()/guy['3PA'].sum())*100) #3P%
        season.append((guy['FTM'].sum()/GP))
        season.append((guy['FTA'].sum()/GP))
        season.append((guy['FTM'].sum()/guy['FTA'].sum())*100) #3P%
        season.append((guy['OREB'].sum()/GP))
        season.append((guy['DREB'].sum()/GP))
        season.append((guy['REB'].sum()/GP))
        season.append((guy['AST'].sum()/GP))
        season.append((guy['TOV'].sum()/GP))
        season.append((guy['AST'].sum()/guy['TOV'].sum())) #AST:TO ratio
        season.append((guy['STL'].sum()/GP))
        season.append((guy['BLK'].sum()/GP))
        season.append((guy['FGM'].sum() + (0.5*guy['3PM'].sum()))/guy['FGA'].sum()) #Effective Field Goal-%
        season.append((guy['Points'].sum())/( (2*guy['FGA'].sum())+(0.88*guy['FTA'].sum()) )) #True Shooting-%
        #Will add usage rate in time for each player
        #Calculate season Offensive Rating
        stat = guy_a['OFFRTG'].to_numpy()
        stat = stat*ratios
        num1 = sum(stat)
        season.append(num1)
        #Calculate season Defensive Rating
        stat = guy_a['DEFRTG'].to_numpy()
        stat = stat*ratios
        num2 = sum(stat)
        season.append(num2)
        #Caculate Season Net Rating
        season.append(num1-num2)
        season.append((guy['PF'].sum()/GP))
        season.append((guy['Plusminus'].sum()))
        #Calculate season Player Impact Estimator
        stat = guy_a['PIE'].to_numpy()
        stat = stat*ratios
        num  = sum(stat)
        season.append(num)
        
        if i != 0:
            new_player = pd.DataFrame(season)
            new_player = new_player.T
            new_player.columns = ['Name', 'Team', 'Season', 'GP', 'Win%', 'Mins', 'Points', 'PPM', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'AST/TO', 'STL', 'BLK', 'EFG%', 'TS%', 'OFFRTG', 'DEFRTG', 'NETRTG', 'PF', 'Plusminus', 'PIE']
            season_stats = pd.concat([new_player, season_stats], ignore_index=True, sort=False)
            #season_stats = season_stats.reset_index()

        else:
            season_stats = pd.DataFrame(season)
            season_stats = season_stats.T
            season_stats.columns = ['Name', 'Team', 'Season', 'GP', 'Win%', 'Mins', 'Points', 'PPM', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'AST/TO', 'STL', 'BLK', 'EFG%', 'TS%', 'OFFRTG', 'DEFRTG', 'NETRTG', 'PF', 'Plusminus', 'PIE']

    season_stats.to_csv(f"output/{year}/Season_Stats{year}.csv")    
    return season_stats

#%%
def partial_seasonal_stats(year):
    
    traditional = pd.read_csv(f"output/{year}/Traditional{year}.csv", index_col = 0)
    advanced    = pd.read_csv(f"output/{year}/Advanced{year}.csv", index_col = 0)
    dates = traditional['Date'].unique()
    # Use first 20% of games to normalize stats
    dates = dates[0:132] 

    for i in tqdm(range(len(dates))):
        trad = traditional
        tstats = trad[trad['Date'] == dates[i]].index
        trad = trad.iloc[tstats[-1]+1:]

        adv = advanced
        astats = advanced[advanced['Date'] == dates[i]].index
        adv = adv.iloc[astats[-1]+1:]

        daily_seasonal_stats(adv, trad, dates[i])

    return True
    
def daily_seasonal_stats(advanced, traditional, date, year):
    players = traditional['Name'].unique()
    
    for i in range(len(players)):
        guy = traditional[traditional['Name'] == players[i]]
        guy_a = advanced[advanced['Name'] == players[i]]
        #calculate ratios of mins/total mins to properly weight stats such as OFFRTG, DEFRTG
        tot_mins = guy_a['Mins'].sum()
        mins = guy_a['Mins'].to_numpy()
        ratios = mins/tot_mins

        season = []
        GP = len(guy['Name'])

        season.append(guy['Name'].iloc[0])
        season.append(guy['Team'].iloc[0])
        season.append(year)
        season.append(GP)
        season.append((len(guy[guy['Result']=='W'])/GP)*100) #Win %
        season.append((guy['Mins'].sum()/GP))
        season.append((guy['Points'].sum()/GP))
        season.append((guy['Points'].sum()/guy['Mins'].sum())) #PPM
        season.append((guy['FGM'].sum()/GP))
        season.append((guy['FGA'].sum()/GP))
        season.append((guy['FGM'].sum()/guy['FGA'].sum())*100) #FG%
        season.append((guy['3PM'].sum()/GP))
        season.append((guy['3PA'].sum()/GP))
        season.append((guy['3PM'].sum()/guy['3PA'].sum())*100) #3P%
        season.append((guy['FTM'].sum()/GP))
        season.append((guy['FTA'].sum()/GP))
        season.append((guy['FTM'].sum()/guy['FTA'].sum())*100) #3P%
        season.append((guy['OREB'].sum()/GP))
        season.append((guy['DREB'].sum()/GP))
        season.append((guy['REB'].sum()/GP))
        season.append((guy['AST'].sum()/GP))
        season.append((guy['TOV'].sum()/GP))
        season.append((guy['AST'].sum()/guy['TOV'].sum())) #AST:TO ratio
        season.append((guy['STL'].sum()/GP))
        season.append((guy['BLK'].sum()/GP))
        season.append((guy['FGM'].sum() + (0.5*guy['3PM'].sum()))/guy['FGA'].sum()) #Effective Field Goal-%
        season.append((guy['Points'].sum())/( (2*guy['FGA'].sum())+(0.88*guy['FTA'].sum()) )) #True Shooting-%
        #Will add usage rate in time for each player
        #Calculate season Offensive Rating
        stat = guy_a['OFFRTG'].to_numpy()
        stat = stat*ratios
        num1 = sum(stat)
        season.append(num1)
        #Calculate season Defensive Rating
        stat = guy_a['DEFRTG'].to_numpy()
        stat = stat*ratios
        num2 = sum(stat)
        season.append(num2)
        #Caculate Season Net Rating
        season.append(num1-num2)
        season.append((guy['PF'].sum()/GP))
        season.append((guy['Plusminus'].sum()))
        #Calculate season Player Impact Estimator
        stat = guy_a['SIE'].to_numpy()
        stat = stat*ratios
        num  = sum(stat)
        season.append(num)

        if i != 0:
            new_player = pd.DataFrame(season)
            new_player = new_player.T
            new_player.columns = ['Name', 'Team', 'Season', 'GP', 'Win%', 'Mins', 'Points', 'PPM', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'AST/TO', 'STL', 'BLK', 'EFG%', 'TS%', 'OFFRTG', 'DEFRTG', 'NETRTG', 'PF', 'Plusminus', 'PIE']
            season_stats = pd.concat([new_player, season_stats], ignore_index=True, sort=False)
            #season_stats = season_stats.reset_index()

        else:
            season_stats = pd.DataFrame(season)
            season_stats = season_stats.T
            season_stats.columns = ['Name', 'Team', 'Season', 'GP', 'Win%', 'Mins', 'Points', 'PPM', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'AST/TO', 'STL', 'BLK', 'EFG%', 'TS%', 'OFFRTG', 'DEFRTG', 'NETRTG', 'PF', 'Plusminus', 'PIE']
    
    date = date.split('/')
    if date[0][0] == '0':
        date[0] = date[0].replace('0', '')
    if date[1][0] == '0':
        date[1] = date[1].replace('0', '')
        
    season_stats.to_csv(f"output/{year}/Seasonal Stats/{date[0]}_{date[1]}_{date[2]}.csv")

    return True

#%%
if __name__ == "__main__":
    seasonal_stats()
    partial_seasonal_stats()
    daily_seasonal_stats()
