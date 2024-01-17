#%%
import time
import os.path
import pandas as pd

from tqdm import tqdm
from schedule import *
from selenium import webdriver
from remove_duplicates import *
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import requests
#%%
def scrape_all_advanced_stats(year):
    '''
    This function will scrape all of the advavnced player box scores from the current nba regular
    season up until today's date.  Using the ChromeDriver.exe, we are able to easily
    parse through the tables of data and save the data in a .csv file and return a 
    dataframe.
    '''
    if year == 2023 or year == '2023':
        link = 'https://www.nba.com/stats/players/boxscores-advanced?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-advanced'

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    driver.implicitly_wait(25)
#    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/button').click()
    time.sleep(15)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/button').click()
    time.sleep(20)
    
    drop_down = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
    options = [x for x in drop_down.find_elements(By.TAG_NAME, "option")]
    pages = []
    for element in options:
        pages.append(element.get_attribute("value"))

    A_tables = []
    for i in tqdm(range(1, len(pages))):
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        A_tables.append(text)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(1)
    
    driver.quit()

    with open("output/{num}/NewAdvancedStats{num}.txt".format(num = year), 'w') as file:
        for row in A_tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
    
    All_adv_scores = clean_new_advanced_stats(year)
    
    df_A = pd.DataFrame(All_adv_scores, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins',
                                                 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%',
                                                 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE'])
    df_A[['Mins']] = df_A[['Mins']].apply(pd.to_numeric)
    df_A[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']] = df_A[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']].astype(float)
    df_A.to_csv('output/{num}/Advanced{num}.csv'.format(num = year))
    
    return df_A

def adv_format_rows(A_box_scores):
    """
    The newly created list of lists is then cleaned according to if the player has a suffix
    in their name or not.  The end goal is to create uniform length lists with which to create
    a dataframe to then save to a .csv. 
    """
    for i in range(len(A_box_scores)):
        player = []

        #Some players have a suffix such as Jr., Sr., 'II', 'III', etc
        #When splitting each line by space, those player with a suffix
        #will have an extra element length wise
        if len(A_box_scores[i]) == 24:
            player.append(A_box_scores[i][0] + " " + A_box_scores[i][1])
            player.append(A_box_scores[i][2])
            
            if A_box_scores[i][4] == "@":
                player.append("A")
            else:
                player.append("H")
            
            player.append(A_box_scores[i][5])
        
            for j in range(6, 24):
                player.append(A_box_scores[i][j])
            A_box_scores[i] = player
        else:
            player.append(A_box_scores[i][0] + " " + A_box_scores[i][1] + " " + A_box_scores[i][2])
            player.append(A_box_scores[i][3])
        
            if A_box_scores[i][5] == "@":
                player.append("A")
            else:
                player.append("H")
            
            player.append(A_box_scores[i][6])
            for j in range(7, len(A_box_scores[i])):
                player.append(A_box_scores[i][j])
        A_box_scores[i] = player    
        
    return A_box_scores

