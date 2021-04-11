import json
from typing import DefaultDict
import copy
import pandas as pd
from pandas import DataFrame

#Disesuaikan dengan directory data Stocklist.xlsx, excluded_word.xlsx, dan result.json
stock_table = pd.read_excel('C:/Users/LENOVO/Documents/Bootcamp/Shift Academy/Data Wrangling/Tasks/10. Scrap Stockbit/StockList.xlsx')
excluded_word = pd.read_excel('C:/Users/LENOVO/Documents/Bootcamp/Shift Academy/Data Wrangling/Tasks/10. Scrap Stockbit/excluded_word.xlsx')
with open('C:/Users/LENOVO/Documents/Bootcamp/Shift Academy/Data Wrangling/Tasks/09. Scrap stock mention/result.json', 'rb') as fp:
    data = json.load(fp)

counter = DefaultDict(int)
bydate = DefaultDict(str)
buffer_date = ''

for chats in data['messages'] :
    try :
        if chats['text'] != '':
            tanggal = chats["date"].split("T")[0]
            pengirim = chats["from"]
            teks = chats["text"].replace("\n"," ").replace(",", " ").replace("."," ").lower()
            teks_perkata = teks.split(" ")
            kode_saham = []
            if tanggal != buffer_date :
                counter = DefaultDict(int)
            else :
                pass
            cek_double = []
            for x in teks_perkata :
                if x not in cek_double :
                    if x in stock_table.Kode.values :
                        if x not in excluded_word.values :
                            kode_saham.append(x)
                            cek_double.append(x)
                            counter[x]+=1
                            bydate[tanggal]=copy.copy(counter)
                        else :
                            continue
                    else :
                        continue
                else :
                    continue
            buffer_date = tanggal
#             print(f'{tanggal} | {pengirim} : {teks} - {kode_saham}')
        else :
            continue
    except :
        continue

stockcode = input('Masukkan kode saham : ')
mention_counter = [bydate[x][stockcode] for x in bydate]
mention_date = [x for x in bydate]
print(stockcode)

df = DataFrame([mention_date,mention_counter]).transpose()
df.columns = ('date','mentions')
print(df)