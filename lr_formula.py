#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics

from tqdm import tqdm
from formula import *
from rf_formula import create_inputs
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.utils import resample
from sklearn.metrics import accuracy_score

#%%
def lr_test(year, gp_weights):
    '''
    Using the same inputs as the RF model, we just use a Logistic Regression to
    predict the outcomes of games.  

    This model goes through 100 random states to ensure diverse sampling.
    '''
    schedule = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col=0)
    day      = schedule[schedule['Date'] == '11/20/2022'].index
    schedule = schedule.loc[:day[-1]]
    dates = schedule['Date'].unique()
    matchups = pd.read_csv(f"output/{year}/Caesars_Lines{year}.csv", index_col=0)
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
        rf = pd.read_csv(f"output/{year}/Seasonal Stats/{dates[a]}", index_col=0)
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

        sim = []

        for b in range(len(mins)):
            player_gp   = gp[b]/avg_gp
            player_mpg  = mins[b]/avg_mpg
            player_ppm  = ppm[b]/avg_ppm
            if drtg[b] == 0:
                player_drtg = 0
            else:
                player_drtg = avg_drtg/drtg[b]

            player_metric = (player_gp*gp_weights) + (player_mpg*((1-gp_weights)/3)) + (player_ppm*((1-gp_weights)/3)) + (player_drtg*((1-gp_weights)/3))
            sim.append(player_metric)

        rf['SIM'] = sim
        rf.to_csv(f"output/{year}/Seasonal Stats/{dates[a]}")


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

    final_inputs.to_csv(f"output/{year}/LR Final Inputs.csv")

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
    results.to_csv(f"output/{year}/LR Test Results/Accuracy.csv")

    return results

#%%
if __name__ == '__main__':
    lr_test()