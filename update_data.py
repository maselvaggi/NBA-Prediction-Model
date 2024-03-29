#%%
from rotation_size import *
from espn_game_info import *
from update_statistics import *
#%%
def run_updates(adv_year: int = 0, adv_pages: int = 0, all_adv_pages: bool = False,
                trad_year: int = 0, trad_pages: int = 0, all_trad_pages: bool = False,
                seasonal_stats_year: int = 0, get_all_seasonal_stats: bool = False, 
                espn_game_info_year: int = 0, get_all_espn_game_info: bool = False):
    '''
    This function is meant to be the only piece of code that the user will need to execute. 

    As of right now, this function will:
    - gather all advanced/traditional player statistics from NBA.com
    - build a schedule of all games played
    - calculate seasonal stats for each player for each day of the regular season
    - grab additional game information from ESPN.com.  
    
    In the future, this function will be able to run the entire model for you. I am currently 
    building towards that.
    '''
    #Advanced, Traditional, Seasonal stats
    print(update_adv_and_trad_stats(adv_year, adv_pages, all_adv_pages, 
                                    trad_year, trad_pages, all_trad_pages, 
                                    seasonal_stats_year, get_all_seasonal_stats))

    #ESPN Game Information
    print(update_espn_game_info(espn_game_info_year, get_all_espn_game_info))

    #update rotation size file
    print(get_team_rotations(adv_year))

    return f"Updates are complete."
# %%
run_updates(adv_year=2024, adv_pages=5, trad_year=2024, trad_pages=5, seasonal_stats_year=2024, espn_game_info_year=2024)
# %%
