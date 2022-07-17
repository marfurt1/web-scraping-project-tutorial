# your app code here
import pandas as pd
import requests 
import sqlite3
from bs4 import BeautifulSoup

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

soup = BeautifulSoup(html_data,"html.parser")
tablas = soup.findAll("table")
tablas

for i, tabla in enumerate(tablas):
    if ("Tesla Quarterly Revenue" in str(tabla)): 
        indice_que_busco = i 
#enumerate me asigna un índice y el contenido que encuentra
df = pd.DataFrame(columns=["date","revenue"])

tablas[indice_que_busco]

for fila in tablas[indice_que_busco].tbody.find_all("tr"):
    datos= fila.find_all("td")

datos

datos[0]

datos[1].text

for fila in tablas[indice_que_busco].tbody.find_all("tr"):
    datos= fila.find_all("td")
    if len(datos)>0:
        fecha=datos[0].text
        revenue=datos[1].text.replace("$","").replace(",","")
        df = df.append({"date":fecha,"revenue":revenue},ignore_index=True)
df.tail()


df=df[df["revenue"]!=""]

df.tail()

type(df)

records = df.to_records(index=False)
list_of_tuples = list(records)
list_of_tuples


# Use the connect() function of sqlite3 to create a database. It will create a connection object.
connection = sqlite3.connect('Tesla.db')

 #Let's create a table in our database to store our revenue values.

c = connection.cursor()

# Create table
c.execute('''CREATE TABLE revenue
             (Date, Revenue)''')


# Insert the values
c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)
# Save (commit) the changes
connection.commit()

#Now retrieve the data from the database

for row in c.execute('SELECT * FROM revenue'):
    print(row)


"""#Result:
database name  “Tesla.db”. We saved the connection to the connection object.
#Next time we run this file, it just connects to the database, and if the database 
is not there, it will create one."""
