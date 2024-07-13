#%%
from advanced import *
from traditional import *
from seasonal_stats import *

#%%
def update_advanced_stats(adv_year, adv_pages, all_adv_pages):
    #protect against random inputs
    if type(adv_year) != int or type(adv_pages) != int:
        raise ValueError("Please enter input for adv_pages/year in the form of an integer.")    
    if adv_year != 2023 and adv_year != 2024 and adv_year != 0:
        raise ValueError(f"No Advanced Stats data for year: {adv_year}. Please use 2023 or 2024.")
    #if value is 2023 or 2024 and positive pages
    if adv_year != 0 and adv_pages != 0:
        if all_adv_pages is True:
            all_advanced_stats = scrape_all_advanced_stats(adv_year)
            all_added_entries = len(all_advanced_stats)

            create_schedule(adv_year)
            return f"All advanced stats were collected. \n{all_added_entries} entries were collected. \nThe {adv_year} season schedule has been updated."
        else:
            #if there is no file to update, must collect all data
            if os.path.exists(f"output/{adv_year}/Advanced{adv_year}.csv"):
                old_advanced_stats = pd.read_csv(f"output/{adv_year}/Advanced{adv_year}.csv")

                updated_adv_entries = len(scrape_new_advanced_stats(adv_year, adv_pages)) - len(old_advanced_stats)

                if updated_adv_entries > 0:
                    create_schedule(adv_year)
                    return f"Advanced stats file has been updated.\n{updated_adv_entries} entries were added to the Advanced stats .csv file.\nThe {adv_year} season schedule file has been updated."

                else:
                    return f"Advanced stats file was not updated, no new entries to add.\nThe {adv_year} season schedule was not updated."

            else:
                all_advanced_stats = scrape_all_advanced_stats(adv_year)
                all_added_entries = len(all_advanced_stats)
                create_schedule(adv_year)

                return f"All advanced stats were collected. \n{all_added_entries} entries were collected. \n The {adv_year} season schedule has been updated."
    #if no input, just skip
    else:
        return "No new advanced stats were collected."
    
def update_traditional_stats(trad_year, trad_pages, all_trad_pages):
    if type(trad_year) != int or type(trad_pages) != int:
        raise ValueError("Please enter input for trad_pages/year in the form of an integer.")  
    if type(all_trad_pages) != bool:
        raise ValueError("Please enter boolean input for all_trad_pages.")
    if trad_year != 2023 and trad_year != 2024 and trad_year != 0:
        raise ValueError('No traditional stats data for year provided. Please use 2023 or 2024.')

    if trad_year != 0 and trad_pages != 0:
        if all_trad_pages == True:
            all_traditional_stats = scrape_all_traditional_stats(trad_year)
            all_added_entries = len(all_traditional_stats)

            return f"All traditional stats were collected. \n{all_added_entries} entries were collected."
        else:
            if os.path.exists(f"output/{trad_year}/Traditional{trad_year}.csv"):
                old_traditional_stats = pd.read_csv(f"output/{trad_year}/Traditional{trad_year}.csv")
                new_traditional_stats = scrape_new_traditional_stats(trad_year, trad_pages)
                updated_trad_entries  = len(new_traditional_stats) - len(old_traditional_stats)

                if updated_trad_entries > 0:
                    dates_for_seasonal_stats = new_traditional_stats['Date'].unique().to_numpy()
                    return dates_for_seasonal_stats, f"Traditional stats file has been updated.\n{updated_trad_entries} entries were added to the traditional stats .csv file."
                else:
                    return "Traditional stats file was not updated, no new entries to add."
            else:
                all_traditional_stats = scrape_all_traditional_stats(trad_year)
                all_added_entries = len(all_traditional_stats)

                return f"All traditional stats have been collected.\n{all_added_entries} entries were collected."
                
    else:
        return f"No new traditional stats were collected."
    
