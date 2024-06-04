# pip install pandas allows for the module to be used
import pandas as pd
import sqlite3

# CSV file to read
df = pd.read_csv('questions.csv')
# sqlite database uri to connect to i.e instance/db_name.db
conn = sqlite3.connect('instance/farm_smart.db')
# turns the column entries into sql and inserts into database
df.to_sql('Questions', conn, if_exists='replace', index=False)
conn.close()
