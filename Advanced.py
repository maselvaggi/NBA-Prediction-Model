#%%
import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver
from remove_duplicates import *
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import requests
# %%
def scrape_all_ADV(year):
    '''
    This function will scrape all of the advavnced player box scores from the current nba regular
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
        link = 'https://www.nba.com/stats/players/boxscores-advanced?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-advanced'

    driver = webdriver.Chrome()
    driver.get(link)
    driver.maximize_window()
    driver.implicitly_wait(25)
#    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/button').click()
    time.sleep(15)
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

    with open("output/{num}/Advancedfile{num}.txt".format(num = year), 'w') as file:
        for row in A_tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
    
    All_adv_scores = clean_all_ADV(year)
    
    df_A = pd.DataFrame(All_adv_scores, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins',
                                                 'OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%',
                                                 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE'])
    df_A[['Mins']] = df_A[['Mins']].apply(pd.to_numeric)
    df_A[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']] = df_A[['OFFRTG', 'DEFRTG', 'NETRTG', 'AST%', 'AST/TO', 'AST RATIO', 'OREB%', 'DREB%', 'REB%', 'TO RATIO', 'EFG%', 'TS%', 'USG%', 'PACE', 'PIE']].astype(float)
    df_A.to_csv('output/{num}/Advanced{num}.csv'.format(num = year))
    
    return df_A

def clean_all_ADV(year):
    """
    This fucntion takes in the newly scraped advanced player box scores from the .txt file.
    Then, the string is split by line, and then split by ' '.  
    """
    advanced = open('output/{num}/Advancedfile{num}.txt'.format(num = year))
    advanced = advanced.read()
    A_game_logs = advanced.split("\n")
    A_game_logs.pop()
    
    A_box_scores = []
    for i in range(len(A_game_logs)):
        A_box_scores.append(A_game_logs[i].split(" "))
    
    all_adv_scores = Adv_format_rows(A_box_scores)
    
    return all_adv_scores
    
def Adv_format_rows(A_box_scores):
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

#%%
df_2024 = scrape_all_ADV(2024)
#%%
def scrape_new_ADV(year, pages):
    """
    This function scrapes a specified number of pages of advanced stats from NBA.com.
    Remember to toggle the number of pages as you see fit.
    """
    if year == 2023 or year == '2023':
        link = 'https://www.nba.com/stats/players/boxscores-advanced?Season=2022-23'
    else:
        link = 'https://www.nba.com/stats/players/boxscores-advanced'

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('disable-popup-blocking')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(link)
    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div/button"))).click()
    # try:
    #     WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[3]/div/div/div/button"))).click()
    # except Exception:
    #     try:
    #         WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div/div/div/button"))).click()
    #     except Exception:
    #         pass

    time.sleep(30)        
    
    A_tables = []
    for i in range(1, pages+1):
        text = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        A_tables.append(text)
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(2)
    
    driver.quit()

    with open("output/{num}/NewAdvancedfile{num}.txt".format(num = year), 'w') as file:
        for row in A_tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
    
    adv_new = clean_new_ADV(year)
    
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

def clean_new_ADV(year):
    """
    The newly created list of lists is then cleaned according to if the player has a suffix
    in their name or not.  The end goal is to create uniform length lists with which to create
    a dataframe to then save to a .csv. 
    """    
    advanced = open('output/{num}/NewAdvancedfile{num}.txt'.format(num = year))
    advanced = advanced.read()
    A_game_logs = advanced.split("\n")
    A_game_logs.pop()
    
    A_box_scores = []
    for i in range(len(A_game_logs)):
        A_box_scores.append(A_game_logs[i].split(" "))
    
    new_adv_scores = Adv_format_rows(A_box_scores)
    
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

#%%
if __name__ == "__main__":
    scrape_all_ADV()
    scrape_new_ADV()
