#%%
import pandas as pd
import numpy as np
from tqdm import tqdm
from formula import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
#%%
def create_inputs(year):
    '''
    This functions remakes the input .csv file for the model to be run.
    This just needs to be updated when factor model weights change.
    '''
    schedule = pd.read_csv('output/{num}/Schedule{num}.csv'.format(num = year), index_col = 0)
    rotations= pd.read_csv('output/{num}/Rotations{num}.csv'.format(num = year), index_col = 0)
    matchups = pd.read_csv('output/{num}/Caesars_Lines{num}.csv'.format(num = year), index_col=0)
    day      = matchups[matchups['Date'] == '11/20/2022'].index
    matchups = matchups.iloc[day[0]:]
    injuries = pd.read_csv('output/{num}/Injury_Data.csv'.format(num = year), index_col = 0)

    for i in range(len(matchups)): #len(matchups))):
        date, home, away = matchups['Date'].iloc[i], matchups['Home'].iloc[i], matchups['Away'].iloc[i]
        
        date = date.split('/')
        if date[0][0] == '0':
            date[0] = date[0].replace('0', '')
            date = '/'.join([date[0], date[1], date[2]])
        else:
            date = '/'.join([date[0], date[1], date[2]])      

        home, home_pts, home_def, home_sie, away, away_pts, away_def, away_sie = matchup(home, away, date, schedule, rotations, injuries)

        if i != 0:
            prediction = [date, home,  home_pts, home_def, home_sie, away, away_pts, away_def, away_sie]
            prediction = pd.DataFrame(data = prediction).T
            prediction.columns = ['Date', 'Home', 'Home Points', 'Home DRTG', 'Home SIE', 'Away', 'Away Points', 'Away DRTG', 'Away SIE']
            rf_inputs = pd.concat([rf_inputs, prediction], ignore_index=True)
        else:
            prediction = [date, home,  home_pts, home_def, home_sie, away, away_pts, away_def, away_sie]
            prediction = pd.DataFrame(data = prediction).T
            prediction.columns = ['Date', 'Home', 'Home Points', 'Home DRTG', 'Home SIE', 'Away', 'Away Points', 'Away DRTG', 'Away SIE']
            rf_inputs = prediction
    


    rf_inputs.to_csv('output/{num}/RF Inputs.csv'.format(num = year))

    return rf_inputs
#%%
def rf_test(year, gp_weights, rs):
    '''
    Using a Random Forest Classifier, this function predicts outcomes of games 
    given a games played weight and a random state input (both as lists). This function was 
    not modified for efficiency, but to just get results.
    '''
    schedule = pd.read_csv('output/{num}/Schedule{num}.csv'.format(num = year), index_col=0)
    day      = schedule[schedule['Date'] == '11/20/2022'].index
    schedule = schedule.loc[:day[-1]]
    dates = schedule['Date'].unique()
    matchups = pd.read_csv('output/{num}/Caesars_Lines{num}.csv'.format(num = year), index_col=0)
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


    for i in range(len(gp_weights)):

    
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

            sim = []

            for b in range(len(mins)):
                player_gp   = gp[b]/avg_gp
                player_mpg  = mins[b]/avg_mpg
                player_ppm  = ppm[b]/avg_ppm
                if drtg[b] == 0:
                    player_drtg = 0
                else:
                    player_drtg = avg_drtg/drtg[b]
                #There are 4 factors in this model, make sure they add up to 1
                player_metric = (player_gp*gp_weights[i]) + (player_mpg*((1-gp_weights[i])/3)) + (player_ppm*((1-gp_weights[i])/3)) + (player_drtg*((1-gp_weights[i])/3))
                sim.append(player_metric)

            rf['SIM'] = sim
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

        final_inputs.to_csv('output/{num}/RF Final Inputs.csv'.format(num = year))

        X = final_inputs.drop(['Date', 'Home', 'Away', 'Actual Result', 'CS Result'], axis = 1)
        y = final_inputs['Actual Result']

        for a in range(len(rs)):
            for b in tqdm(range(30, 45)): #45
                s = b/100
                for c in range(50, 151): #151
                    num = c*10
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=s, random_state=rs[a])
                    rf_model = RandomForestClassifier(n_estimators=num, max_features="auto", random_state=rs[a])
                    rf_model.fit(X_train, y_train)

                    predictions = rf_model.predict(X_test)

                    model_results = X_test
                    model_results['Predictions'] = predictions

                    indexes = model_results.index.values

                    predicted = final_inputs.loc[indexes]
                    predicted["RF Result"] = predictions

                    correct = np.where(predicted['Actual Result'] == predicted['RF Result'])
                    correct = list(correct[0])
                    rf_accuracy = len(correct)/len(predicted)

                    correct = np.where(predicted['Actual Result'] == predicted['CS Result'])
                    correct = list(correct[0])
                    cs_accuracy = len(correct)/len(predicted)                    

                    if c != 50:
                        partial_outputs = [rs[a], s,num,rf_accuracy, cs_accuracy]
                        partial_outputs = pd.DataFrame(data = partial_outputs).T
                        partial_outputs.columns = ['Random State',  'Test Size', 'N Estimators', 'RF Accuracy', 'CS Accuracy']
                        semi_outputs = pd.concat([semi_outputs, partial_outputs], ignore_index=True)
                    else:
                        partial_outputs = [rs[a], s,num,rf_accuracy, cs_accuracy]
                        partial_outputs = pd.DataFrame(data = partial_outputs).T            
                        partial_outputs.columns = ['Random State', 'Test Size', 'N Estimators', 'RF Accuracy', 'CS Accuracy']
                        semi_outputs = partial_outputs
                if b != 30:
                    outputs = pd.concat([outputs, semi_outputs], ignore_index=True)
                else:
                    outputs = semi_outputs
            
            if a != 0:
                #My device is old and kept crashing so checkpoints were added.
                weight_outputs = pd.concat([weight_outputs, outputs])
                directory = 'output/{num}/RF Test Results/'.format(num = year)
                name_1 = ''.join(['GP', str(gp_weights[i])])
                name_2 = ''.join(['RS', str(rs[a])])
                name_2 = ''.join([name_2, '.csv'])
                name   = '_'.join([name_1, name_2])

                location = ''.join([directory, name])
                weight_outputs.to_csv(location)
            else:
                weight_outputs = outputs
                directory = 'output/{num}/RF Test Results/'.format(num = year)
                name_1 = ''.join(['GP', str(gp_weights[i])])
                name_2 = ''.join(['RS', str(rs[a])])
                name_2 = ''.join([name_2, '.csv'])
                name   = '_'.join([name_1, name_2])

                location = ''.join([directory, name])
                weight_outputs.to_csv(location)

        directory = 'output/{num}/RF Test Results/'.format(num = year)
        name = ''.join(['GP', str(gp_weights[i]), '.csv'])
        location = ''.join([directory, name])
        weight_outputs.to_csv(location)

#%%
if __name__=='__main__':
    rf_test()
    create_inputs()
