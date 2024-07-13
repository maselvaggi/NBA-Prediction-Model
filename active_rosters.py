#%%
import pandas as pd
import numpy as np
from tqdm import tqdm

#%%
def create_active_rosters(year):
    print((f"                    {year} Active Rosters                     \n"
           f"==============================================================")) 
    players_in  = pd.read_csv(f"output/{year}/Traditional{year}.csv", index_col=0)
    players_in  = players_in[['Date', 'Team', 'Name']]
    players_out = pd.read_csv(f"output/{year}/Injury_Data{year}.csv'", index_col = 0) #works by not including the index_col = 0 only, no clue as to why
    players_out = players_out[['Date', 'Team', 'Name']]
    players_dnp = pd.read_csv(f"output/{year}/DNP{year}.csv", index_col=0)
    players_dnp = players_dnp[['Date', 'Team', 'Name']]
    schedule = pd.read_csv(f"output/{year}/Schedule{year}.csv'", index_col=0)

    dates = schedule['Date'].unique()

    for i in tqdm(range(len(dates))):
        played = players_in[players_in['Date'] == dates[i]]
        out    = players_out[players_out['Date'] == dates[i]]
        dnp    = players_dnp[players_dnp['Date'] == dates[i]]
        teams  = players_in['Team'].unique()

        for j in range(len(teams)):
            played_team = played[played['Team'] == teams[j]]
            out_team    = out[out['Team'] == teams[j]]
            dnp_team    = dnp[dnp['Team'] == teams[j]]

            if j != 0:
                active_roster = pd.concat([active_roster, played_team], ignore_index=True)
                active_roster = pd.concat([active_roster, dnp_team], ignore_index=True)
                active_roster = pd.concat([active_roster, out_team], ignore_index=True)            
            else:
                active_roster = pd.concat([played_team, dnp_team], ignore_index=True)
                active_roster = pd.concat([active_roster, out_team], ignore_index=True)

        
        active_roster = active_roster.drop_duplicates()
        active_roster.to_csv(f"output/{year}/Active Rosters/{dates[i]}.csv")


    return f"{year} active rosters are updated!"

#%%
if __name__ == '__main__':
    create_active_rosters(2024)