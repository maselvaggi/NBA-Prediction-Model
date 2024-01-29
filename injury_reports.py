#%%
import requests
import pandas as pd
from tqdm import tqdm
from pypdf import PdfReader
# import numpy as np
# import re
# import time
# from lxml import html
# from lxml import etree
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By

#%%
def injury_df(year):
    """
    """
    #you need advanced.csv and schedule.csv to run this function
    file_names = pdf_names(year)
    schedule = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col=0)
    not_injured = pd.read_csv(f"output/{year}/Traditional{year}.csv", index_col=0)

    for i in tqdm(range(len(file_names))):
        date = file_names[i].replace('_', '/').replace('.pdf', '')
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

#%%
def pdf_names(year):
    """
    This fucntion pulls the matchups from the schedule2223.csv
    file and dates of those matchups to create the names of each 
    downloaded PDF.  These names are used to reference each saved
    PDF.
    """
    schedule  = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
    file_names = schedule['Date'].unique()

    for i in range(len(file_names)):
        day = file_names[i].replace('/', '_')
        day = ''.join([day, '.pdf'])
        file_names[i] = day

    return file_names

def pdf_download(year):
    """
    This downloads all the box score pdfs from the NBA for the 2022-2023 Season. 
    May need to create a function to be more selective on which pdfs to get in the future.
    """
    links = pdf_links(year)
    file_names = pdf_names(year)

    for i in tqdm(range(len(links))):
        response = requests.get(links[i])
        with open(f"output/{year}/Injury Reports/{file_names[i]}", 'wb') as f:
            f.write(response.content)

def pdf_links(year):
    """
    This function creates the links that will then be used to
    download the needed PDF files locally.
    """
    schedule  = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
    date = schedule['Date'].unique()

    for i in range(len(date)):
        day = date[i].split('/')
        day = "-".join([day[2], day[0], day[1]])
        date[i] = day

    links = []

    for i in range(len(date)):
        links.append(f"https://ak-static.cms.nba.com/referee/injury/Injury-Report_{date[i]}_09PM.pdf")
    
    return links

#%%
# These functions are only used to gather DNP/DNDs. Regular Injury Reports
# do not include players who do not see the court. 
# This used the inactives in box scores from nba.com
# the issue is that some players were listed without their full name
# and this created tons of issues trying to verify who was who- especially
# during trade season:
def injury_DNP(year):
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
    file_names = old_pdf_names(year)

    for i in tqdm(range(len(file_names))):
        reader = PdfReader(f"output/{year}/Box Scores/{file_names[i]}")
        page = reader.pages[0]
        text = page.extract_text()

        with open(f"output/{year}/Inactives{year}.txt", 'w') as file:
            file.write(text)

        inactives = open(f"output/{year}/Inactives{year}.txt")
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
                
        # Recombines injuries that got split at ','
        # Also makes sure players with no injuries listed
        # are not attached to another row,
        for n in range(0,2):
            injury[n] = injury[n].split(', ')
            remove = []
            for p in range(len(injury[n])):
                if '(' not in injury[n][p] and ')' in injury[n][p]:
                    injury[n][p-1] = ', '.join([injury[n][p-1],injury[n][p]])
                    injury[n][p].replace(')', '==')
                    remove.append(p)
            injury[n] = [x for y, x in enumerate(injury[n]) if y not in remove]

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
        away, home = file_names[i][9:12], file_names[i][12:15]
        year, month, day = file_names[i][0:4], file_names[i][4:6], file_names[i][6:8]
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
            injury[m] = injury[m].split('=')

        for o in range(len(injury)):
            if len(injury[o]) != 4:
                injury[o] = injury[o][0:3]


        if i !=0:
            temp_injury = pd.DataFrame(injury, columns=['Date', 'Team', 'Name', 'Injury'], index = None)
            injury_data = pd.concat([temp_injury, injury_data], ignore_index = True)
        else:
          injury_data = pd.DataFrame(injury, columns=['Date', 'Team', 'Name', 'Injury'], index = None)
          injury_data

    injury_data = injury_data.dropna()
    injury_data = pd.concat([injury_data[injury_data['Injury'].str.contains('DNP')] , injury_data[injury_data['Injury'].str.contains('DND')]], ignore_index=True)
    injury_data.to_csv(f"output/{year}/DNP{year}.csv")    
    return injury_data

def old_pdf_names(date, home, away):
    """
    This fucntion pulls the matchups from the schedule2023.csv
    file and dates of those matchups to create the names of each 
    downloaded PDF.  These names are used to reference each saved
    PDF.
    """
    file_names = []

    for i in range(len(date)):
        day = date[i].split('/')
        day = "".join([day[2], day[0], day[1]])
        date[i] = day

        file_names.append(f"{date[i]}_{away[i]}{home[i]}")

    return file_names

def old_pdf_download(year):
    """
    This downloads all the box score pdfs from the NBA for the 2022-2023 Season. 
    May need to create a function to be more selective on which pdfs to get in the future.
    """
    links, date, home, away = old_pdf_links(year)
    file_names = old_pdf_names(date, home, away)

    for i in range(len(links)):
        response = requests.get(links[i])
        with open(f"output/{year}/Box Scores/{file_names[i]}", 'wb') as f:
            f.write(response.content)

def old_pdf_links(year):
    """
    This function creates the links that will then be used to
    download the needed PDF files locally.
    """
    schedule  = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
    date = schedule['Date'].to_numpy()
    home = schedule['Team'].to_numpy()
    away = schedule['Opponent'].to_numpy()

    for i in range(len(date)):
        day = date[i].split('/')
        day = "".join([day[2], day[0], day[1]])
        date[i] = day

    links = []

    for i in range(len(date)):
        links.append(f"https://statsdmz.nba.com/pdfs/{date[i]}/{date[i]}_{away[i]}{home[i]}.pdf")
    
    return links, date, home, away

#%% This was the original way to get injury reports:
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
    pdf_download()
