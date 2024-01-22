#%%
import pandas as pd
from seasonal_stats import *
from formula import *
from tqdm import tqdm



# %%
def backtest(year):
    """
    This file is not in use.
    
    """
    schedule = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
    rotations= pd.read_csv(f"output/{year}/Rotations{year}.csv", index_col = 0)
    matchups = pd.read_csv(f"output/{year}/Caesars_Lines{year}.csv", index_col=0)
    day      = matchups[matchups['Date'] == '11/20/2022'].index
    matchups = matchups.iloc[day[0]:]
    injuries = pd.read_csv(f"output/{year}/Injury_Data{year}.csv", index_col = 0)
    directory = f"output/{year}/Model Predictions"

    for i in tqdm(range(len(matchups))): #len(matchups))):
        caesars_favorite, caesars_spread = matchups['Favorite'].iloc[i], matchups['Spread'].iloc[i]
        date, home, away = matchups['Date'].iloc[i], matchups['Home'].iloc[i], matchups['Away'].iloc[i]
        
        date = date.split('/')
        if date[0][0] == '0':
            date[0] = date[0].replace('0', '')
            date = '/'.join([date[0], date[1], date[2]])
        else:
            date = '/'.join([date[0], date[1], date[2]])

        home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away = matchup(home, away, date, schedule, rotations, injuries)
        prediction = [home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away, caesars_favorite, caesars_spread]

        prediction = [date, home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away, caesars_favorite, caesars_spread]
        prediction = pd.DataFrame(data = prediction).T
        prediction.columns = ['Date', 'Home', 'Home Spread', 'Implied Home Win %', 'Decimal Home', 'American Home', 'Away', 'Implied Away Win %', 'Decimal Away', 'American Away', "Caesar's Favorite", "Caesar's Spread"]
        if i != 201:
            prediction = [date, home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away, caesars_favorite, caesars_spread]
            prediction = pd.DataFrame(data = prediction).T
            prediction.columns = ['Date', 'Home', 'Home Spread', 'Implied Home Win %', 'Decimal Home', 'American Home', 'Away', 'Implied Away Win %', 'Decimal Away', 'American Away', "Caesar's Favorite", "Caesar's Spread"]
            final_lines = pd.concat([final_lines, prediction], ignore_index=True)
        else:
            prediction = [date, home, home_spread, implied_home, decimal_home, american_home, away, implied_away, decimal_away, american_away, caesars_favorite, caesars_spread]
            prediction = pd.DataFrame(data = prediction).T
            prediction.columns = ['Date', 'Home', 'Home Spread', 'Implied Home Win %', 'Decimal Home', 'American Home', 'Away', 'Implied Away Win %', 'Decimal Away', 'American Away', "Caesar's Favorite", "Caesar's Spread"]
            final_lines = prediction
        if i == 100:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)        
        elif i == 200:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 300:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 400:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 500:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 600:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 700:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 800:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)
        elif i == 900:
            num = str(i)
            location = ''.join([directory, num, '.csv'])
            final_lines.to_csv(location)


    final_lines.to_csv(f"output/{year}/Model Predictions{year}.csv")
    return final_lines
#%%
formula_predictions = backtest()

#%%
results = pd.read_csv('output/{num}/Model Predictions{num}.csv'.format(num = year), index_col=0)
results

correct = 0
for i in range(len(results['Home Spread'])):
    if results['Home Spread'].iloc[i] < 0:
        if results['Home'].iloc[i] == results["Caesar's Favorite"].iloc[i]:
            correct += 1
    elif results['Home Spread'].iloc[i] > 0:
        if results['Away'].iloc[i] == results["Caesar's Favorite"].iloc[i]:
            correct +=1

correct/len(results)

#%%
schedule =  pd.read_csv('output/Schedule2223.csv', index_col = 0)
results = pd.read_csv('output/Model Predictions.csv', index_col=0)

#%%
dates = results['Date'].unique()

for i in range(len(dates)):

    index_date = dates[i].split('/')
    if len(index_date[0]) == 1:
        index_date[0] = ''.join(['0', index_date[0]])
    if len(index_date[1]) == 1:
        index_date[1] = ''.join(['0', index_date[1]])
    index_date = '/'.join([index_date[0], index_date[1], index_date[2]])

    temp = results[results['Date'] == dates[i]]
    temp = temp.sort_values(by = 'Home')
    temp_schedule = schedule[schedule['Date'] == index_date]
    temp_schedule = temp_schedule.sort_values(by = 'Team')

    # if dates[i] == '12/17/2022':
    #     remove = ['PHX', 'OKC', 'HOU', 'MIL']
    #     temp_schedule = temp_schedule[~temp_schedule['Team'].isin(remove)]
 
    game_result = []
    for j in range(len(temp_schedule)):
        game_result.append(temp_schedule['Result'].iloc[j])

    temp['Home Result'] = game_result

    if i !=0:
        full_results = pd.concat([full_results, temp], ignore_index=True)
    else:
        full_results = temp

full_results

#%%
my_model_correct = 0
Caesars_correct = 0

for i in range(len(full_results['Home'])):
    if full_results['Implied Home Win %'].iloc[i] > 50 and full_results['Home Result'].iloc[i] == 'W':
        my_model_correct +=1
    elif full_results['Implied Home Win %'].iloc[i] < 50 and full_results['Home Result'].iloc[i] == 'L':
        my_model_correct +=1

for i in range(len(full_results["Caesar's Spread"])):
    if full_results["Caesar's Favorite"].iloc[i] == full_results["Home"].iloc[i]:
        if full_results['Home Result'].iloc[i] == 'W':
            Caesars_correct += 1
    elif full_results["Caesar's Favorite"].iloc[i] == full_results["Away"].iloc[i]:
        if full_results['Home Result'].iloc[i] == 'L':
            Caesars_correct += 1

