#%%
import pandas as pd

#%%
def get_team_rotations(year):
    """
    Here we are creating the average rotation size per team, per game.

    For a player to be considered part of the rotation for a particular
    game, they had to have played more than 10 mins.  This is to ensure 
    the exclusion of most garbage time minutes while including players
    who perhaps do not play as much as star player but do make an impact. 

    A simple moving average (sma) is created using a 10 game window.  
    The logic behind this is to take into account that rosters change 
    during the season, teams change their rotation size throughout the
    season, coaching changes bring different schemes in the building. 

    A cumulative moving average (cma) is created to fill the nan's of
    the sma dataframe.

    Last, we round off the rotation size and save that as a .csv file 
    to be used as an input when running the model.  
    """
    box_scores = pd.read_csv('output/{num}/Advanced{num}.csv'.format(num = year), index_col=0)
    box_scores['Date'] = pd.to_datetime(box_scores['Date'], format = '%m/%d/%Y')
    box_scores = box_scores.sort_values(by = ['Date'], ascending = True)
    teams = box_scores['Team'].unique()

    rotations= []
    box_scores = box_scores[box_scores['Mins'] > 10]

    for i in teams:
        season = box_scores[box_scores['Team'] == i]
        dates  = season['Date'].unique()
        team_rotations = []
        for j in dates:
            team_rotations.append(len(season[season['Date'] == j]))

        #team_rotations.reverse()
        rotations.append(team_rotations)

    rotations = pd.DataFrame(rotations)
    rotations = rotations.T
    rotations.columns = teams
    sma = []
    cma = []
    for i in teams:
        #get simply moving average of 10 game window
        sma_team = rotations[i].rolling(10).mean().to_numpy() 
        sma.append(sma_team)
        
        #get cumulative moving average to replace nans in first 10 rows of sma
        cma_team = rotations[i].expanding().mean().to_numpy()
        cma.append(cma_team)

    sma = pd.DataFrame(sma)
    sma = sma.T
    sma.columns = teams

    cma = pd.DataFrame(cma)
    cma = cma.T
    cma.columns = teams
    ten_games = cma.iloc[0:9]
    sma = sma.dropna()
    rotations = pd.concat([ten_games, sma])

    model_rotations = round(rotations)
    model_rotations.to_csv('output/{num}/Rotations{num}.csv'.format(num = year))

    return model_rotations
# %%
rotations = get_team_rotations('2023')

#%%
if __name__ == "__main__":
    get_team_rotations()