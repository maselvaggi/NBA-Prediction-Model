# %%
import pandas as pd
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from Traditional import *
from Advanced import *
from Injury_reports import *


"""
This script will contain code to actually run the model.
Right now, just being used for sparse testing. 
"""
# %%
traditional = pd.read_csv("Traditional.csv", index_col = 0)
advanced    = pd.read_csv("Advanced.csv", index_col = 0)
traditional = traditional.sort_values(by = ['Date', 'Name'])
advanced = advanced.sort_values(by = ['Date', 'Name'])

#%%
traditional = traditional.sort_values(by = ['Date', 'Name'])
advanced = advanced.sort_values(by = ['Date', 'Name'])
defrtg = advanced['DEFRTG'].to_numpy()
model_data = traditional[['Name', 'Mins', 'Points']]
model_data['DEFRTG'] = defrtg
model_data.to_csv('Model_data_Dirty.csv')
#%%
model_data = pd.read_csv('Model_data_Dirty.csv', index_col = 0)
# %%
season_stats = Trad_seasonal_stats(traditional)

# %%
season_stats.to_csv('Season_Stats.csv')
season_stats

# %% [markdown]
# -------------------TRADITIONAL BOX SCORES-------------------

#%%
trad = scrape_all_Trad()
trad
# %%
trad = scrape_new_Trad()
trad

#%%
adv = scrape_new_ADV()
adv
#%%
test_t = traditional
test_a = advanced
                
#%%
traditional = pd.read_csv("Traditional.csv", index_col = 0)
#season_stats = Trad_seasonal_stats(traditional)
# -------------------ADVANCED BOX SCORES-------------------
#%%
advanced = pd.read_csv("Advanced.csv", index_col = 0)
advanced

#%%
player = advanced[advanced['Name'] == 'Mikal Bridges']

#%%
mins = player["Mins"].sum()
ratio = []
for i in range(len(player['Name'])):
    ratio.append(player['Mins'].iloc[i]/mins)

#%%
len(ratio)

for i in range(len(ratio)):
    player['OFFRTG'].iloc[i] = player['OFFRTG']*ratio[i]

#%%
player['OFFRTG'] = ratio
player["OFFRTG"]

#%%
player