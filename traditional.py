#%%
import time
import os.path
import pandas as pd

from tqdm import tqdm
from selenium import webdriver
from remove_duplicates import *
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#%%
def scrape_all_traditional_stats(year):
    '''
    This function will scrape all of the player box scores from the current nba regular
    season up until today's date.  Using the ChromeDriver.exe, we are able to easily
    parse through the tables of data and save the data in a .csv file and return a 
    dataframe.
    '''
    if year == 2023 or year == '2023':
        link = 'https://www.nba.com/stats/players/boxscores-traditional?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-traditional'

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    driver.implicitly_wait(25)
    #driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/button').click()
    time.sleep(20)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/button').click()
    time.sleep(20)

    drop_down = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
    options = [x for x in drop_down.find_elements(By.TAG_NAME, "option")]
    pages = []
    for element in options:
        pages.append(element.get_attribute("value"))
        
    #Code to grab all pages of data
    tables = []

    for i in tqdm(range(1, len(pages))):
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        tables.append(text)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(1)
        
    driver.quit()
    
    with open(f'output/{year}/NewTraditionalStats{year}.txt', 'w') as file:
        for row in tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
            
    trad_all = clean_new_traditional_stats(year)
    
    df_T = pd.DataFrame(trad_all, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 
                                           'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
                                           'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
                                           'BLK', 'TOV', 'PF', 'Plusminus'])
    
    df_T[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus' ]] = df_T[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']].apply(pd.to_numeric) 
    df_T[['FG%', '3P%', 'FT%']] = df_T[['FG%', '3P%', 'FT%']].astype(float)
    
    df_T.to_csv(f'output/{year}/Traditional{year}.csv')


    return df_T

def trad_format_rows(T_box_scores):
    """
    This function formats each list eleemnt into a format that will be transformed into a dataframe
    of all traditional stat box scores.
    """
    for i in range(len(T_box_scores)):
        player = []

        #Some players have a suffix such as Jr., Sr., 'II', 'III', etc
        #When splitting each line by space, those player with a suffix
        #will have an extra element length wise
        if len(T_box_scores[i]) == 28:
            player.append(T_box_scores[i][0] + " " + T_box_scores[i][1])
            player.append(T_box_scores[i][2])

            if T_box_scores[i][4] == "@":
                player.append("A")
            else:
                player.append("H")
                
            player.append(T_box_scores[i][5])

            for j in range(6, 28):
                player.append(T_box_scores[i][j])
            T_box_scores[i] = player
        else:
            player.append(T_box_scores[i][0] + " " + T_box_scores[i][1] + " " + T_box_scores[i][2])
            player.append(T_box_scores[i][3])

            if T_box_scores[i][5] == "@":
                player.append("A")
            else:
                player.append("H")

            player.append(T_box_scores[i][6])
            for j in range(7, len(T_box_scores[i])):
                player.append(T_box_scores[i][j])
                
        T_box_scores[i] = player   
    
    return T_box_scores

def scrape_new_traditional_stats(year, pages):
    """
    This fucntion does exactly the same as scrape_all_Trad() but you can specify
    how many pages of player box scores you want to scrape.

    """

    if year == 2023 or year == '2023':
        link = 'https://www.nba.com/stats/players/boxscores-traditional?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-traditional'

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()

    time.sleep(20)        
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/button').click()
    time.sleep(20)
    
    drop_down = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
    options = [x for x in drop_down.find_elements(By.TAG_NAME, "option")]
    table_pages = []
    for element in options:
        table_pages.append(element.get_attribute("value"))

    if pages > len(table_pages):
        raise ValueError("The number of pages you entred: {num1} is greater than the number of pages available: {num2}.".format(num1 = pages, num2 = len(table_pages)))    
 
    tables = []

    for i in tqdm(range(1, pages+1)):
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        tables.append(text)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(1)
        
    driver.quit()
    
    with open(f"output/{year}/NewTraditionalStats{year}.txt", 'w') as file:
        for row in tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
            
    trad_new = clean_new_traditional_stats(year)
    
    df_T_new = pd.DataFrame(trad_new, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 
                                      'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
                                       'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
                                       'BLK', 'TOV', 'PF', 'Plusminus'])
    
    df_T_new[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus' ]] = df_T_new[['Mins', 'Points', 'FGM','FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV','PF', 'Plusminus']].apply(pd.to_numeric) 
    df_T_new[['FG%', '3P%', 'FT%']] = df_T_new[['FG%', '3P%', 'FT%']].astype(float)
    
    traditional_old = pd.read_csv(f"output/{year}/Traditional{year}.csv")
    traditional = pd.concat([df_T_new, traditional_old], ignore_index=True, sort=False)
    traditional = traditional[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'Points',
                               'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB',
                               'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']]
    traditional = traditional.drop_duplicates().reset_index()
    #keeps old indexes as column. So I'm just overwriting it in a lazy way-- look into better way
    traditional = traditional[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'Points', 
                               'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB', 
                               'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']]
    traditional = remove_duplicates(traditional)

    unique_trad_dates = traditional['Date'].unique()
    for i in range(len(unique_trad_dates)):
        if "/" not in unique_trad_dates[i]:
            pass
        else:
            fix_this_date = unique_trad_dates[i]
            fix_this_date = fix_this_date.split('/')
            fixed_date = f"{fix_this_date[2]}-{fix_this_date[0]}-{fix_this_date[1]}"

            traditional = traditional.replace(unique_trad_dates[i], fixed_date)

    traditional.to_csv(f"output/{year}/Traditional{year}.csv")
    
    return traditional    

def clean_new_traditional_stats(year):
    
    traditional = open(f"output/{year}/NewTraditionalStats{year}.txt")
    traditional = traditional.read()
    T_game_logs = traditional.split("\n")
    T_game_logs.pop()
    
    T_box_scores = []
    for i in range(len(T_game_logs)):
        T_box_scores.append(T_game_logs[i].split(" "))
    
    T_box_scores = trad_format_rows(T_box_scores)
    
    return T_box_scores

def update_traditional_stats(trad_year, trad_pages, all_trad_pages):

    if type(trad_year) != int or type(trad_pages) != int:
        raise ValueError("Please enter input in the form of an integer.")  
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
                old_traditional_stats = len(old_traditional_stats)

                new_traditional_stats = scrape_new_traditional_stats(trad_year, trad_pages)
                new_traditional_stats = len(new_traditional_stats)
                updated_trad_entries  = new_traditional_stats - old_traditional_stats

                if updated_trad_entries > 0:
                    return f"Traditional stats file has been updated.\n{updated_trad_entries} entries were added to the traditional stats .csv file."
                else:
                    return "Traditional stats file was not updated, no new entries to add."
            else:
                all_traditional_stats = scrape_all_traditional_stats(trad_year)
                all_added_entries = len(all_traditional_stats)

                return f"All traditional stats have been collected.\n{all_added_entries} entries were collected."
                
    else:
        return "No new traditional stats were collected."

# %%
if __name__ == "__main__":
    scrape_all_traditional_stats()
    scrape_new_traditional_stats()
    update_traditional_stats()
