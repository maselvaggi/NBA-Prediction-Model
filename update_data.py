#%%
from advanced import *
from schedule import *
from traditional import *
from espn_game_info import *
from seasonal_stats import *

#%%
def run_updates(adv_year: int = 0, adv_pages: int = 0, all_adv_pages: bool = False, trad_year: int = 0, trad_pages: int = 0, all_trad_pages: bool = False, seasonal_stats_year: int = 0, get_all_seasonal_stats: bool = False, espn_game_info_year: int = 0, get_all_espn_game_info: bool = False):
    '''
    This function is meant to be the only piece of code that the user will need to 
    execute to gather all data.  The end goal is to automate as much of the data collection
    as well as the model execution as possible.  

    As of right now, this function will gather all advanced/traditional player statistics from
    NBA.com.  The function also will build an NBA schedule for you as well.  
    
    This function does not gather relevant game info from ESPN.go.com- this is the next step.
    '''
    #Advanced stats
    print(update_advanced_stats(adv_year, adv_pages, all_adv_pages))

    #Traditional Stats    
    print(update_traditional_stats(trad_year, trad_pages, all_trad_pages))

    #Seasonal Stats
    print(update_seasonal_stats(seasonal_stats_year, get_all_seasonal_stats))

    #ESPN Game Information
    print(update_espn_game_info(espn_game_info_year, get_all_espn_game_info))

    return "Updates are complete."