#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

from tqdm import tqdm
from rf_formula import create_inputs
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.metrics import accuracy_score



#%%
def lr_test(year, gp_weights):
    '''
    Using the same inputs as the RF model, we just use a Logistic Regression to
    predict the outcomes of games.  

    This model goes through 100 random states to ensure diverse sampling.
    '''
    schedule = pd.read_csv('output/{num}/Schedule2223.csv'.format(num = year), index_col=0)
    day      = schedule[schedule['Date'] == '11/20/2022'].index
    schedule = schedule.loc[:day[-1]]
    dates = schedule['Date'].unique()
    matchups = pd.read_csv('output/{num}/Caesars_Lines.csv'.format(num = year), index_col=0)
    day      = matchups[matchups['Date'] == '11/20/2022'].index
    matchups = matchups.iloc[day[0]:]
    matchup_dates = matchups['Date'].unique()

    dates = schedule['Date'].unique()
    dates = list(dates)
    dates.reverse()
    sched_dates = dates

    csr = []
    for i in range(len(matchups['Home'])):
        if matchups['Home'].iloc[i] == matchups['Favorite'].iloc[i]:
            csr.append('W')
        else:
            csr.append('L')

    csr = np.array(csr)
    matchups['CS Result'] = csr

    for i in range(len(dates)):
        date = dates[i].split('/')
        if date[0][0] == '0':
            date[0] = date[0].replace('0', '')
        if date[1][0] == '0':
            date[1] = date[1].replace('0', '')

        date = '_'.join([date[0], date[1], date[2]])
        date = ''.join([date, '.csv'])
        dates[i] = date

    for a in range(len(dates)):
        directory = 'output/{num}/Seasonal Stats/'.format(num = year)
        location = ''.join([directory, dates[a]])
        rf = pd.read_csv(location, index_col=0)
        mins = rf['Mins'].to_numpy()
        gp   = rf['GP'].to_numpy()
        ppm  = rf['PPM'].to_numpy()
        drtg = rf['DEFRTG'].to_numpy()

        total_mins = gp*mins
        sum_mins   = sum(total_mins)

        avg_ppm = 0
        for b in range(len(total_mins)):
            temp = ppm[b]*(total_mins[b]/sum_mins)
            avg_ppm = temp + avg_ppm

        avg_drtg = 0
        for b in range(len(total_mins)):
            temp = drtg[b]*(total_mins[b]/sum_mins)
            avg_drtg = temp + avg_drtg    
        
        avg_gp  = gp.mean()
        avg_mpg = sum_mins/len(total_mins)
        avg_mpg = avg_mpg/avg_gp

        sie = []

        for b in range(len(mins)):
            player_gp   = gp[b]/avg_gp
            player_mpg  = mins[b]/avg_mpg
            player_ppm  = ppm[b]/avg_ppm
            if drtg[b] == 0:
                player_drtg = 0
            else:
                player_drtg = avg_drtg/drtg[b]

            player_metric = (player_gp*gp_weights) + (player_mpg*((1-gp_weights)/3)) + (player_ppm*((1-gp_weights)/3)) + (player_drtg*((1-gp_weights)/3))
            sie.append(player_metric)

        rf['SIM'] = sie
        rf.to_csv(location)


    data = create_inputs()
    data_dates = data['Date'].unique()

    for a in range(len(sched_dates)):

        sched_date = sched_dates[a].replace('.csv', '').replace('_', '/')       
        sched_date = sched_date.split('/')

        if len(sched_date[0]) == 1:
            sched_date[0] = ''.join(['0', sched_date[0]])
        if len(sched_date[1]) == 1:
            sched_date[1] = ''.join(['0', sched_date[1]])

        sched_date = '/'.join([sched_date[0], sched_date[1], sched_date[2]])

        partial_inputs = data[data['Date'] == data_dates[a]]
        partial_sched  = schedule[schedule['Date'] == sched_date]
        partial_cs     = matchups[matchups['Date'] == matchup_dates[a]]

        partial_inputs, partial_sched, partial_cs = partial_inputs.sort_values(by='Home', ascending=True), partial_sched.sort_values(by='Team', ascending=True), partial_cs.sort_values(by='Home', ascending=True)

        results = partial_sched['Result'].to_numpy()
        partial_inputs['Actual Result'] = list(results)
        cs_results = partial_cs['CS Result'].to_numpy()
        partial_inputs['CS Result'] = cs_results
        
        
        if a != 0:
            final_inputs = pd.concat([final_inputs, partial_inputs], ignore_index=True)
        else:
            final_inputs = partial_inputs

    final_inputs.to_csv('output/{num}/LR Final Inputs.csv'.format(num = year))

    X = final_inputs.drop(['Date', 'Home', 'Away', 'Home Points', 'Away Points', 'Actual Result', 'CS Result'], axis = 1)
    y = final_inputs['Actual Result']

    accuracy = []
    cs_accuracy = []
    for a in tqdm(range(0,100)):
        x_train, x_test, y_train, y_test = train_test_split(X, y, train_size = 0.7, random_state = a)

        # restructure data for input into model
        y_train = y_train.values.ravel()
        y_test = y_test.values.ravel()

        # train model
        reg = LogisticRegression(random_state=0)
        reg.fit(x_train, y_train)

        state_accuracy = []
        state_cs_accuracy = []
        n_iterations = 1000
        for i in range(n_iterations):
            X_bs, y_bs = resample(x_train, y_train, replace=True)
            indexes = X_bs.index.values
            data = final_inputs.loc[indexes]
            cs_picks = data['CS Result']

            # make predictions
            y_hat = reg.predict(X_bs)

            # evaluate model
            score = accuracy_score(y_bs, y_hat)
            cs_score = accuracy_score(y_bs, cs_picks)
            state_accuracy.append(score)
            state_cs_accuracy.append(cs_score)
        
        accuracy.append(statistics.mean(state_accuracy))
        cs_accuracy.append(statistics.mean(state_cs_accuracy))

    # plot distribution of accuracy
    # sns.kdeplot(accuracy)
    # sns.kdeplot(cs_accuracy)
    # plt.title("Accuracy across 1000 bootstrap samples of the held-out test set")
    # plt.xlabel("Accuracy")
    # plt.show()

    results = pd.DataFrame(data = [accuracy, cs_accuracy]).T

    results.columns = ['Model', 'CS']
    results.to_csv('output/{num}/LR Test Results/Accuracy.csv'.format(num = year))

    return results

