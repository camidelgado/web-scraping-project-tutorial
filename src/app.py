# your app code here

!pip install pandas
!pip install sqlite3

import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
import numpy as np

!pip install tqdm
import tqdm 

url='https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
pagina=requests.get(url)
pagina_texto=pagina.text

print(pagina)

texto_beauty=BeautifulSoup(pagina_texto,'html.parser')

type(texto_beauty)
Tables=texto_beauty.findAll('table') 
#aca esta listando todas las tablas que estan en el html
print(len(Tables))
id_table_quarter=None
for i in range(len(Tables)):
    if 'Tesla Quarterly Revenue' in str(Tables[i]):
        id_table_quarter=+ i
        print('El contenido se encuentra en:', id_table_quarter)
        break

table_quarter =Tables[1]
table_quarter_body=table_quarter.tbody
table_quarter_body

lista_tr=table_quarter_body.find_all("tr")
lista_tr


revenue=[]

for tr in tqdm.tqdm(lista_tr):
    all_tr=tr.find_all('td')
    date=all_tr[0].text
    data=all_tr[1].text
    revenue.append([date,data])
    #print('*'*10)
    #print(len(date),date)
    #print(date[0].text,date[1].text) 
    #de esta forma agarro la fecha y el valor
print(revenue)


revenue_df=pd.DataFrame(revenue, columns=['Date','Revenue'])
revenue_df.head()

elemento=revenue_df['Revenue'][0]
elemento=elemento.replace("$", "")
elemento=elemento.replace(",", "")
elemento

def preproces(row):
    row=row.replace("$", "")
    row=row.replace(",", "")
    if row=='':
        return np.nan   
    return float(row)

revenue_df['Revenue']=revenue_df['Revenue'].apply(preproces)
revenue_df

revenue_df.dropna(subset='Revenue')

revenue_df.to_csv('revenue_df.csv', index=None)

conn=sqlite3.Connection('Tesla.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE rev
             (Date, Revenue)''')

records = revenue_df.to_records(index=False)
list_of_tuples = list(records)

# Insert the values
c.executemany('INSERT INTO rev VALUES (?,?)', list_of_tuples)
# Save (commit) the changes
conn.commit()

for row in c.execute('SELECT * FROM rev'):
    print(row)