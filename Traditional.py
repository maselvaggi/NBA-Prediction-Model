#%%
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#%%
def scrape_all_Trad():

    driver = webdriver.Chrome()
    driver.get('https://www.nba.com/stats/players/boxscores-traditional')
    driver.implicitly_wait(25)
    driver.find_element_by_xpath('/html/body/div[5]/div[3]/div/div/div/button').click()
    time.sleep(20)

    drop_down = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select')
    options = [x for x in drop_down.find_elements_by_tag_name("option")]
    pages = []
    for element in options:
        pages.append(element.get_attribute("value"))
        
    #Code to grab ALL DATA
    tables = []

    for i in range(1, len(pages)):
        text = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        tables.append(text)
        driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(2)
        
    driver.quit()
    
    with open("Traditionalfile.txt", 'w') as file:
        for row in tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
            
    trad_all = clean_all_Trad()
    
    df_T = pd.DataFrame(trad_all, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 
                                           'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
                                           'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
                                           'BLK', 'TOV', 'PF', 'Plusminus'])
    
    df_T[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus' ]] = df_T[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']].apply(pd.to_numeric) 
    df_T[['FG%', '3P%', 'FT%']] = df_T[['FG%', '3P%', 'FT%']].astype(float)
    
    df_T.to_csv('Traditional.csv')


    return df_T
    
    
def clean_all_Trad():
    
    traditional = open('Traditionalfile.txt')
    traditional = traditional.read()
    T_game_logs = traditional.split("\n")
    T_game_logs.pop()
    
    T_box_scores = []
    for i in range(len(T_game_logs)):
        T_box_scores.append(T_game_logs[i].split(" "))
    
    T_box_scores = all_Trad(T_box_scores)
    
    return T_box_scores


def all_Trad(T_box_scores):

    for i in range(len(T_box_scores)):
        player = []

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

#%%
def scrape_new_Trad():
    
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('disable-popup-blocking')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.nba.com/stats/players/boxscores-traditional')
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
    time.sleep(20)

    tables = []

    for i in range(1, 15):
        text = driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[3]/table/tbody').text
        tables.append(text)
        driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]').click()
        time.sleep(1)
        
    driver.quit()
    
    with open("NewTraditionalfile.txt", 'w') as file:
        for row in tables:
            s = "".join(map(str, row))
            file.write(s+'\n')
            
    trad_new = clean_new_Trad()
    
    df_T_new = pd.DataFrame(trad_new, columns=['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 
                                      'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%',
                                       'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
                                       'BLK', 'TOV', 'PF', 'Plusminus'])
    
    df_T_new[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus' ]] = df_T_new[['Mins', 'Points', 'FGM', 'FGA',  '3PM', '3PA', 'FTM', 'FTA', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']].apply(pd.to_numeric) 
    df_T_new[['FG%', '3P%', 'FT%']] = df_T_new[['FG%', '3P%', 'FT%']].astype(float)
    
    traditional_old = pd.read_csv("Traditional.csv")
    traditional = pd.concat([df_T_new, traditional_old], ignore_index=True, sort=False)
    traditional = traditional[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']]
    traditional = traditional.drop_duplicates().reset_index()
    #keeps old indexes as column. So I'm just overwriting it in a lazy way-- look into better way
    traditional = traditional[['Name', 'Team', 'Location', 'Opponent', 'Date', 'Result', 'Mins', 'Points', 'FGM', 'FGA', 'FG%', '3PM', '3PA', '3P%','FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'Plusminus']]
    traditional = remove_duplicates(traditional)
    traditional.to_csv('Traditional.csv')
    
    return traditional    

def clean_new_Trad():
    
    traditional = open('NewTraditionalfile.txt')
    traditional = traditional.read()
    T_game_logs = traditional.split("\n")
    T_game_logs.pop()
    
    T_box_scores = []
    for i in range(len(T_game_logs)):
        T_box_scores.append(T_game_logs[i].split(" "))
    
    T_box_scores = new_Trad(T_box_scores)
    
    return T_box_scores

def new_Trad(T_box_scores):

    for i in range(len(T_box_scores)):
        player = []

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

def remove_duplicates(data):
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

# %%
if __name__ == "__main__":
    scrape_all_Trad()
    all_Trad()
    clean_all_Trad()
    scrape_new_Trad()
    clean_new_Trad()
    new_Trad()
    remove_duplicates()