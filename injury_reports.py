#%%
import time
import requests
import pandas as pd
from tqdm import tqdm
from pypdf import PdfReader
# import numpy as np
# import re
# from lxml import html
# from lxml import etree
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By

#%%
def get_injury_data(year):
    """
    """
    #you need traditional.csv and schedule.csv to run this function
    file_names = injury_report_links_and_names(year, get_only_file_names = True)
    schedule = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col=0)
    not_injured = pd.read_csv(f"output/{year}/Traditional{year}.csv", index_col=0)

    for i in tqdm(range(len(file_names))):
        date = file_names[i][:10] #remove .pdf to access only date
        day = schedule[schedule['Date'] == date]
        day_teams = list(day['Team'].unique()) + list(day['Opponent'].unique())
        
        reader = PdfReader(f"output/{year}/Injury Reports/{file_names[i]}")
        len(reader.pages)
        inactives = []
        for a in range(len(reader.pages)):
            text = reader.pages[a].extract_text()

            with open(f"output/{year}/Inactives{year}.txt", 'w') as file:
                file.write(text)

            temp = open(f"output/{year}/Inactives{year}.txt")
            temp = temp.read()
            temp = temp.split("\n")

            inactives = inactives + temp

        for b in range(len(inactives)):
            if '(' not in inactives[b] and ')' in inactives[b]:
                inactives[b-1] = ' '.join([inactives[b-1], inactives[b]])

        inactives = [h for h in inactives if ',' in h]

        #just get all names from injury reports
        for c in range(len(inactives)):
            if ' Out ' in inactives[c]:
                inactives[c] = inactives[c].split(' Out ')
            elif ' Doubtful ' in inactives[c]:
                inactives[c] = inactives[c].split(' Doubtful ')
            elif ' Questionable ' in inactives[c]:
                inactives[c] = inactives[c].split(' Questionable ')
            elif ' Probable ' in inactives[c]:
                inactives[c] = inactives[c].split(' Probable ')
            elif ' Available ' in inactives[c]:
                inactives[c] = inactives[c].split(' Available ')   
            elif ' Out' in inactives[c]:
                inactives[c] = inactives[c].split(' Out')
            elif ' Doubtful' in inactives[c]:
                inactives[c] = inactives[c].split(' Doubtful')             
            elif ' Questionable' in inactives[c]:
                inactives[c] = inactives[c].split(' Questionable')
            elif ' Probable' in inactives[c]:
                inactives[c] = inactives[c].split(' Probable')
            elif ' Available' in inactives[c]:
                inactives[c] = inactives[c].split(' Available')
        
        #change from team names to abbreviations
        for d in range(len(inactives)):
            if 'Celtics' in inactives[d][0]:
                if ' Celtics ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Celtics ')
                    inactives[d][0] = temp[1]
                    inactives[d] = 'BOS&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Celtics')
                    inactives[d][0] = temp[1]
                    inactives[d] = 'BOS&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Nets' in inactives[d][0]:
                if ' Nets ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Nets ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'BKN&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Nets')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'BKN&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Knicks' in inactives[d][0]:
                if ' Knicks ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Knicks ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'NYK&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Knicks')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'NYK&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif '76ers' in inactives[d][0]:
                if ' 76ers ' in inactives[d][0]:
                    temp = inactives[d][0].split(' 76ers ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'PHI&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' 76ers')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'PHI&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')    
            elif 'Raptors' in inactives[d][0]:
                if ' Raptors ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Raptors ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'TOR&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Raptors')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'TOR&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Bulls' in inactives[d][0]:
                if ' Bulls ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Bulls ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'CHI&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Bulls')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'CHI&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Bucks' in inactives[d][0]:
                if ' Bucks ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Bucks ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MIL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Bucks')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MIL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Pacers' in inactives[d][0]:
                if ' Pacers ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Pacers ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'IND&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Pacers')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'IND&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Cavaliers' in inactives[d][0]:
                if ' Cavaliers ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Cavaliers ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'CLE&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Cavaliers')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'CLE&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Pistons' in inactives[d][0]:
                if ' Pistons ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Pistons ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'DET&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Pistons')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'DET&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Hawks' in inactives[d][0]:
                if ' Hawks ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Hawks ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'ATL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Hawks')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'ATL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')    
            elif 'Heat' in inactives[d][0]:
                if ' Heat ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Heat ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MIA&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Heat')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MIA&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Hornets' in inactives[d][0]:
                if ' Hornets ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Hornets ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'CHA&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Hornets')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'CHA&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Magic' in inactives[d][0]:
                if ' Magic ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Magic ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'ORL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Magic')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'ORL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Wizards' in inactives[d][0]:
                if ' Wizards ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Wizards ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'WAS&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Wizards')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'WAS&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Warriors' in inactives[d][0]:
                if ' Warriors ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Warriors ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'GSW&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Warriors')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'GSW&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Lakers' in inactives[d][0]:
                if ' Lakers ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Lakers ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'LAL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Lakers')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'LAL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Suns' in inactives[d][0]:
                if ' Suns ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Suns ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'PHX&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Suns')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'PHX&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Kings' in inactives[d][0]:
                if ' Kings ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Kings ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'SAC&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Kings')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'SAC&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Clippers' in inactives[d][0]:
                if ' Clippers ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Clippers ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'LAC&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Clippers')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'LAC&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Nuggets' in inactives[d][0]:
                if ' Nuggets ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Nuggets ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'DEN&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Nuggets')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'DEN&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Timberwolves' in inactives[d][0]:
                if ' Timberwolves ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Timberwolves ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MIN&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Timberwolves')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MIN&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Thunder' in inactives[d][0]:
                if ' Thunder ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Thunder ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'OKC&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Thunder')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'OKC&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Blazers' in inactives[d][0]:
                if ' Blazers ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Blazers ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'POR&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Blazers')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'POR&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Jazz' in inactives[d][0]:
                if ' Jazz ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Jazz ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'UTA&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Jazz')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'UTA&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Mavericks' in inactives[d][0]:
                if ' Mavericks ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Mavericks ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'DAL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Mavericks')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'DAL&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Spurs' in inactives[d][0]:
                if ' Spurs ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Spurs ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'SAS&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Spurs')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'SAS&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Rockets' in inactives[d][0]:
                if ' Rockets ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Rockets ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'HOU&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Rockets')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'HOU&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Grizzlies' in inactives[d][0]:
                if ' Grizzlies ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Grizzlies ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MEM&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Grizzlies')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'MEM&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
            elif 'Pelicans' in inactives[d][0]:
                if ' Pelicans ' in inactives[d][0]:
                    temp = inactives[d][0].split(' Pelicans ')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'NOP&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')
                else:
                    temp = inactives[d][0].split(' Pelicans')
                    inactives[d][0] = temp[1]        
                    inactives[d] = 'NOP&' + inactives[d][0]+ '&' + inactives[d][1]
                    inactives[d] = inactives[d].split('&')

        for e in range(len(inactives)):
            if len(inactives[e]) == 3:
                temp = inactives[e][0]
            if len(inactives[e]) == 2:
                inactives[e] = temp + '&' + inactives[e][0] + '&' + inactives[e][1]
                inactives[e] = inactives[e].split('&')
            else:
                pass

        inactives = [f for f in inactives if len(f) == 3]

        #last, first --> first last
        for g in range(len(inactives)):
            temp = inactives[g][1]
            temp = temp.split(', ')
            temp = temp[1] + ' ' + temp[0]
            inactives[g][1] = temp

        

        date = file_names[i]
        date = date.replace('_', '/').replace('.pdf', '')
        for h in range(len(inactives)):
            inactives[h].insert(0, date)

        if i !=0:
            inactives = pd.DataFrame(inactives, columns=['Date', 'Team', 'Name', 'Injury'], index = None)
            inactives = inactives[inactives['Team'].isin(day_teams)]
            injury_data = pd.concat([inactives, injury_data], ignore_index = True)
        else:
            injury_data = pd.DataFrame(inactives, columns=['Date', 'Team', 'Name', 'Injury'], index = None)
            injury_data = injury_data[injury_data['Team'].isin(day_teams)]

    injury_data = injury_data.drop_duplicates(subset = ['Date','Name'], keep = 'first' )

    dates = not_injured['Date'].unique()

    for i in tqdm(range(len(dates))):
        #removes players who played but listed in IR
        temp = not_injured[not_injured['Date'] == dates[i]]
        players = temp['Name'].unique()

        temp = injury_data[injury_data['Date'] == dates[i]]
        temp = temp[~temp['Name'].isin(players)]

        if i !=0:
            new_injury_data = pd.concat([temp, new_injury_data], ignore_index=True)
        else:
            new_injury_data = temp

    new_injury_data.to_csv(f"output/{year}/Injury_Data{year}.csv")    
    return new_injury_data

