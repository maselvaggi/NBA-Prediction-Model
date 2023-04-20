#%%
import pandas as pd
from PyPDF2 import PdfReader
# import numpy as np
# import re
# import time
# from lxml import html
# from lxml import etree
# from bs4 import BeautifulSoup
# import requests
# from selenium import webdriver
# from selenium.webdriver.common.by import By

# %% Now In USE:
#This gets all the box score pdfs. May need to create a function to 
#be more selective on which pdfs to get in the future.
# for i in range(len(links2223)):
#     direct = 'Box Scores/'
#     response = requests.get(links2223[i])
#     direct = ''.join([direct, file_names[i]])
#     with open(direct, 'wb') as f:
#         f.write(response.content)

# %%
def injury_df():
    """
    This function pulls the text from each downloaded PDF file.
    It grabs all players who are listed as DND/DNP/Inactive.
    From there, the data is cleaned and put into a .csv file organized
    by date/team/player/injury.  Most players have an injury listed.
    If a player does not have an injury listed, it was either omitted 
    on the PDF itself or scrubbed during the cleaning process to avoid
    error.
    """
    #you need advanced.csv and schedule.csv to run this function
    file_names = pdf_names()

    for i in range(len(file_names)):
        name = file_names[i]
        path = 'Box Scores'
        path = '/'.join([path,name])

        reader = PdfReader(path)
        page = reader.pages[0]
        text = page.extract_text()

        with open("Inactives.txt", 'w') as file:
            file.write(text)

        inactives = open('Inactives.txt')
        inactives = inactives.read()
        inactives = inactives.split("\n")

        indexes = []
        for a in range(250, len(inactives)):
            if 'Inactive' in inactives[a]:
                indexes.append(a)
            elif 'Points in the Paint' in inactives[a]:
                indexes.append(a)
            else:
                pass
        indexes

        injuries = []
        for b in range(indexes[0], indexes[-1]):
            injuries.append(inactives[b])

        # This creates the completed inactive strings
        for c in range(len(injuries)):
            if 'Inactive' in injuries[c]:
                pass
            else:
                injuries[c-1] = " ".join([injuries[c-1], injuries[c]])

        # This keeps only the full Inactive strings and removes the partial strings
        injury = []
        for d in range(len(injuries)):
            if 'Inactive' in injuries[d]:
                injury.append(injuries[d])

        # This grabs players that did not play from the regular boxscore
        dnp = []
        for e in range(len(inactives)):
            if "VISITOR" in inactives[e]:
                dnp.append(inactives[e])
            elif "HOME" in inactives[e]:
                dnp.append(inactives[e])        
            elif "DNP" in inactives[e]:
                dnp.append(e)
            elif "DND" in inactives[e]:
                dnp.append(e)
            else:
                pass
        DNP = []
        for f in range(len(dnp)):
            if type(dnp[f]) is str:
                DNP.append(dnp[f])
            else:
                player = " (".join([inactives[dnp[f]-1], inactives[dnp[f]]])
                player = "".join([player, ')'])
                DNP.append(player)

        # this combines players who were available that did not play with those who were injured
        j = 0
        for g in range(1, len(DNP)):
            if "HOME" in DNP[g]:
                j +=1
            else:
                injury[j] = ", ".join([injury[j],DNP[g]])

        for h in range(0,2):
            injury[h] = injury[h].split(', ')

        injury_away = injury[0]
        injury_home = injury[1]

        injury_away[0] = injury_away[0].split(' - ')
        if len(injury_away[0]) == 2:
            injury_away[0] = injury_away[0][1]
        else:
            injury_away[0] = ' - '.join([injury_away[0][1], injury_away[0][2]]) #Removes "Inactive: teamname - "

        injury_home[0] = injury_home[0].split(' - ')
        if len(injury_home[0]) == 2:
            injury_home[0] = injury_home[0][1]
        else:
            injury_home[0] = ' - '.join([injury_home[0][1], injury_home[0][2]])#Removes "Inactive: teamname - "

        #Add team name, date to each element
        away, home = name[9:12], name[12:15]
        year, month, day = name[0:4], name[4:6], name[6:8]
        date = '/'.join([month, day, year])
        for k in range(len(injury_away)):
            injury_away[k] = " = ".join([away, injury_away[k]])
            injury_away[k] = ' = '.join([date, injury_away[k]])

        for l in range(len(injury_home)):
            injury_home[l] = " = ".join([home, injury_home[l]])
            injury_home[l] = ' = '.join([date, injury_home[l]])

        injury = injury_away + injury_home

        for m in range(len(injury)):
            injury[m] = injury[m].replace(' = ','=').replace(' (', '=').replace(')','')

        for n in range(len(injury)):
            injury[n] = injury[n].split('=')

        for o in range(len(injury)):
            if len(injury[o]) == 5:
                injury[o] = injury[o][0:3]

        if i !=0:
            temp_injury = pd.DataFrame(injury, columns=['Date', 'Team', 'Player', 'Injury'], index = None)
            injury_data = pd.concat([temp_injury, injury_data], ignore_index = True)
        else:
            injury_data = pd.DataFrame(injury, columns=['Date', 'Team', 'Player', 'Injury'], index = None)

        print(i)    

    injury_data.to_csv('Injury_Data.csv')    
    return injury_data