my_model_correct/len(full_results['Home']), Caesars_correct/len(full_results['Home'])
#%%
full_results

#%%
matchups = pd.read_csv('output/Caesars_Lines.csv', index_col=0)
date = matchups['Date'].iloc[586]
date = date.split('/')
if date[0][0] == '0':
    date[0] = date[0].replace('0', '')
    date = '/'.join([date[0], date[1], date[2]])

date

#%%
#date = matchups['Date'].iloc[586]
date = '1/2/2023'

index_date = date.split('/')
if len(index_date[0]) == 1:
    index_date[0] = ''.join(['0', index_date[0]])
if len(index_date[1]) == 1:
    index_date[1] = ''.join(['0', index_date[1]])
index_date = '/'.join([index_date[0], index_date[1], index_date[2]])
day = schedule[schedule['Date'] == index_date].index
day
#%%
schedule = schedule.iloc[day[-1]+1:]

schedule

#%%
directory = 'output/Model Predictions '
end = '.csv'

for i in range(2,8):
    version = str(i)
    location = ''.join([directory, version, end])
    temp = pd.read_csv(location, index_col=0)

    if i != 2:
        combined_results = pd.concat([combined_results, temp], ignore_index= True)
    else:
        combined_results = temp

combined_results

#%%
dates = combined_results['Date'].unique()

for i in range(len(dates)):
    print(dates[i])
    index_date = dates[i].split('/')
    if len(index_date[0]) == 1:
        index_date[0] = ''.join(['0', index_date[0]])
    if len(index_date[1]) == 1:
        index_date[1] = ''.join(['0', index_date[1]])
    index_date = '/'.join([index_date[0], index_date[1], index_date[2]])

    temp = combined_results[combined_results['Date'] == dates[i]]
    temp = temp.sort_values(by = 'Home')
    temp_schedule = schedule[schedule['Date'] == index_date]
    temp_schedule = temp_schedule.sort_values(by = 'Team')

    if dates[i] == '12/30/2022':
        team = ['ORL']
        temp_schedule = temp_schedule[~temp_schedule['Team'].isin(team)]
    elif dates[i] == '3/10/2023':
        team = ['SAS', 'LAL', 'MIN', 'MIA']
        temp_schedule = temp_schedule[~temp_schedule['Team'].isin(team)]

    game_result = []
    for j in range(len(temp_schedule)):
        game_result.append(temp_schedule['Result'].iloc[j])

    temp['Home Result'] = game_result

    if i !=0:
        full_results = pd.concat([full_results, temp], ignore_index=True)
    else:
        full_results = temp


#%%
primary = pd.read_csv('output/Model Predictions.csv', index_col=0)
dates = primary['Date'].unique()

for i in range(len(dates)):
    print(dates[i])
    index_date = dates[i].split('/')
    if len(index_date[0]) == 1:
        index_date[0] = ''.join(['0', index_date[0]])
    if len(index_date[1]) == 1:
        index_date[1] = ''.join(['0', index_date[1]])
    index_date = '/'.join([index_date[0], index_date[1], index_date[2]])

    temp = primary[primary['Date'] == index_date]
    temp = temp.sort_values(by = 'Home')
    temp_schedule = schedule[schedule['Date'] == index_date]
    temp_schedule = temp_schedule.sort_values(by = 'Team')

    game_result = []
    for j in range(len(temp_schedule)):
        game_result.append(temp_schedule['Result'].iloc[j])

    temp['Home Result'] = game_result

    if i !=0:
        first_full_results = pd.concat([first_full_results, temp], ignore_index=True)
    else:
        first_full_results = temp

first_full_results
#%%
first_full_results = pd.read_csv('output/Model Predictions.csv', index_col=0)


full_results = pd.concat([first_full_results, full_results], ignore_index=True)
full_results
#%%
full_results.to_csv('output/Model Predictions.csv')

#%% '3/23/2023', '3/24/2023','3/25/2023', '3/26/2023', '3/27/2023', '3/28/2023', '3/29/2023','3/30/2023', '3/31/2023', '4/1/2023', '4/2/2023','4/3/2023', '4/4/2023', '4/5/2023', '4/6/2023',  
dates = ['4/7/2023','4/8/2023', '4/9/2023']
semi = full_results #[~full_results['Date'].isin(dates)]
semi
# %%
correct = 0
for i in range(len(semi['Home Spread'])):
    if semi['Home Spread'].iloc[i] < 0:
        if semi['Home'].iloc[i] == semi["Caesar's Favorite"].iloc[i]:
            correct += 1
    elif semi['Home Spread'].iloc[i] > 0:
        if semi['Away'].iloc[i] == semi["Caesar's Favorite"].iloc[i]:
            correct +=1

agree_with_Caesars = correct/len(semi['Home'])
agree_with_Caesars

#%%
my_model_correct = 0
Caesars_correct = 0

for i in range(len(semi['Home'])):
    if semi['Implied Home Win %'].iloc[i] > 50 and semi['Home Result'].iloc[i] == 'W':
        my_model_correct +=1
    elif semi['Implied Home Win %'].iloc[i] < 50 and semi['Home Result'].iloc[i] == 'L':
        my_model_correct +=1

for i in range(len(semi["Caesar's Spread"])):
    if semi["Caesar's Favorite"].iloc[i] == semi["Home"].iloc[i]:
        if semi['Home Result'].iloc[i] == 'W':
            Caesars_correct += 1
    elif semi["Caesar's Favorite"].iloc[i] == semi["Away"].iloc[i]:
        if semi['Home Result'].iloc[i] == 'L':
            Caesars_correct += 1

my_model_correct/len(semi['Home']), Caesars_correct/len(semi['Home'])

# %%