def injury_report_download(year):
    """
    This downloads all the injury report pdfs from the NBA.com for the selected year.

    The input year is the latter year in the season schedule:
    input of 2024 would correspond to the 2023-2024 season.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.86 Safari/537.36'}

    links, file_names = injury_report_links_and_names(year)

    for i in tqdm(range(len(links))):
        response = requests.get(links[i], headers = headers)
        with open(f"output/{year}/Injury Reports/{file_names[i]}", 'wb') as f:
            f.write(response.content)
        time.sleep(0.3)

def injury_report_links_and_names(year, get_only_file_names:bool = False):
    """
    This function creates:
    - links that will then be used to download the needed PDF files locally.
    - file names to save downloaded .pdfs under correct names.
    """
    schedule  = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
    link_dates  = schedule['Date'].unique()
    file_name_dates =  schedule['Date'].to_numpy()
    home = schedule['Team'].to_numpy()
    away = schedule['Opponent'].to_numpy()
    file_names = []

    if get_only_file_names is True:
        #this only gets called in injury_df()
        file_names = [file_name_dates[i] +f"_{away[i]}{home[i]}.pdf" for i in range(len(file_name_dates))]
        return file_names     
    else:
        links = []
        
        for i in range(len(link_dates)):
            links.append(f"https://ak-static.cms.nba.com/referee/injury/Injury-Report_{link_dates[i]}_09PM.pdf")
            file_names.append(link_dates[i]+'.pdf')
        return links, file_names

#%%
if __name__ == "__main__":
#    get_injury_data(2024)
    injury_report_download(2024)
#    injury_report_links_and_names()

#%%
schedule  = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
file_name_dates =  schedule['Date'].to_numpy()
home = schedule['Team'].to_numpy()
away = schedule['Opponent'].to_numpy()
file_names = [file_name_dates[i] +f"_{away[i]}{home[i]}.pdf" for i in range(len(file_name_dates))]