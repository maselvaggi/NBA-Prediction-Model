#%%
import pandas as pd

#%%
def create_schedule():
    # Need advanced.csv in order to create schedule.csv
    schedule = pd.read_csv('Advanced.csv', index_col = 0)

    schedule = schedule[['Date','Team', 'Location', 'Opponent', 'Result']]
    schedule = schedule.drop_duplicates()
    schedule = schedule[schedule['Location'] == "H"]
    
    schedule.to_csv('Schedule2223.csv')
    schedule = pd.read_csv('Schedule2223.csv', index_col=0)
    
    return schedule

# %%
if __name__ == "__main__":
    create_schedule()