def scrape_new_advanced_stats(year, pages):
    """
    This function scrapes a specified number of pages of advanced stats from NBA.com.
    Remember to toggle the number of pages as you see fit.
    """
    if year == 2023 or year == '2023':
        link = 'https://www.nba.com/stats/players/boxscores-advanced?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-advanced'

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div/button"))).click()
    # try:
    #     WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div/button"))).click()
    # except Exception:
    #     try:
    #         WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div/div/div/button"))).click()
    #     except Exception:
    #         pass
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
    
    A_tables = []
    for i in tqdm(range(1, pages+1)):
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        A_tables.append(text)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(2)
    
    driver.quit()

    with open("output/{num}/NewAdvancedStats{num}.txt".format(num = year), 'w') as file:
        for row in A_tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
    
    adv_new = clean_new_advanced_stats(year)
    
    df_A_new = pd.DataFrame(adv_new, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 
                                              'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 
                                              'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE'])

    df_A_new[['Mins']] = df_A_new[['Mins']].apply(pd.to_numeric)
    df_A_new[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']] = df_A_new[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']].astype(float)
    
    advanced_old = pd.read_csv("output/{num}/Advanced{num}.csv".format(num = year))
    advanced = pd.concat([df_A_new, advanced_old], ignore_index=True, sort=False)
    advanced = advanced[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']]
    advanced = advanced.drop_duplicates().reset_index()
    #keeps old indexes as column. So I'm just overwriting it in a lazy way-- look into better way
    advanced = advanced[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']]
    advanced = remove_duplicates(advanced)
    advanced.to_csv('output/{num}/Advanced{num}.csv'.format(num = year))
    
    return advanced

def clean_new_advanced_stats(year):
    """
    The newly created list of lists is then cleaned according to if the player has a suffix
    in their name or not.  The end goal is to create uniform length lists with which to create
    a dataframe to then save to a .csv. 
    """    
    advanced = open('output/{num}/NewAdvancedStats{num}.txt'.format(num = year))
    advanced = advanced.read()
    A_game_logs = advanced.split("\n")
    A_game_logs.pop()
    
    A_box_scores = []
    for i in range(len(A_game_logs)):
        A_box_scores.append(A_game_logs[i].split(" "))
    
    new_adv_scores = adv_format_rows(A_box_scores)
    
    return new_adv_scores
    
def remove_duplicates(data):
    """
    This function removes duplicate rows from the updated dataframe.
    """
    names = data['Name'].unique()
    fix_names = []
    for i in names:
        guy = data[data['Name'] == i]    
        if len(guy['Name']) != len(guy['Date'].unique()):
            fix_names.append(i)

    #remove duplicate row for single date. Lower interger index value is correct (more recent)
    duplicates = []
    for i in fix_names:
        guy = data[data['Name'] == i]
        duplicates.append(guy.index[guy.duplicated(['Date'])].tolist())

    for i in duplicates:
        data = data.drop(index = i[0])    
    return data

def update_advanced_stats(adv_year, adv_pages, all_adv_pages):
    #protect against random inputs
    if type(adv_year) != int or type(adv_pages) != int:
        raise ValueError("Please enter input in the form of an integer.")    
    if adv_year != 2023 and adv_year != 2024 and adv_year != 0:
        raise ValueError('No Advanced Stats data for year: {num}. Please use 2023 or 2024.'.format(num = adv_year))
    #if value is 2023 or 2024 and positive pages
    if adv_year != 0 and adv_pages != 0:
        if all_adv_pages == True:
            all_advanced_stats = scrape_all_advanced_stats(adv_year)
            all_added_entries = len(all_advanced_stats)

            create_schedule(adv_year)
            return "All advanced stats were collected. \n {num} entries were collected. \nThe {year} season schedule has been updated.".format(num = all_added_entries, year = adv_year)
        else:
            #if there is no file to update, must collect all data
            if os.path.exists('output/{num}/Advanced{num}.csv'.format(num = adv_year)):
                old_advanced_stats = pd.read_csv('output/{num}/Advanced{num}.csv'.format(num = adv_year))
                old_advanced_stats = len(old_advanced_stats)

                new_advanced_stats = scrape_new_advanced_stats(adv_year, adv_pages)
                new_advanced_stats = len(new_advanced_stats)
                updated_adv_entries = new_advanced_stats - old_advanced_stats

                if updated_adv_entries > 0:
                    create_schedule(adv_year)
                    return "Advanced stats file has been updated.\n{num} entries were added to the Advanced stats .csv file.\nThe {year} season schedule file has been updated.".format(num = updated_adv_entries, year = adv_year)       

                else:
                    return "Advanced stats file was not updated, no new entries to add.\nThe {num} season schedule was not updated.".format(num = adv_year)

            else:
                all_advanced_stats = scrape_all_advanced_stats(adv_year)
                all_added_entries = len(all_advanced_stats)
                create_schedule(adv_year)

                return "All advanced stats were collected. \n{num} entries were collected. \n The {year} season schedule has been updated.".format(num = all_added_entries, year = adv_year)
    #if not input, just skip
    else:
        return "No new advanced stats were collected."


#%%
if __name__ == "__main__":
    scrape_all_advanced_stats()
    scrape_new_advanced_stats()
    update_advanced_stats()