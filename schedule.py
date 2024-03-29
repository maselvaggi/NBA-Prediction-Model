#%%
import pandas as pd

def create_schedule(year):
    """
    This function is able to create the entire NBA season schedule using the 
    scraped data. 

    Will need to create another function to create schedule for games that 
    have not happend yet.  This would entail downloading a file from perhaps
    NBA.com and doing some data cleaning on the text.  
    """
    # Need advanced.csv in order to create schedule.csv
    schedule = pd.read_csv(f"output/{year}/Advanced{year}.csv", index_col = 0)

    schedule = schedule[['Date','Team', 'Location', 'Opponent', 'Result']]
    schedule = schedule.drop_duplicates()
    schedule = schedule[schedule['Location'] == "H"]
    schedule = schedule.reset_index(drop=True)
    
    schedule.to_csv(f"output/{year}/Schedule{year}.csv")
    schedule = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col=0)
    
    return schedule

#%%
if __name__ == "__main__":
    create_schedule()
