#%%
import pandas as pd
from sqlalchemy import create_engine

#%%
schedule = pd.read_csv('output/Schedule2223.csv', index_col=0)
schedule
#%%
engine = create_engine('postgresql://postgres:20171847@localhost:5432/NY17')
field_data.to_sql('field_data', engine)

#%%
conn = psycopg2.connect(database = 'NY17', user = 'postgres', password = '20171847', host = 'localhost', port = '5432')

cursor = conn.cursor()

sql = 'DROP TABLE data'

cursor.execute(sql)

conn.commit()
conn.close()
# %%