def pdf_names():
    """
    This fucntion pulls the matchups ffrom the schedule2223.csv
    file and dates of those matchups to create the names of each 
    downloaded PDF.  These names are used to reference each saved
    PDF.
    """
    schedule  = pd.read_csv('Schedule2223.csv', index_col = 0)
    date = schedule['Date'].to_numpy()
    home = schedule['Team'].to_numpy()
    away = schedule['Opponent'].to_numpy()

    for i in range(len(date)):
        day = date[i].split('/')
        day = "".join([day[2], day[0], day[1]])
        date[i] = day

    file_names = []

    for i in range(len(date)):
        name = "_".join([date[i], away[i]])
        name = "".join([name, home[i], '.pdf'])
        file_names.append(name)

    return file_names

def pdf_links():
    """
    This function creates the links that will then be used to
    download the needed PDF files locally.
    """
    schedule  = pd.read_csv('Schedule2223.csv', index_col = 0)
    date = schedule['Date'].to_numpy()
    home = schedule['Team'].to_numpy()
    away = schedule['Opponent'].to_numpy()

    for i in range(len(date)):
        day = date[i].split('/')
        day = "".join([day[2], day[0], day[1]])
        date[i] = day

    links2223 = []

    for i in range(len(date)):
        link = "https://statsdmz.nba.com/pdfs/"
        link = "".join([link, date[i]])
        link = "/".join([link, date[i]])
        matchup = "".join([away[i], home[i], '.pdf'])
        link = "_".join([link, matchup])
        links2223.append(link)
    
    return links2223
#%%
# injury_data = pd.read_csv('Injury_Data.csv', index_col = 0)
# injury_data



#%% No Longer In Use But Leaving for Reference:
# url = 'https://hoopshype.com/lists/nba-injuries-tracker/'
# record = requests.get(url)
# time.sleep(30)
# soup = BeautifulSoup(record.content, "html.parser")
# #dom = etree.HTML(str(soup))
# #blah = dom.xpath('//*[@id="882171005"]/div/table/tbody/tr[1]')

# driver = webdriver.Chrome()
# driver.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vSBRYR7jdH3xK5ipXhYzKpIbm4QhpynEF2zusMSQCNSYF3hM5KiVH5dKFXuWHbQBzQTNyVrByVhu6gT/pubhtml/sheet?headers=false&gid=882171005&single=true&widget=true&range=p1:s6300&headers=false')

# html = driver.find_element_by_xpath('//*[@id="882171005"]/div/table/tbody').text
# driver.quit()

# with open("InjuryReport.txt", 'w') as file:
#     file.write(html)

# injuries = open("InjuryReport.txt")
# injuries = injuries.read()
# injuries_split = injuries.split("\n")

# status = ['Available', 'Probable', 'Questionable', 'Doubtful', 'Out']

# for i in range(1,len(injuries_split)):
#     if any([x in injuries_split[i] for x in status]):
#         pass
#     else:
#         if any(map(str.isdigit, injuries_split[i])) is False:
#             combo = [injuries_split[i-1], injuries_split[i]]
#             injuries_split[i-1] = " ".join(combo)

# for i in range(len(injuries_split)):
#     if "Available" or "Probable" or "Questionable" or "Doubtful" or "Out" in injuries_split[i]:
#         if "Available" in injuries_split[i]:
#             txt = injuries_split[i]
#             x = txt.split(" Available ", 1)
#             x.append("Available")
#             injuries_split[i] = x
#         elif "Probable" in injuries_split[i]:
#             txt = injuries_split[i]
#             x = txt.split(" Probable ", 1)
#             x.append("Probable")
#             injuries_split[i] = x
#         elif "Questionable" in injuries_split[i]:
#             txt = injuries_split[i]
#             x = txt.split(" Questionable ", 1)
#             x.append("Questionable")
#             injuries_split[i] = x
#         elif "Doubtful" in injuries_split[i]:
#             txt = injuries_split[i]
#             x = txt.split(" Doubtful ", 1)
#             x.append("Doubtful")
#             injuries_split[i] = x
#         elif "Out" in injuries_split[i]:
#             txt = injuries_split[i]
#             x = txt.split(" Out ", 1)
#             x.append("Out")
#             injuries_split[i] = x                        

# for i in range(1,len(injuries_split)):
#     if type(injuries_split[i]) == str:
#         if any(map(str.isdigit, injuries_split[i])) == False:
#             pass
#         else:
#             num = i
#     else:
#         injuries_split[i].insert(0,injuries_split[num])

# injuries_split = [ele for ele in injuries_split if len(ele) == 4]

# injuries_split

# injuries = pd.DataFrame(injuries_split, columns=['Date', 'Player', 'Injury', 'Status'], index = None)
# injuries = injuries[1:] #= injuries['Date', 'Player', 'Injury', 'Status']
# injuries.to_csv("Injuries.csv")
# injuries = pd.read_csv("Injuries.csv", index_col= 0)
# ailments = injuries['Injury'].unique()

# still_available = []
# for i in ailments:
#     if i.count('G League'):
#         still_available.append(i)
#     elif i.count('Trade'):
#         still_available.append(i)
#     elif i.count("Coach"):
#         still_available.append(i)
#     else:
#         pass
    
# still_available




#%%
if __name__ == "__main__":
    injury_df()
    pdf_names()
    pdf_links()