def update_adv_and_trad_stats(adv_year, adv_pages, all_adv_pages,  trad_year, trad_pages, all_trad_pages,seasonal_stats_year, get_all_seasonal_stats, adv_dates = None, trad_dates = None):
    #Check Inputs
    if type(adv_year) != int or type(adv_pages) != int:
        raise ValueError("Please enter input for adv_pages/year in the form of an integer.")    
    if type(all_adv_pages) != bool:
        raise ValueError("Please enter boolean input for all_adv_pages.")
    if adv_year != 2023 and adv_year != 2024 and adv_year != 0:
        raise ValueError(f"No Advanced Stats data for year: {adv_year}. Please use 2023 or 2024.")
    
    if type(trad_year) != int or type(trad_pages) != int:
        raise ValueError("Please enter input for traditional pages/year in the form of an integer.")  
    if type(all_trad_pages) != bool:
        raise ValueError("Please enter boolean input for all_trad_pages.")
    if trad_year != 2023 and trad_year != 2024 and trad_year != 0:
        raise ValueError('No traditional stats data for year provided. Please use 2023 or 2024.')

    print((f"                   {adv_year} Advanced Stats                        \n"
           f"=============================================================="))
    #Start collecting specified Advanced Stats data
    if adv_year != 0:
        if all_adv_pages is True or adv_pages == 0:
            all_advanced_stats = scrape_all_advanced_stats(adv_year)
            adv_dates = all_advanced_stats['Date'].unique()

            print((f"All advanced stats were collected with {len(all_advanced_stats)} entries added to the Advanved stats .csv file.\n"))
        else:
            #if there is no file to update, must collect all data
            if os.path.exists(f"output/{adv_year}/Advanced{adv_year}.csv"):
                old_advanced_stats  = pd.read_csv(f"output/{adv_year}/Advanced{adv_year}.csv")
                scrape_new_advanced_stats(adv_year, adv_pages)
                
                new_advanced_stats  = pd.read_csv(f"output/{adv_year}/Advanced{adv_year}.csv")                
                updated_adv_entries = len(new_advanced_stats) - len(old_advanced_stats)

                adv_dates = new_advanced_stats['Date'].unique()

                if updated_adv_entries != 0:
                    create_schedule(adv_year)
                    print((f"The {adv_year} Advanced stats and Schedule files have been updated.\n{updated_adv_entries} entries were added to the Advanced stats .csv file.\n"))

                else:
                    adv_dates = None
                    print((f"Advanced stats file was not updated, no new entries to add.\nThe {adv_year} season schedule was not updated.\n"))

            else:
                all_advanced_stats = scrape_all_advanced_stats(adv_year)
                all_added_entries = len(all_advanced_stats)
                adv_dates = all_advanced_stats['Date'].unique()
                create_schedule(adv_year)

                print((f"All advanced stats were collected. \n{all_added_entries} entries were collected. \n The {adv_year} season schedule has been updated.\n"))


    print((f"                  {trad_year} Traditional Stats                       \n"
           f"=============================================================="))
    #Start collecting specified Traditional Stats data
    if trad_year != 0:
        if all_trad_pages == True or trad_pages == 0:
            all_traditional_stats = scrape_all_traditional_stats(trad_year)
            trad_dates = all_traditional_stats['Date'].unique()

            print((f"All traditional stats were collected. \n{len(all_traditional_stats)} entries were collected.\n"))
        else:
            if os.path.exists(f"output/{trad_year}/Traditional{trad_year}.csv"):
                old_traditional_stats = pd.read_csv(f"output/{trad_year}/Traditional{trad_year}.csv")
                new_traditional_stats = scrape_new_traditional_stats(trad_year, trad_pages)
                completed_traditional_stats = pd.read_csv(f"output/{trad_year}/Traditional{trad_year}.csv")
                updated_trad_entries  = len(completed_traditional_stats) - len(old_traditional_stats)

                if updated_trad_entries > 0:
                    trad_dates = new_traditional_stats['Date'].unique()
                    print((f"Traditional stats file has been updated.\n{updated_trad_entries} entries were added to the traditional stats .csv file.\n"))
                else:
                    trad_dates = None
                    print((f"Traditional stats file was not updated, no new entries to add.\n"))
            else:
                all_traditional_stats = scrape_all_traditional_stats(trad_year)
                all_added_entries = len(all_traditional_stats)

                print((f"All traditional stats have been collected.\n{all_added_entries} entries were collected.\n"))
    
    #Combine dates
    if adv_dates is not None:
        if trad_dates is not None:
            all_dates = np.concatenate([adv_dates, trad_dates])
            all_dates = np.unique(all_dates)

            seasonal_stats_message = update_seasonal_stats(seasonal_stats_year, get_all_seasonal_stats, all_dates)
        else:
            seasonal_stats_message = update_seasonal_stats(seasonal_stats_year, get_all_seasonal_stats, adv_dates)
    else:
        if trad_dates is not None:
            seasonal_stats_message = update_seasonal_stats(seasonal_stats_year, get_all_seasonal_stats, trad_dates)
        else:
            print((f"                    {seasonal_stats_year} Seasonal Stats                       \n"
                   f"=============================================================="))
            seasonal_stats_message = f"No seasonal stats to update. No dates provided.\n"
    
    return seasonal_stats_message
    
