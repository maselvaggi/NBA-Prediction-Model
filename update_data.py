#%%
import os.path

from advanced import *
from traditional import *
from caesars_odds import *
from schedule import *
#%%

def run_updates(adv_year: int = 0, adv_pages: int = 0, all_adv_pages: bool = False, trad_year: int = 0, trad_pages: int = 0, all_trad_pages: bool = False):
    #Advanced stats
    adv_message = update_advanced_stats(adv_year, adv_pages, all_adv_pages)
    print(adv_message)

    #Traditional Stats    
    trad_message = update_traditional_stats(trad_year, trad_pages, all_trad_pages)
    print(trad_message)

    return 'Updates are complete.'

def update_advanced_stats(adv_year, adv_pages, all_adv_pages):
    #protect against random inputs
    if adv_year != 2023 and adv_year != 2024 and adv_year != 0:
        raise ValueError('No Advanced Stats data for year: {num}. Please use 2023 or 2024.'.format(num = adv_year))
    #if value is 2023 or 2024 and positive pages
    if adv_year != 0 and adv_pages != 0:
        if all_adv_pages == True:
            all_advanced_stats = scrape_all_ADV(adv_year)
            all_added_entries = len(all_advanced_stats)

            create_schedule(adv_year)
            return "All advanced stats were collected. \n {num} entries were collected. \n The {year} season schedule has been updated.".format(num = all_added_entries, year = adv_year)
        else:
            #if there is no file to update, must collect all data
            if os.path.exists('output/{num}/Advanced{num}.csv'.format(num = adv_year)):
                old_advanced_stats = pd.read_csv('output/{num}/Advanced{num}.csv'.format(num = adv_year))
                old_advanced_stats = len(old_advanced_stats)

                new_advanced_stats = scrape_new_ADV(adv_year, adv_pages)
                new_advanced_stats = len(new_advanced_stats)
                updated_adv_entries = new_advanced_stats - old_advanced_stats

                if updated_adv_entries > 0:
                    create_schedule(adv_year)
                    return "Advanced stats file has been updated.\n{num} entries were added to the Advanced stats .csv file.\nThe {year} season schedule file has been updated.".format(num = updated_adv_entries, year = adv_year)       

                else:
                    return "Advanced stats file was not updated, no new entries to add.\nThe {num} season schedule was not updated.".format(num = adv_year)

            else:
                all_advanced_stats = scrape_all_ADV(adv_year)
                all_added_entries = len(all_advanced_stats)
                create_schedule(adv_year)
                return "All advanced stats were collected. \n {num} entries were collected. \n The {year} season schedule has been updated.".format(num = all_added_entries, year = adv_year)

    #if not input, just skip
    else:
        return "No new advanced stats were collected."

def update_traditional_stats(trad_year, trad_pages, all_trad_pages):
    if trad_year != 2023 and trad_year != 2024 and trad_year != 0:
        raise ValueError('No traditional stats data for year provided. Please use 2023 or 2024.')

    if trad_year != 0 and trad_pages != 0:
        if all_trad_pages == True:
            all_traditional_stats = scrape_all_Trad(trad_year)
            all_added_entries = len(all_traditional_stats)

            return "All traditional stats were collected. \n {num} entries were collected.".format(num = all_added_entries)
        else:
            if os.path.exists('output/{num}/Traditional{num}.csv'.format(num = trad_year)):
                old_traditional_stats = pd.read_csv('output/{num}/Traditional{num}.csv'.format(num = trad_year))
                old_traditional_stats = len(old_traditional_stats)

                new_traditional_stats = scrape_new_Trad(trad_year, trad_pages)
                new_traditional_stats = len(new_traditional_stats)
                updated_trad_entries  = new_traditional_stats - old_traditional_stats

                if updated_trad_entries > 0:
                    return "Traditional stats file has been updated.\n{num} entries were added to the traditional stats .csv file.".format(num = updated_trad_entries)
                else:
                    return "Traditional stats file was not updated, no new entries to add."
            else:
                all_traditional_stats = scrape_all_Trad(trad_year)
                all_added_entries = len(all_traditional_stats)

                return "All traditional stats have been collected.\n{num} entries were collected.".format(num = all_added_entries)
                
    else:
        return "No new traditional stats were collected."

#%%
run_updates(adv_year = 2024, adv_pages = 1, trad_year= 2024, trad_pages= 1)

# %%
