import pandas as pd
from datetime import datetime, timedelta

file = 'data_for_generate_example_data_for_today.csv'

df = pd.read_csv(file, sep=';')

today = datetime.now()
days = datetime(today.year,today.month,today.day) - datetime(2021,3,31)

for i in range(len(df)):
    df.loc[i, 'start_date'] = (datetime.strptime(df.loc[i, 'start_date'], "%d.%m.%Y").date() + days).strftime("%d.%m.%Y")

df.to_csv('example_data'+'_for_'+today.strftime('%d-%m-%Y')+'.csv', index=False, sep=';')
#df.to_csv('main_data.csv', index=False, sep=';')