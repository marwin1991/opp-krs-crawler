
import csv
from msilib.schema import Error
import re
from tkinter import E
import requests
from bs4 import BeautifulSoup

def getLi(dane, name):
    try:
        return str([elem for elem in dane.findAll('li') if name in str(elem.text)][0]).replace("</li>","").replace("<li><strong>" + name + "</strong>","")
    except:
        return ""

def getLiEpit(dane, name):
    try:
        return str([elem for elem in dane.findAll('li') if name in str(elem.text)][0]).replace("</li>","").replace("<li><strong>" + name + "</strong>","")
    except Exception as e:
        return ""
    

with open('C:/Users/Piotr/Desktop/a/dane.csv', newline='') as csvfile:
   writer = csv.writer(open('C:/Users/Piotr/Desktop/a/dane-finall-output.csv', 'w', newline=''), delimiter=',')
   spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
   for row in spamreader:
       r = requests.get('https://www.pitax.pl/rozliczenie-pit-online-' + row[0]+ "/")
       text = r.text
       soup = BeautifulSoup(text)
       dane = soup.find("div", {"id": "opp-address"})
       if dane != None:
           adres =  getLi(dane, "Adres:").replace(",", "")
           www =   getLi(dane, "WWW:").replace(",", "")
           email =   getLi(dane, "E-mail:").replace(",", "")
           telefon =   getLi(dane, "Telefon:").replace(",", "")
           row.append(adres)
           row.append(www)
           row.append(email)
           row.append(telefon)
       else:
           r2 = requests.get('https://www.e-pity.pl/pity-2021/akcja-e-life-jeden-procent-2022-KRS-' + row[0])
           text2 = r2.text
           soup2 = BeautifulSoup(text2)
           dane2 = soup2.find("div", {"class": "opp-data"})
           if dane2 != None:
               adres =  getLiEpit(dane2, "Adres:").replace(",", "")
               www =   BeautifulSoup(getLiEpit(dane2, "www:").replace(",", "")).text
               email =   BeautifulSoup(getLiEpit(dane2, "e-mail:").replace(",", "")).text
               telefon =   getLiEpit(dane2, "Telefon:").replace(",", "") 
               row.append(adres)
               row.append(www)
               row.append(email)
               row.append(telefon)
           else:
               print("Brak danych dla " + row[0])
               row.append("")
               row.append("")
               row.append("")
               row.append("")
       writer.writerow(row)
