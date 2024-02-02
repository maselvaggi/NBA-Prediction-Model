#%%
import time
import requests
import pandas as pd
from tqdm import tqdm
from pypdf import PdfReader

#%%
# These functions are only used to gather DNP/DNDs.
def get_player_DNPs(year):
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
    file_names = box_score_links_and_names(year, get_only_file_names=True)

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

def box_score_download(year):
    """
    This downloads all the box score pdfs from the NBA for the 2022-2023 Season. 
    May need to create a function to be more selective on which pdfs to get in the future.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.86 Safari/537.36'}

    links, file_names = box_score_links_and_names(year)

    for i in tqdm(range(len(links))):
        response = requests.get(links[i], headers = headers)
        with open(f"output/{year}/Box Scores/{file_names[i]}", 'wb') as f:
            f.write(response.content)
        time.sleep(0.3)

def box_score_links_and_names(year, get_only_file_names: bool = False):
    """
    This function creates the links that will then be used to
    download the needed PDF files locally.
    """
    schedule  = pd.read_csv(f"output/{year}/Schedule{year}.csv", index_col = 0)
    date = schedule['Date'].to_numpy()
    home = schedule['Team'].to_numpy()
    away = schedule['Opponent'].to_numpy()

    file_names = []
    if get_only_file_names is True:
        #this only gets called in get_player_DNPs()
        for i in range(len(date)):
            file_names.append(f"{date[i]}_{away[i]}{home[i]}")
            file_names = [i +'.pdf' for i in file_names]
        return file_names       
    else:
        links = []
        for i in range(len(date)):
            file_names.append(f"{date[i]}_{away[i]}{home[i]}")
            links.append(f"https://statsdmz.nba.com/pdfs/{date[i]}/{date[i]}_{away[i]}{home[i]}.pdf")
        
        return links, file_names

if __name__ == "__main__":
    box_score_download()