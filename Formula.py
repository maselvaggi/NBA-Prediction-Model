#%%
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.stats import truncnorm
import statsmodels.api as sm
import time


"""
This code is from the proof of concept model. This needs to be integrated
with the new code.  This code will be used to run the first backtest.

- Make sure drtg_mean is calculated.
"""
#%%
def get_truncated_normal(mean=1, sd=1, low=0.5, upp=1.5):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

X = get_truncated_normal(mean=1, sd=1, low= 0.5, upp= 1.5)
X.rvs()

def def_truncated_normal(mean=1, sd=1, low=0.95, upp=1.05):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

Y = def_truncated_normal(mean=1, sd=1, low=0.95, upp=1.05)
Y.rvs()

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
    
    final_odds = f"Home bettings odds, {home} ({home_spread}), Implied Prob: {implied_home}%, Decimal: {decimal_home}, USA Odds: {american_home}. Away bettings odds, {away}, Implied Prob: {implied_away}%, Decimal: {decimal_away}, USA Odds: {american_away}."
    
    return final_odds

#%%
def Minutes(mpg, rotation_size):
    add_mins = sum(mpg[-(len(mpg)-rotation_size):]) #sum mins from players not in rotation_size
    
    #First Adjustment
    mpg = mpg[0:rotation_size]
    add_mins = add_mins/len(mpg)
    mpg = mpg + add_mins
    
    bench_initial = sum(mpg[5:])
    excess_mins = sum(mpg) - 240
    avg_deduct = excess_mins/len(mpg)
    starter_deduct = avg_deduct/2
    
    #Final Deduction for starters
    mpg[:5] = mpg[:5] - starter_deduct
    
    bench_players = len(mpg)-5
    num = (sum(mpg[:5]) + bench_initial) -240 #finding number to divide from using bench_players
    bench_deduct = num/bench_players
    mpg[5:] = mpg[5:]-bench_deduct
    
    return mpg

#%%
def points_home(proj_pts_home, mpg_home, ppm_home, drtg_bos):
    for i in range(len(proj_pts_home)):
        proj_pts_home[i] = (mpg_home[i]*ppm_home[i]*X.rvs()) * ((drtg_bos/drtg_mean)*Y.rvs())
    
    return sum(proj_pts_home) + 1.5
    
    
    
def points_away(proj_pts_away, mpg_away, ppm_away, drtg_bkn):
    for i in range(len(proj_pts_away)):
        proj_pts_away[i] = (mpg_away[i]*ppm_away[i]*X.rvs()) * ((drtg_bkn/drtg_mean)*Y.rvs())
    
    return sum(proj_pts_away) - 1.5   


#%%
def drtg_home(drtg_bkn, mpg_home, bkn_drtg, rotation_size_home):
    for i in range(rotation_size_home):
        drtg_bkn[i] = (mpg_home[i]/240)*bkn_drtg[i]
    
    return sum(drtg_bkn)
    
    
def drtg_away(drtg_bos, mpg_away, bos_drtg, rotation_size_away): 
    for i in range(rotation_size_away):
        drtg_bos[i] = (mpg_away[i]/240)*bos_drtg[i]
    
    return sum(drtg_bos)

#%%
def official_projections(home, injury_report_home, rotation_size_home, away, injury_report_away, rotation_size_away):
    bkn = data.loc[data['TEAM'] == home]
    bkn = bkn.sort_values(by='MPG', ascending=False)
    if injury_report_home != []:
        bkn = bkn[~bkn['NAME'].isin(injury_report_home)] #returns all rows not including those in injury report
        
    bkn["DRtg"] = bkn["DRtg"].fillna(drtg_mean)
    bkn_drtg = bkn["DRtg"][0:rotation_size_home].to_numpy()    
    
    bos = data.loc[data['TEAM'] == away]
    bos = bos.sort_values(by='MPG', ascending=False)
    if injury_report_away != []:
        bos = bos[~bos['NAME'].isin(injury_report_away)] #returns all rows not including those in injury report
        
    bos["DRtg"] = bos["DRtg"].fillna(drtg_mean)
    bos_drtg = bos["DRtg"][0:rotation_size_away].to_numpy()    
        
    mpg_home = bkn['MPG'].to_numpy()
    mpg_away = bos['MPG'].to_numpy()
    
    mpg_home = Minutes(mpg_home, rotation_size_home)
    mpg_away = Minutes(mpg_away, rotation_size_away)
    
    ppm_home = bkn["PPM"][0:rotation_size_home].to_numpy()
    ppm_away = bos["PPM"][0:rotation_size_away].to_numpy()
    
    drtg_bkn = np.full(rotation_size_home,0)
    drtg_bkn = drtg_home(drtg_bkn, mpg_home, bkn_drtg, rotation_size_home)
    drtg_bos = np.full(rotation_size_away,0)
    drtg_bos = drtg_home(drtg_bos, mpg_away, bos_drtg, rotation_size_away)
    
    proj_pts_home = np.full(rotation_size_home,0)
    proj_pts_away = np.full(rotation_size_away,0)

    HMPTS = points_home(proj_pts_home, mpg_home, ppm_home, drtg_bos)
    AWPTS = points_away(proj_pts_away, mpg_away, ppm_away, drtg_bkn)
    

    return HMPTS, AWPTS
    
def matchup(home, injury_report_home, rotation_size_home, away, injury_report_away, rotation_size_away):
    t0 = time.time()
    proj_away = np.full(1500,1.0)
    proj_home = np.full(1500,1.0)

    for i in range(len(proj_away)):
        proj_home[i], proj_away[i] = official_projections(home, injury_report_home, rotation_size_home, away, injury_report_away, rotation_size_away)
        
    df_outcomes = pd.DataFrame(data=[proj_home, proj_away]).T
    df_outcomes.columns = ("Home", "Away")
    df_outcomes = df_outcomes.drop(df_outcomes[df_outcomes["Home"] == df_outcomes["Away"]].index)    
    
    game_odds = odds(df_outcomes, away, home)
    
    t1 = time.time()

    total = t1-t0

    return game_odds, total
