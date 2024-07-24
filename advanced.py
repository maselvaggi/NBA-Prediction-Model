#%%
import time
import os.path
import numpy as np
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
    This function will scrape all of the advavnced player box scores from the current nba 
    regular season up until today's date.  Using the ChromeDriver.exe, we are able to 
    easily parse through the tables of data and save the data in a .csv file and return a 
    dataframe.
    '''
    advanced_links = {
        2024:"https://www.nba.com/stats/players/boxscores-advanced?Season=2023-24&SeasonType=Regular+Season",
        2023:"https://www.nba.com/stats/players/boxscores-advanced?Season=2022-23&SeasonType=Regular+Season",
        2022:"https://www.nba.com/stats/players/boxscores-advanced?Season=2021-22&SeasonType=Regular+Season",
        2021:"https://www.nba.com/stats/players/boxscores-advanced?Season=2020-21&SeasonType=Regular+Season",
        2020:"https://www.nba.com/stats/players/boxscores-advanced?Season=2019-20&SeasonType=Regular+Season",
        2019:"https://www.nba.com/stats/players/boxscores-advanced?Season=2018-19&SeasonType=Regular+Season",
        2018:"https://www.nba.com/stats/players/boxscores-advanced?Season=2017-18&SeasonType=Regular+Season",
        2017:"https://www.nba.com/stats/players/boxscores-advanced?Season=2016-17&SeasonType=Regular+Season",
        2016:"https://www.nba.com/stats/players/boxscores-advanced?Season=2015-16&SeasonType=Regular+Season",
        2015:"https://www.nba.com/stats/players/boxscores-advanced?Season=2014-15&SeasonType=Regular+Season",
        2014:"https://www.nba.com/stats/players/boxscores-advanced?Season=2013-14&SeasonType=Regular+Season"
    }

    link = advanced_links[year]      

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    driver.implicitly_wait(25)
#    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/button').click()
    time.sleep(15)

    #pop up
 #   driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
    time.sleep(20)

    #get number of pages
    drop_down = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
    options = [x for x in drop_down.find_elements(By.TAG_NAME, "option")]
    pages = []
    for element in options:
        pages.append(element.get_attribute("value"))

    A_tables = []
    for i in tqdm(range(1, len(pages))):
        # table body text
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        A_tables.append(text)
        # right arrow button
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(1)
    
    driver.quit()

    with open(f"output/{year}/NewAdvancedStats{year}.txt", 'w', encoding='utf-8') as file:
        for row in A_tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
    
    All_adv_scores = clean_new_advanced_stats(year)
    
    df_A = pd.DataFrame(All_adv_scores, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins',
                                                 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%',
                                                 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE'])
    df_A[['Mins']] = df_A[['Mins']].apply(pd.to_numeric)
    df_A[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']] = df_A[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']].astype(float)

    unique_adv_dates = df_A['Date'].unique()
    for i in range(len(unique_adv_dates)):
        if '/' not in unique_adv_dates[i]:
            pass
        else:
            fix_this_date = unique_adv_dates[i]
            fix_this_date = fix_this_date.split('/')
            fixed_date = f"{fix_this_date[2]}-{fix_this_date[0]}-{fix_this_date[1]}"
            df_A = df_A.replace(unique_adv_dates[i], fixed_date)    
    
    df_A.to_csv(f"output/{year}/Advanced{year}.csv")
    
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
        if len(A_box_scores[i]) == 23:
            player.append(A_box_scores[i][0])
            player.append(A_box_scores[i][1])
            
            if A_box_scores[i][3] == "@":
                player.append("A")
            else:
                player.append("H")
            
            player.append(A_box_scores[i][4])
        
            for j in range(5, len(A_box_scores[i])):
                player.append(A_box_scores[i][j])
        
        elif len(A_box_scores[i]) == 24:
            player.append(A_box_scores[i][0] + " " + A_box_scores[i][1])
            player.append(A_box_scores[i][2])
            
            if A_box_scores[i][4] == "@":
                player.append("A")
            else:
                player.append("H")
            
            player.append(A_box_scores[i][5])
        
            for j in range(6, len(A_box_scores[i])):
                player.append(A_box_scores[i][j])

        elif len(A_box_scores[i]) == 25:
            player.append(A_box_scores[i][0] + " " + A_box_scores[i][1] + " " + A_box_scores[i][2])
            player.append(A_box_scores[i][3])
        
            if A_box_scores[i][5] == "@":
                player.append("A")
            else:
                player.append("H")
            
            player.append(A_box_scores[i][6])
            for j in range(7, len(A_box_scores[i])):
                player.append(A_box_scores[i][j])

        elif len(A_box_scores[i]) == 26:
            player.append(A_box_scores[i][0] + " " + A_box_scores[i][1] + " " + 
                          A_box_scores[i][2] + " " + A_box_scores[i][3])
            player.append(A_box_scores[i][4])
        
            if A_box_scores[i][6] == "@":
                player.append("A")
            else:
                player.append("H")
            
            player.append(A_box_scores[i][7])
            for j in range(8, len(A_box_scores[i])):
                player.append(A_box_scores[i][j])

        A_box_scores[i] = player    

    return A_box_scores

def scrape_new_advanced_stats(year, pages):
    """
    This function scrapes a specified number of pages of advanced stats from NBA.com.
    Remember to toggle the number of pages as you see fit.
    """
    advanced_links = {
        2024:"https://www.nba.com/stats/players/boxscores-advanced?Season=2023-24&SeasonType=Regular+Season",
        2023:"https://www.nba.com/stats/players/boxscores-advanced?Season=2022-23&SeasonType=Regular+Season",
        2022:"https://www.nba.com/stats/players/boxscores-advanced?Season=2021-22&SeasonType=Regular+Season",
        2021:"https://www.nba.com/stats/players/boxscores-advanced?Season=2020-21&SeasonType=Regular+Season",
        2020:"https://www.nba.com/stats/players/boxscores-advanced?Season=2019-20&SeasonType=Regular+Season",
        2019:"https://www.nba.com/stats/players/boxscores-advanced?Season=2018-19&SeasonType=Regular+Season",
        2018:"https://www.nba.com/stats/players/boxscores-advanced?Season=2017-18&SeasonType=Regular+Season",
        2017:"https://www.nba.com/stats/players/boxscores-advanced?Season=2016-17&SeasonType=Regular+Season",
        2016:"https://www.nba.com/stats/players/boxscores-advanced?Season=2015-16&SeasonType=Regular+Season",
        2015:"https://www.nba.com/stats/players/boxscores-advanced?Season=2014-15&SeasonType=Regular+Season",
        2014:"https://www.nba.com/stats/players/boxscores-advanced?Season=2013-14&SeasonType=Regular+Season"
    }

    link = advanced_links[year]      
    
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
#    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/button').click()
    time.sleep(20)

    #get number of pages
    drop_down = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
    options = [x for x in drop_down.find_elements(By.TAG_NAME, "option")]
    table_pages = []
    for element in options:
        table_pages.append(element.get_attribute("value"))

    if pages > len(table_pages):
        raise ValueError(f"The number of pages you entred: {pages} is greater than the number of pages available: {len(table_pages)}.")    

    A_tables = []
    for i in tqdm(range(1, pages+1)):
        # table body text
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        A_tables.append(text)
        # right arrow button
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(2)
    
    driver.quit()

    with open(f"output/{year}/NewAdvancedStats{year}.txt", 'w') as file:
        for row in A_tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
    
    adv_new = clean_new_advanced_stats(year)
    
    df_A_new = pd.DataFrame(adv_new, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 
                                              'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 
                                              'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE'])

    df_A_new[['Mins']] = df_A_new[['Mins']].apply(pd.to_numeric)
    df_A_new[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']] = df_A_new[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']].astype(float)

    #fix dates, concat new with old, return only new data
    unique_adv_dates = df_A_new['Date'].unique()
    for i in range(len(unique_adv_dates)):
        if '/' not in unique_adv_dates[i]:
            pass
        else:
            fix_this_date = unique_adv_dates[i]
            fix_this_date = fix_this_date.split('/')
            fixed_date = f"{fix_this_date[2]}-{fix_this_date[0]}-{fix_this_date[1]}"
            df_A_new = df_A_new.replace(unique_adv_dates[i], fixed_date)

    advanced_old = pd.read_csv(f"output/{year}/Advanced{year}.csv")
    advanced = pd.concat([df_A_new, advanced_old], ignore_index=True, sort=False)

    unique_adv_dates = advanced['Date'].unique()
    for i in range(len(unique_adv_dates)):
        if '/' not in unique_adv_dates[i]:
            pass
        else:
            fix_this_date = unique_adv_dates[i]
            fix_this_date = fix_this_date.split('/')
            fixed_date = f"{fix_this_date[2]}-{fix_this_date[0]}-{fix_this_date[1]}"
            advanced = advanced.replace(unique_adv_dates[i], fixed_date)    

    advanced = advanced[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'OFFRTG',
                         'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 
                         'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']]
    advanced = advanced.drop_duplicates().reset_index()
    #keeps old indexes as column. So I'm just overwriting it in a lazy way
    advanced = advanced[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'OFFRTG', 
                         'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 
                         'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']]
    
    advanced = remove_duplicates(advanced)    
    advanced.to_csv(f"output/{year}/Advanced{year}.csv")
    
    return df_A_new

def clean_new_advanced_stats(year):
    """
    The newly created list of lists is then cleaned according to if the player has a suffix
    in their name or not.  The end goal is to create uniform length lists with which to create
    a dataframe to then save to a .csv. 
    """    
    advanced = open('output/{num}/NewAdvancedStats{num}.txt'.format(num = year), encoding='utf-8')
    advanced = advanced.read()
    A_game_logs = advanced.split("\n")
    A_game_logs.pop()
    
    A_box_scores = []
    for i in range(len(A_game_logs)):
        A_box_scores.append(A_game_logs[i].split(" "))
    
    new_adv_scores = adv_format_rows(A_box_scores)
    
    return new_adv_scores

#%%
if __name__ == "__main__":
    scrape_all_advanced_stats()
    scrape_new_advanced_stats()