def update_seasonal_stats(seasonal_stats_year, get_all_seasonal_stats, dates_to_update=None):
    print((f"                      {seasonal_stats_year} Seasonal Stats                       \n"
           f"=============================================================="))
    if dates_to_update is None and get_all_seasonal_stats is False:
        return "No seasonal stat files to update.\n"
    if type(seasonal_stats_year) != int:
        raise ValueError("Please enter input in the form of an integer.")  
    if type(get_all_seasonal_stats) != bool:
        raise ValueError("Please enter boolean input for get_all_seasonal_stats.")
    if seasonal_stats_year != 2023 and seasonal_stats_year != 2024 and seasonal_stats_year != 0:
        raise ValueError('No traditional stats data for year provided. Please use 2023 or 2024.')
    if seasonal_stats_year == 0:
        return "There were no updates made to the seasonal stats files.\n"
    
    files_updated = 0
    traditional = pd.read_csv(f"output/{seasonal_stats_year}/Traditional{seasonal_stats_year}.csv", index_col = 0)
    advanced    = pd.read_csv(f"output/{seasonal_stats_year}/Advanced{seasonal_stats_year}.csv", index_col = 0)

    if get_all_seasonal_stats is True:
        dates = advanced['Date'].unique()

        for i in tqdm(range(2, len(dates))):
            #grab all data up to but not including the date selected.
            trad_marker = traditional[traditional['Date'] == dates[-i]].index
            partial_traditional_stats = traditional.iloc[trad_marker[-1]+1:]

            adv_marker = advanced[advanced['Date'] == dates[-i]].index
            partial_advanced_stats = advanced.iloc[adv_marker[-1]+1:]
            daily_seasonal_stats(partial_advanced_stats, partial_traditional_stats, dates[-i], seasonal_stats_year)

            files_updated += 1

        return f"There were {files_updated} files updated in the {seasonal_stats_year} season stats folder.\n"
    else:
        for i in tqdm(range(len(dates_to_update))):
            #grab all data up to but not including the date selected.
            trad_marker = traditional[traditional['Date'] == dates_to_update[-i]].index
            partial_traditional_stats = traditional.iloc[trad_marker[-1]+1:]

            adv_marker = advanced[advanced['Date'] == dates_to_update[-i]].index
            partial_advanced_stats = advanced.iloc[adv_marker[-1]+1:]
            daily_seasonal_stats(partial_advanced_stats, partial_traditional_stats, dates_to_update[-i], seasonal_stats_year)

            files_updated += 1            

        return f"There were {files_updated} files updated in the {seasonal_stats_year} season stats folder.\n"

#%%
if __name__=="__main__":
    update_adv_and_trad_stats()
    update_seasonal_stats()