#%%
'''
This code is from the original model.  This code calculates team projected points for a given game
and team Defensive Ratings. 

Team As PPG and Team Bs DRTG are compared to create Team As final projected points.
Same goes for Team B.
'''
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

def player_impact_estimator(mpg, proj_pie, pie):
    for i in range(len(proj_pie)):
        proj_pie[i] = (mpg[i]*pie[i])
    
    return sum(proj_pie) 

def points_home(proj_pts_home, mpg_home, ppm_home):
    for i in range(len(proj_pts_home)):
        proj_pts_home[i] = (mpg_home[i]*ppm_home[i]) 
    
    return sum(proj_pts_home) + 1.5    
    

def points_away(proj_pts_away, mpg_away, ppm_away):
    for i in range(len(proj_pts_away)):
        proj_pts_away[i] = (mpg_away[i]*ppm_away[i])
    
    return sum(proj_pts_away) - 1.5   


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
    
    drtg_bkn = np.full(int(home_rotation),0.0)
    drtg_bkn = drtg_home(drtg_bkn, mpg_home, bkn_drtg, home_rotation)
    drtg_bos = np.full(int(away_rotation),0.0)
    drtg_bos = drtg_away(drtg_bos, mpg_away, bos_drtg, away_rotation)

    ppm_home = bkn["PPM"][0:int(home_rotation)].to_numpy()
    ppm_away = bos["PPM"][0:int(away_rotation)].to_numpy()    
    
    proj_pts_home = np.full(int(home_rotation),0.0)
    proj_pts_away = np.full(int(away_rotation),0.0)

    home_pts = points_home(proj_pts_home, mpg_home, ppm_home)
    away_pts = points_away(proj_pts_away, mpg_away, ppm_away)

    proj_pie_home = np.full(int(home_rotation),0.0)
    proj_pie_away = np.full(int(away_rotation),0.0)

    pie_home = bkn["SIM"][0:int(home_rotation)].to_numpy()
    pie_away = bos["SIM"][0:int(away_rotation)].to_numpy()    

    home_pie = player_impact_estimator(mpg_home, proj_pie_home, pie_home)    
    away_pie = player_impact_estimator(mpg_away, proj_pie_away, pie_away)

    return home_pts, drtg_bkn, home_pie, away_pts, drtg_bos, away_pie
    

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
    home_pts, home_def, home_pie, away_pts, away_def, away_pie = official_projections(season_stats, home, injuries_home, home_rotation, away, injuries_away, away_rotation)   
        
    return home, home_pts, home_def, home_pie, away, away_pts, away_def, away_pie


#%%
if __name__ == '__main__':
    lr_test()