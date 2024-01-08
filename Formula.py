#%%
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.stats import norm
from scipy.stats import truncnorm

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
'''
This code is from the original model.  This code calculates team projected points for a given game
and team Defensive Ratings. 

Team As PPG and Team Bs DRTG are compared to create Team As final projected points.
Same goes for Team B.
'''
def calculate_player_minutes(mpg, inj, rotation_size):
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

def selvaggi_importance_metric(mpg, proj_sim, sim):
    for i in range(len(proj_sim)):
        proj_sim[i] = (mpg[i]*sim[i])
    
    return sum(proj_sim) 

def calculate_home_points(proj_pts_home, mpg_home, ppm_home):
    for i in range(len(proj_pts_home)):
        proj_pts_home[i] = (mpg_home[i]*ppm_home[i]) 
    
    return sum(proj_pts_home) + 1.5    
    
def calculate_away_points(proj_pts_away, mpg_away, ppm_away):
    for i in range(len(proj_pts_away)):
        proj_pts_away[i] = (mpg_away[i]*ppm_away[i])
    
    return sum(proj_pts_away) - 1.5   

def calculate_home_defensive_rating(home_team_drtg, mpg_home, home_player_drtg, home_rotation):
    
    for i in range(int(home_rotation)):
        home_team_drtg[i] = (mpg_home[i]/240)*home_player_drtg[i]
    
    return sum(home_team_drtg)
     
def calculate_away_defensive_rating(away_team_drtg, mpg_away, away_player_drtg, away_rotation):
    for i in range(int(away_rotation)):
        away_team_drtg[i] = (mpg_away[i]/240)*away_player_drtg[i]
    
    return sum(away_team_drtg)

def calculate_mean_player_defensive_rating(season_stats):

    tot_mins = season_stats['Mins'].sum()
    mins = season_stats['Mins'].to_numpy()
    defrtg = season_stats['DEFRTG'].to_numpy()
    ratios = mins/tot_mins
    defrtg = ratios*defrtg
    defrtg_mean = sum(defrtg)

    return defrtg_mean

def official_projections(season_stats, home, injuries_home, home_rotation, away, injuries_away, away_rotation):
    drtg_mean = calculate_mean_player_defensive_rating(season_stats)

    home_stats = season_stats.loc[season_stats['Team'] == home]
    home_stats = home_stats.sort_values(by='Mins', ascending=False)
    if injuries_home != []:
        home_stats_temp = home_stats[~home_stats['Name'].isin(injuries_home)] #returns all rows not including those in injury report
        home_inj  = home_stats[home_stats['Name'].isin(injuries_home)]
        mpg_inj_home = home_inj['Mins'].to_numpy()
        
        if int(home_rotation) > len(home_stats_temp['Name']):
            home_rotation = len(home_stats_temp['Name'])
    else:
        mpg_inj_home = [0]

    home_stats["DEFRTG"] = home_stats["DEFRTG"].fillna(drtg_mean)
    home_player_drtg = home_stats["DEFRTG"][0:int(home_rotation)].to_numpy()    
    
    away_stats = season_stats.loc[season_stats['Team'] == away]
    away_stats = away_stats.sort_values(by='Mins', ascending=False)
    if injuries_away != []:
        away_stats_temp = away_stats[~away_stats['Name'].isin(injuries_away)] #returns all rows not including those in injury report
        away_inj  = away_stats[away_stats['Name'].isin(injuries_away)]
        mpg_inj_away = away_inj['Mins'].to_numpy()

        
        if int(away_rotation) > len(away_stats_temp['Name']):
            away_rotation = len(away_stats_temp['Name'])
    else:
        mpg_inj_away = [0]


    away_stats["DEFRTG"] = away_stats["DEFRTG"].fillna(drtg_mean)
    away_player_drtg = away_stats["DEFRTG"][0:int(away_rotation)].to_numpy()    
        
    mpg_home = home_stats['Mins'].to_numpy()
    mpg_away = away_stats['Mins'].to_numpy()
    
    mpg_home = calculate_player_minutes(mpg_home, mpg_inj_home, home_rotation)
    mpg_away = calculate_player_minutes(mpg_away, mpg_inj_away, away_rotation)
    
    home_team_drtg = np.full(int(home_rotation),0.0)
    home_team_drtg = calculate_home_defensive_rating(home_team_drtg, mpg_home, home_player_drtg, home_rotation)
    away_team_drtg = np.full(int(away_rotation),0.0)
    away_team_drtg = calculate_away_defensive_rating(away_team_drtg, mpg_away, away_player_drtg, away_rotation)

    ppm_home = home_stats["PPM"][0:int(home_rotation)].to_numpy()
    ppm_away = away_stats["PPM"][0:int(away_rotation)].to_numpy()    
    
    proj_pts_home = np.full(int(home_rotation),0.0)
    proj_pts_away = np.full(int(away_rotation),0.0)

    home_pts = calculate_home_points(proj_pts_home, mpg_home, ppm_home)
    away_pts = calculate_away_points(proj_pts_away, mpg_away, ppm_away)

    proj_sim_home = np.full(int(home_rotation),0.0)
    proj_sim_away = np.full(int(away_rotation),0.0)

    sim_home = home_stats["SIM"][0:int(home_rotation)].to_numpy()
    sim_away = away_stats["SIM"][0:int(away_rotation)].to_numpy()    

    home_sim = selvaggi_importance_metric(mpg_home, proj_sim_home, sim_home)    
    away_sim = selvaggi_importance_metric(mpg_away, proj_sim_away, sim_away)

    return home_pts, home_team_drtg, home_sim, away_pts, away_team_drtg, away_sim
    
def matchup(year, home, away, date, schedule, rotations, injuries):

    cleaned_date = date.replace('/', '_')
    cleaned_date = ''.join([cleaned_date,'.csv'])
    directory = 'output/{num}/Seasonal Stats/'.format(num = year)
    location = ''.join([directory, cleaned_date])
    season_stats = pd.read_csv(location, index_col=0)

    index_date = date.split('/')
    if len(index_date[0]) == 1:
        index_date[0] = ''.join(['0', index_date[0]])
    if len(index_date[1]) == 1:
        index_date[1] = ''.join(['0', index_date[1]])
    index_date = '/'.join([index_date[0], index_date[1], index_date[2]])

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
    home_pts, home_def, home_sim, away_pts, away_def, away_sim = official_projections(season_stats, home, injuries_home, home_rotation, away, injuries_away, away_rotation)   
        
    return home, home_pts, home_def, home_sim, away, away_pts, away_def, away_sim

#%%
if __name__=='__main__':
    matchup()
    official_projections() #
    calculate_mean_player_defensive_rating()
    calculate_away_defensive_rating()
    calculate_home_defensive_rating()
    calculate_away_points()
    calculate_home_points()
    selvaggi_importance_metric() 
    calculate_player_minutes() 
