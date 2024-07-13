#%%
import pandas as pd

#%%
def get_team_rotations(adv_year, trad_year):
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

    #following code will run into issues if you scrape for different years at once.
    if adv_year == 0 and trad_year == 0:
        return "No updates made to the Rotation size file."
    elif adv_year != 0:
        year = adv_year
        print((f"                   {adv_year} Rotation Size File                     \n"
               f"=============================================================="))    

        box_scores = pd.read_csv(f"output/{adv_year}/Advanced{adv_year}.csv", index_col=0)
    else:
        year = trad_year
        print((f"                   {trad_year} Rotation Size File                     \n"
               f"=============================================================="))    

        box_scores = pd.read_csv(f"output/{trad_year}/Advanced{trad_year}.csv", index_col=0)

    box_scores['Date'] = pd.to_datetime(box_scores['Date'], format = '%Y-%m-%d')
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
        #get simple moving average of 10 game window
        sma_team = rotations[i].rolling(10).mean().to_numpy() 
        sma.append(sma_team)
        
        #get cumulative moving average to replace nans in first 10 rows of sma
        cma_team = rotations[i].expanding().mean().to_numpy()
        cma.append(cma_team)

    sma = pd.DataFrame(sma)
    sma = sma.T
    sma.columns = teams
    sma = sma.iloc[9:]

    cma = pd.DataFrame(cma)
    cma = cma.T
    cma.columns = teams
    first_ten_games = cma.iloc[0:9]

    rotations = pd.concat([first_ten_games, sma])

    model_rotations = round(rotations)
    model_rotations.to_csv(f"output/{year}/Rotations{year}.csv")

    return f"{year} rotation size file is updated!"
#%%
if __name__ == "__main__":
    get_team_rotations()