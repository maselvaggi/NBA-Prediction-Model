#%%
import pandas as pd
import numpy as np
from tqdm import tqdm

#%%
def create_active_rosters(year):
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
        date = dates[i].replace('/', '_')
        active_roster.to_csv(f"output/{year}/Active Rosters/{date}.csv")


    return active_roster

#%% Not in Use
# def car():
#     traditional = pd.read_csv('output/Traditional.csv', index_col=0)
#     injury_data = pd.read_csv('output/Injury_Data.csv', index_col=0)

#     dates = traditional['Date'].unique()
#     dates = dates[:132]

#     file_names = []
#     for i in dates:
#         file_names.append(''.join([i.replace('/', '_'),'.csv']))

#     stats_directory = 'output/Seasonal Stats'
#     for i in tqdm(range(len(dates))):
#         file = file_names[i]
#         location = '/'.join([stats_directory, file])
#         season_stats = pd.read_csv(location)
#         season_stats = season_stats.sort_values(by = 'Mins', ascending = False)

#         players_in  = traditional[traditional['Date'] == dates[i]]
#         players_out = injury_data[injury_data['Date'] == dates[i]]
#         games = traditional[traditional['Date'] == dates[i]]
#         teams = games['Team'].unique()

#         all_players_in, season_stats = get_players_in(players_in, season_stats, teams)
#         all_players_out = get_players_out(players_out, season_stats, teams)

#         active_rosters = pd.concat([all_players_in, all_players_out], ignore_index= True)
#         active_rosters = active_rosters.sort_values(['Team', 'Mins'], ascending = [True, False])
        
#         directory = 'output/Active Rosters'
#         name = file_names[i]
#         location = '/'.join([directory, name])
#         active_rosters.to_csv(location)

#     return True

# #%%
# car()

# #%%
# def get_players_in(players_in, season_stats, teams):

#     for i in range(len(teams)):
#         team = players_in[players_in['Team'] == teams[i]]
#         team_np = team['Name'].to_numpy()
#         player_in  = season_stats[season_stats['Team'].isin(team_np)]
#         season_stats = season_stats[~season_stats['Name'].isin(team_np)]
        
#         player_in = player_in.assign(Team = teams[i]) # New players now with correct team

#         if i != 0:
#             all_players_in = pd.concat([player_in, all_players_in], ignore_index= True)
#         else:
#             all_players_in = player_in

#     all_players_in = all_players_in.sort_values(by = 'Mins', ascending=False)

#     return all_players_in, season_stats
# #%%
# def get_players_out(players_out, season_stats, teams):

#     for i in range(len(teams)):
#         team = players_out[players_out['Team'] == teams[i]]
#         team_np = team['Name'].to_numpy()

#         player_out = season_stats[season_stats['Name'].isin(team_np)]
#         season_stats = season_stats[~season_stats['Name'].isin(team_np)]

#         player_out_np = player_out['Name'].to_numpy()

#         team = team[~team['Name'].isin(player_out_np)]

#         if len(team) != 0:
#             team_np = team['Name'].to_numpy()
#             for j in range(len(team_np)):
#                 check_player = season_stats[season_stats['Name'].str.contains(team_np[j])]

#                 if len(check_player) == 0:
#                     pass
#                 elif len(check_player) == 1:
#                     player_out = pd.concat([player_out, check_player], ignore_index=True)
#                     season_stats = season_stats[~season_stats['Name'].str.contains(team_np[j])]
#                 else:
#                     guy = check_player.head(1)
#                     player_out = pd.concat([player_out,guy], ignore_index=True)

#                     name = list(guy['Name'].iloc[0])
#                     season_stats = season_stats[~season_stats['Name'].isin(name)]

#         else:
#             pass

#         player_out = player_out.assign(Team = teams[i])

#         if i !=0:
#             all_players_out = pd.concat([player_out, all_players_out], ignore_index=True)
#         else:
#             all_players_out = player_out

#     all_players_out = all_players_out.sort_values(by = 'Mins', ascending=False)

#     return all_players_out

#%%
if __name__ == '__main__':
    create_active_rosters()