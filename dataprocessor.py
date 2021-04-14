import pandas as pd
from pandas import DataFrame
import calendar as cal
import os
from typing import DefaultDict
import copy
import datetime
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class DataProcessor():

    def __init__(self, filepath=None):
        self.__filepath = filepath
        self.stock_table = pd.read_excel(r'files\StockList.xlsx')
        self.excluded_word = pd.read_excel(r'files\excluded_word.xlsx')
        self.awal = '0000'
        self.akhir = '0000'
        self.df = None
        self.dffilter = None

    '''
    load data, hanya menerima .csv, .json, .pkl
    '''
    def load(self, filepath):
        __, fileext = os.path.splitext(filepath)
        if('json' in fileext): # json
            self.df = pd.read_json(filepath)
        elif('csv' in fileext): # csv
            self.df = pd.read_csv(filepath)
        elif('pkl' in fileext): # csv
            self.df = pd.read_pickle(filepath)
        else: #
            return 'hanya menerima file csv, pickel dan json'
        return 'load file berhasil'

    '''
    method utk mendapatkan list kode saham dari data chat
    '''
    def getKodeSaham(self):
        # iterate over range
        lstKode = set()
        texts = ','.join([i.lower() for i in self.dffilter['text'] if  isinstance(i,str)])
        # for i in self.stock_table.Kode.values:
        #     if i.lower() in texts:
        #         lstKode.add(i.upper())
        for i in range(len(self.stock_table.Kode)):
            if self.stock_table.Kode[i].lower() in texts:
                lstKode.add('{} - {}'.format(self.stock_table.Kode[i].upper(),self.stock_table.Company[i]))
        lst = list(lstKode)
        lst.sort()
        return lst

    '''
    method utk memfilter data berdasarkan range yg dipilih, disimpan dalam df baru
    '''
    def filter(self, awal = '0000', akhir='0000'):
        is_all = True
        if('0000' in awal and '0000' in akhir):
            pass # sementara tidak dilakukan, data terlalu besar
        elif('0000' not in awal and '0000' in akhir):
            is_all = False
            self.awal = awal
            d = datetime.datetime.strptime(self.awal, '%Y-%m')
            self.awal = str(d.year)+'-{:02d}'.format(d.month)+'-{:02d}'.format(d.day)
            self.akhir = str(d.year)+'-{:02d}'.format(d.month)+'-{:02d}'.format(cal.monthrange(d.year, d.month)[1])
        else:
            is_all = False
            da = datetime.datetime.strptime(awal, '%Y-%m')
            self.awal = str(da.year)+'-{:02d}'.format(da.month)+'-{:02d}'.format(da.day) #datetime.datetime.strptime(awal, '%Y-%m')
            #str(da.year)+'-{:02d}'.format(da.month)+'-{:02d}'.format(da.day)
            dk = datetime.datetime.strptime(akhir, '%Y-%m')
            self.akhir = str(dk.year)+'-{:02d}'.format(dk.month)+'-{:02d}'.format(cal.monthrange(dk.year, dk.month)[1]) #datetime.datetime.strptime(akhir, '%Y-%m')
            #str(dk.year)+'-{:02d}'.format(dk.month)+'-{:02d}'.format(dk.day)
        if is_all:
            self.dffilter = pd.DataFrame([x for x in self.df['messages']])[['date','text']]
        else:
            self.dffilter = pd.DataFrame([x for x in self.df['messages'] if datetime.datetime.strptime(x['date'][:10], '%Y-%m-%d') >= datetime.datetime.strptime(self.awal, '%Y-%m-%d') and datetime.datetime.strptime(x['date'][:10], '%Y-%m-%d') <= datetime.datetime.strptime(self.akhir, '%Y-%m-%d')])[['date','text']]
        return self

    def getCount(self, stockcode):
        stockcode = stockcode.lower()
        __date = 0
        __text = 1
        counter = DefaultDict(int)
        bydate = DefaultDict(str)
        buffer_date = ''
        for index, row in self.dffilter.iterrows() :
            # try:
            if row[__text] != '' and isinstance(row[__text], str):
                tanggal = row[__date].split("T")[0]
                teks = row[__text].replace("\n"," ").replace(",", " ").replace("."," ").lower()
                teks_perkata = teks.split(" ")
                kode_saham = []
                if tanggal != buffer_date :
                    counter = DefaultDict(int)
                else :
                    pass
                cek_double = []
                for x in teks_perkata :
                    if x not in cek_double :
                        if x in self.stock_table.Kode.values :
                            if x not in self.excluded_word.values :
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
                # teks_rep = ' '.join([x for x in teks if x not in self.excluded_word.values])
                # if teks_rep.find(stockcode) != -1: # diganti ini
                #     counter[stockcode]+=1
                #     bydate[tanggal]=copy.copy(counter)
                buffer_date = tanggal
            else :
                continue
            # except:
            #     print('error ', row)
            #     continue


        mention_counter = [bydate[x][stockcode] for x in bydate]
        mention_date = [x for x in bydate]

        df = pd.DataFrame([mention_date,mention_counter]).transpose()
        df.columns = ('date','mentions')
        print(df.tail())
        return df[(df['date'] >= self.awal) & (df['date'] <= self.akhir)]

    '''
    mendapatkan pergerakan harga saham dari yahoo finance
    '''
    def getPergerakanHargaSaham(self, stockcode):
        check_stockcode = stockcode.find(".JK")

        if check_stockcode == -1:
            stockcode = (stockcode+".JK")
        else:
            stockcode
        #Input stockcode ke Yahoo Finance
        stockinfo = yf.download(stockcode, start="{}".format(self.awal), end="{}".format(self.akhir))
        stock_price = stockinfo['Adj Close']
        #Mengambil Nama Perusahaan
        company_info = yf.Ticker("{}".format(stockcode))
        company_name = company_info.info["longName"]
        return '{} [{}]'.format(company_name, stockcode.upper()), stock_price, DataFrame(stock_price)

    '''
    sanding data, memasukkan informasi price ke dataframe lain, utk keperluan plotting
    '''
    def sandingData(self, dfa, stockprice):
        dfprice = DataFrame(stockprice)
        # ubah index jadi column
        dfprice['date'] = dfprice.index
        # proses menyandingkan data mentions dengan price berdasarkan tanggal
        dfa_date = dfa['date'].tolist()
        dfp1 = dfprice[dfprice['date'].isin(dfa_date)]
        dfp1['date'] = dfp1['date'].astype(str)
        dfa1 = dfa[dfa['date'].isin(dfp1['date'].tolist())]
        # add new column: price
        dfa1['price'] = dfp1['Adj Close'].tolist()
        dfa2 = dfa1.copy(deep=True)
        # normalisasi
        mention_max = dfa1['mentions'].max()
        mention_min = dfa1['mentions'].min()
        price_max = dfa1['price'].max()
        price_min = dfa1['price'].min()
        # dfa1['mentions'] = (dfa1['mentions']/(mention_max if mention_max > 0 else 1))*100
        # dfa1['price'] = (dfa1['price']/(price_max if price_max > 0 else 1))*100
        dfa1['mentions'] = ((dfa1['mentions']-mention_min)/((mention_max-mention_min) if (mention_max-mention_min) > 0 else 1))*100
        dfa1['price'] = ((dfa1['price']-price_min)/((price_max-price_min) if (price_max-price_min) > 0 else 1))*100
        return dfa1, dfa2

    def plot(self, root, dfa1, company_name):
        print('plot')
        figure1 = plt.Figure(figsize=(9,5), dpi=100)
        ax1 = figure1.add_subplot(111)
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().grid(row=0, column=2)
        df1 = dfa1[['date','mentions']].groupby('date').sum()
        df1.plot( kind='line', legend=True, ax=ax1, color='skyblue',marker='o', fontsize=10)
        df2 = dfa1[['date', 'price']].groupby('date').sum()
        df2.plot( kind='line', legend=True, ax=ax1, marker='', color='olive', linewidth=2)
        # plt.legend()
        ax1.set_title("Pergerakan Harga Saham "+company_name)


        # plt.figure(figsize=(15,6))
        # plt.title("Pergerakan Harga Saham "+company_name)
        # plt.plot(stock_price)
        # plt.plot( 'date', 'mentions', data=dfa1, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
        # plt.plot( 'date', 'price', data=dfa1, marker='', color='olive', linewidth=2)
        # show legend
        # plt.legend()
        # show graph
        # plt.show()

    def corr(self, dfa):
        dfa['mentions']=np.float64(dfa['mentions'])
        dfa['price']=np.float64(dfa['price'])
        return dfa['mentions'].corr(dfa['price'])
