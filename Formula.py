#%%
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.stats import norm
from scipy.stats import truncnorm
import statsmodels.api as sm


"""
This code is from the proof of concept model. This needs to be integrated
with the new code.  This code will be used to run the first backtest.

"""
#%%
def get_truncated_normal(mean=1, sd=1, low=0.5, upp=1.5):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

X = get_truncated_normal(mean=1, sd=1, low= 0.5, upp= 1.5)


def def_truncated_normal(mean=1, sd=1, low=0.95, upp=1.05):
    return truncnorm((low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

Y = def_truncated_normal(mean=1, sd=1, low=0.95, upp=1.05)


#%%
#American betting odds for home and away teams
def USA_home(decimal_home):
    if decimal_home >= 2:
        american_home = (decimal_home - 1)*100
    else:
        american_home = (-100)/(decimal_home-1)
    
    return american_home


def USA_away(decimal_away):
    if decimal_away >= 2:
        american_away = (decimal_away - 1)*100
    else:
        american_away = (-100)/(decimal_away-1)
    
    return american_away


def odds(df_outcomes, away, home):
    #wins = 0
    #for i in range(len(df_outcomes["Home"])):
    #    if(df_outcomes["Home"].iloc[i] > df_outcomes["Away"].iloc[i]):
    #        wins += 1
    
    wins = len(df_outcomes.loc[df_outcomes['Home'] > df_outcomes['Away']])
    
    home_spread = (df_outcomes["Away"].mean() - df_outcomes["Home"].mean())
            
    implied_home = (wins/len(df_outcomes["Away"]))*100
    implied_away = 100 - implied_home 
    
    decimal_home = 100/implied_home
    decimal_away = 100/implied_away
    
    american_home = USA_home(decimal_home)
    american_away = USA_away(decimal_away)
    
    home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away =home, home_spread,implied_home, decimal_home, american_home,away, implied_away,decimal_away,american_away
    
    return home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away

#%%
def Minutes(mpg, inj, rotation_size):
    add_mins = sum(mpg[-(len(mpg)-int(rotation_size)):]) + sum(inj) #sum mins from players not in rotation_size
    
    #First Adjustment
    mpg = mpg[0:int(rotation_size)]
    add_mins = add_mins/len(mpg)
    mpg = mpg + add_mins
    
    bench_initial = sum(mpg[5:])
    excess_mins = sum(mpg) - 240
    avg_deduct = excess_mins/len(mpg)
    starter_deduct = avg_deduct/2
    
    #Final Deduction for starters
    mpg[:5] = mpg[:5] - starter_deduct
    
    bench_players = len(mpg)-5
    num = (sum(mpg[:5]) + bench_initial) - 240 #finding number to divide from using bench_players
    bench_deduct = num/bench_players
    mpg[5:] = mpg[5:]-bench_deduct
    
    return mpg

#%%
def points_home(proj_pts_home, mpg_home, ppm_home, drtg_bos, drtg_mean):
    for i in range(len(proj_pts_home)):
        proj_pts_home[i] = (mpg_home[i]*ppm_home[i]*X.rvs()) * ((drtg_bos/drtg_mean)*Y.rvs())
    
    return sum(proj_pts_home) + 1.5    
    

def points_away(proj_pts_away, mpg_away, ppm_away, drtg_bkn, drtg_mean):
    for i in range(len(proj_pts_away)):
        proj_pts_away[i] = (mpg_away[i]*ppm_away[i]*X.rvs()) * ((drtg_bkn/drtg_mean)*Y.rvs())
    
    return sum(proj_pts_away) - 1.5   


#%%
def drtg_home(drtg_bkn, mpg_home, bkn_drtg, rotation_size_home):
    
    for i in range(int(rotation_size_home)):
        drtg_bkn[i] = (mpg_home[i]/240)*bkn_drtg[i]
    
    return sum(drtg_bkn)
    
    
def drtg_away(drtg_bos, mpg_away, bos_drtg, rotation_size_away): 
    for i in range(int(rotation_size_away)):
        drtg_bos[i] = (mpg_away[i]/240)*bos_drtg[i]
    
    return sum(drtg_bos)


def def_rtg_mean(season_stats):

    tot_mins = season_stats['Mins'].sum()
    mins = season_stats['Mins'].to_numpy()
    defrtg = season_stats['DEFRTG'].to_numpy()
    ratios = mins/tot_mins
    defrtg = ratios*defrtg
    defrtg_mean = sum(defrtg)

    return defrtg_mean

#%%
def official_projections(season_stats, home, injuries_home, home_rotation, away, injuries_away, away_rotation):
    drtg_mean = def_rtg_mean(season_stats)

    bkn = season_stats.loc[season_stats['Team'] == home]
    bkn = bkn.sort_values(by='Mins', ascending=False)
    if injuries_home != []:
        bkn_temp = bkn[~bkn['Name'].isin(injuries_home)] #returns all rows not including those in injury report
        bkn_inj  = bkn[bkn['Name'].isin(injuries_home)]
        mpg_inj_home = bkn_inj['Mins'].to_numpy()
        
        if int(home_rotation) > len(bkn_temp['Name']):
            home_rotation = len(bkn_temp['Name'])
    else:
        mpg_inj_home = [0]

    bkn["DEFRTG"] = bkn["DEFRTG"].fillna(drtg_mean)
    bkn_drtg = bkn["DEFRTG"][0:int(home_rotation)].to_numpy()    
    
    bos = season_stats.loc[season_stats['Team'] == away]
    bos = bos.sort_values(by='Mins', ascending=False)
    if injuries_away != []:
        bos_temp = bos[~bos['Name'].isin(injuries_away)] #returns all rows not including those in injury report
        bos_inj  = bos[bos['Name'].isin(injuries_away)]
        mpg_inj_away = bos_inj['Mins'].to_numpy()

        
        if int(away_rotation) > len(bos_temp['Name']):
            away_rotation = len(bos_temp['Name'])
    else:
        mpg_inj_away = [0]


    bos["DEFRTG"] = bos["DEFRTG"].fillna(drtg_mean)
    bos_drtg = bos["DEFRTG"][0:int(away_rotation)].to_numpy()    
        
    mpg_home = bkn['Mins'].to_numpy()
    mpg_away = bos['Mins'].to_numpy()
    
    mpg_home = Minutes(mpg_home, mpg_inj_home, home_rotation)
    mpg_away = Minutes(mpg_away, mpg_inj_away, away_rotation)
    
    ppm_home = bkn["PPM"][0:int(home_rotation)].to_numpy()
    ppm_away = bos["PPM"][0:int(away_rotation)].to_numpy()
    
    drtg_bkn = np.full(int(home_rotation),0)
    drtg_bkn = drtg_home(drtg_bkn, mpg_home, bkn_drtg, home_rotation)
    drtg_bos = np.full(int(away_rotation),0)
    drtg_bos = drtg_away(drtg_bos, mpg_away, bos_drtg, away_rotation)
    
    proj_pts_home = np.full(int(home_rotation),0)
    proj_pts_away = np.full(int(away_rotation),0)

    HMPTS = points_home(proj_pts_home, mpg_home, ppm_home, drtg_bos, drtg_mean)
    AWPTS = points_away(proj_pts_away, mpg_away, ppm_away, drtg_bkn, drtg_mean)
    
    return HMPTS, AWPTS
    

def matchup(home, away, date, schedule, rotations, injuries):
    proj_away = np.full(1500,1.0)
    proj_home = np.full(1500,1.0)

    cleaned_date = date.replace('/', '_')
    cleaned_date = ''.join([cleaned_date,'.csv'])
    directory = 'output/Seasonal Stats/'
    location = ''.join([directory, cleaned_date])
    season_stats = pd.read_csv(location, index_col=0)

    index_date = date.split('/')
    if len(index_date[0]) == 1:
        index_date[0] = ''.join(['0', index_date[0]])
    if len(index_date[1]) == 1:
        index_date[1] = ''.join(['0', index_date[1]])
    file_date  = '_'.join([index_date[0], index_date[1], index_date[2]])
    index_date = '/'.join([index_date[0], index_date[1], index_date[2]])


    directory = 'output/Active Rosters/'
    location = ''.join([directory, file_date, '.csv'])
    active = pd.read_csv(location, index_col=0)

    home_roster = active[active['Team'] == home]
    home_roster = home_roster['Name'].to_list()
    away_roster = active[active['Team'] == away]
    away_roster = away_roster['Name'].to_list()
    
    home_seasonal = season_stats[season_stats['Team'] == home]
    away_seasonal = season_stats[season_stats['Team'] == away]

    home_seasonal = home_seasonal[home_seasonal['Name'].isin(home_roster)]
    away_seasonal = away_seasonal[away_seasonal['Name'].isin(away_roster)]

    season_stats = pd.concat([home_seasonal, away_seasonal], ignore_index=True)

    day      = schedule[schedule['Date'] == index_date].index
    schedule = schedule.iloc[day[-1]+1:]

    home_team_num = schedule['Team'].value_counts()[home] + schedule['Opponent'].value_counts()[home]
    home_rotation = rotations[home].iloc[home_team_num-1]
    away_team_num = schedule['Team'].value_counts()[away] + schedule['Opponent'].value_counts()[away]
    away_rotation = rotations[away].iloc[away_team_num-1]

    injuries_temp = injuries[injuries['Date'] == date]
    injuries_home = injuries_temp[injuries_temp['Team'] == home]
    injuries_home = injuries_temp['Name'].unique()
    injuries_temp = injuries[injuries['Date'] == date]
    injuries_away = injuries_temp[injuries_temp['Team'] == away]
    injuries_away = injuries_temp['Name'].unique()



    for i in range(len(proj_away)):
        proj_home[i], proj_away[i] = official_projections(season_stats, home, injuries_home, home_rotation, away, injuries_away, away_rotation)
        
    df_outcomes = pd.DataFrame(data=[proj_home, proj_away]).T
    df_outcomes.columns = ("Home", "Away")
    df_outcomes = df_outcomes.drop(df_outcomes[df_outcomes["Home"] == df_outcomes["Away"]].index)    
    
    home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away = odds(df_outcomes, away, home)
    
    return home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away

#%%
active = pd.read_csv('output/Active Rosters/04_09_2023.csv', index_col=0)
active

#%%
schedule = pd.read_csv('output/Schedule2223.csv', index_col = 0)
rotations= pd.read_csv('output/Rotations.csv', index_col = 0)
matchups = pd.read_csv('output/Caesars_Lines.csv', index_col=0)
day      = matchups[matchups['Date'] == '11/20/2022'].index
matchups = matchups.iloc[day[0]:]
injuries = pd.read_csv('output/Injury_Data.csv', index_col = 0)
matchup('DET', 'BKN', '12/18/2022', schedule, rotations, injuries)
#%%
if __name__=='__main__':
    matchup()

