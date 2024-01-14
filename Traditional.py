#%%
import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver
from remove_duplicates import *
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#%%
def scrape_all_Trad(year):
    '''
    This function will scrape all of the player box scores from the current nba regular
    season up until today's date.  Using the ChromeDriver.exe, we are able to easily
    parse through the tables of data and save the data in a .csv file and return a 
    dataframe.

    I only recommend using this function if you are starting out.  This function will
    take a lot of time to run.  The time.sleep is put in there to be kind to NBA.com.

    NBA.com has caught on to the script and will change the location of the pop up in
    the xpath.  Highly recommend just waiting a second after the popup becomes visible
    to see if the script can click out of the popup (if the script is successful, the 
    popup will be exited almost immediately), if not, just click out of the pop up
    yourself and the script will then be able to scrape all the necessay data.

    If you do not click out of the popup, the script will stop and return an error.
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
    
    with open('output/{num}/Traditionalfile{num}.txt'.format(num = year), 'w') as file:
        for row in tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
            
    trad_all = clean_all_Trad(year)
    
    df_T = pd.DataFrame(trad_all, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 
                                           'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
                                           'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
                                           'BLK', 'TOV', 'PF', 'Plusminus'])
    
    df_T[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus' ]] = df_T[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']].apply(pd.to_numeric) 
    df_T[['FG%', '3P%', 'FT%']] = df_T[['FG%', '3P%', 'FT%']].astype(float)
    
    df_T.to_csv('output/{num}/Traditional{num}.csv'.format(num = year))


    return df_T
    
    
def clean_all_Trad(year):
    """
    I save the data in a txt file to have a copy, and it makes it easier to 
    view after splitting by new line.
    """
    traditional = open('output/{num}/Traditionalfile{num}.txt'.format(num = year))
    traditional = traditional.read()
    T_game_logs = traditional.split("\n")
    T_game_logs.pop()
    
    T_box_scores = []
    for i in range(len(T_game_logs)):
        T_box_scores.append(T_game_logs[i].split(" "))
    
    T_box_scores = Trad_format_rows(T_box_scores)
    
    return T_box_scores


def Trad_format_rows(T_box_scores):
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

def scrape_new_Trad(year, pages):
    """
    This fucntion does exactly the same as scrape_all_Trad() but you can specify
    how many pages of player box scores you want to scrape.

    Similar to scrape_all_trad(), make sure to see if the popup get closed out by the script.
    After about a seceond, just click out of the popup and the script will run like normal.

    If you do not click out of the script, there will be a error and the script will stop.
    """

    if year == 2023 or year == '2023':
        link = 'https://www.nba.com/stats/players/boxscores-traditional?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-traditional'

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()

    #WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div/button"))).click()
    # driver.implicitly_wait(50)
    # try:
    #     tables = []
    #     for i in range(1, 20):
    #         text = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
    #         tables.append(text)
    #         driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
    #         time.sleep(1)
            
    #     driver.quit()
    # except Exception:
    #     try:
    #         driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/div/div/button').click()
    #     except Exception:
    #         try:
    #             driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/button').click()
    #         except Exception:
    #             try:
    #                 driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div/div/button').click()
    #             except Exception:
    #                 pass
    time.sleep(30)        

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
    
    with open("output/{num}/NewTraditionalfile{num}.txt".format(num = year), 'w') as file:
        for row in tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
            
    trad_new = clean_new_Trad(year)
    
    df_T_new = pd.DataFrame(trad_new, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 
                                      'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
                                       'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
                                       'BLK', 'TOV', 'PF', 'Plusminus'])
    
    df_T_new[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus' ]] = df_T_new[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']].apply(pd.to_numeric) 
    df_T_new[['FG%', '3P%', 'FT%']] = df_T_new[['FG%', '3P%', 'FT%']].astype(float)
    
    traditional_old = pd.read_csv("output/{num}/Traditional{num}.csv".format(num = year))
    traditional = pd.concat([df_T_new, traditional_old], ignore_index=True, sort=False)
    traditional = traditional[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']]
    traditional = traditional.drop_duplicates().reset_index()
    #keeps old indexes as column. So I'm just overwriting it in a lazy way-- look into better way
    traditional = traditional[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']]
    traditional = remove_duplicates(traditional)
    traditional.to_csv('output/{num}/Traditional{num}.csv'.format(num = year))
    
    return traditional    

def clean_new_Trad(year):
    
    traditional = open('output/{num}/NewTraditionalfile{num}.txt'.format(num = year))
    traditional = traditional.read()
    T_game_logs = traditional.split("\n")
    T_game_logs.pop()
    
    T_box_scores = []
    for i in range(len(T_game_logs)):
        T_box_scores.append(T_game_logs[i].split(" "))
    
    T_box_scores = Trad_format_rows(T_box_scores)
    
    return T_box_scores

def Trad_format_rows(T_box_scores):
    """
    This function builds a list of lists.  Each list within the larger list
    will be a row in the dataframe.  
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

# %%
if __name__ == "__main__":
    scrape_all_Trad()
    scrape_new_Trad()