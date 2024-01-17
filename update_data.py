#%%
from advanced import *
from traditional import *
from espn_game_info import *
from schedule import *
#%%

def run_updates(adv_year: int = 0, adv_pages: int = 0, all_adv_pages: bool = False, trad_year: int = 0, trad_pages: int = 0, all_trad_pages: bool = False, espn_game_info_year: int = 0, get_all_espn_game_info: bool = False):
    '''
    This function is meant to be the only piece of code that the user will need to 
    execute to gather all data.  The end goal is to automate as much of the data collection
    as well as the model execution as possible.  

    As of right now, this function will gather all advanced/traditional player statistics from
    NBA.com.  The function also will build an NBA schedule for you as well.  
    
    This function does not gather relevant game info from ESPN.go.com- this is the next step.
    '''
    #Advanced stats
    adv_message = update_advanced_stats(adv_year, adv_pages, all_adv_pages)
    print(adv_message)

    #Traditional Stats    
    trad_message = update_traditional_stats(trad_year, trad_pages, all_trad_pages)
    print(trad_message)

    espn_info_message = update_espn_game_info(espn_game_info_year, get_all_espn_game_info)
    print(espn_info_message)
    
    return "Updates are complete."

#%%
run_updates(adv_year = 2024, adv_pages = 1, trad_year= 2024, trad_pages= 1)
# %%
