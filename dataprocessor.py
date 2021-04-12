import pandas as pd
import calendar as cal
import os
from typing import DefaultDict
import copy
import datetime

class DataProcessor():

    def __init__(self, filepath=None):
        self.__filepath = filepath
        self.stock_table = pd.read_excel(r'files\StockList.xlsx')
        self.excluded_word = pd.read_excel(r'files\excluded_word.xlsx')
        self.__listKodeSaham = ['AALI','LSIP','BWPT','SIMP','SSMS','SMAR','SGRO','DSNG','PALM','ANDI','CSRA','UNSP','MGRO','GZCO','ANJT','JAWA','MAGP','PSGO','PGUN','PNGO','GOLL','KLSE-LAGENDA','FAPA','BISI','BEEF','DSFI','MNCN','SCMA','FILM','LINK','ABBA','DMMX','IPTV','VIVA','EMTK','MSIN','MARI','JTPE','MDIA','KBLV','MSKY','TMPO','LPLI','BLTZ','FORU','WIFI','BMTR','SRTG','KREN','BHIT','MLPL','BNBR','POOL','ABMM','PEGE','NICK','MGNA','PLAS','OCAP','LPPF','ACES','ERAA','MAPI','RALS','MPPA','AMRT','TELE','MCAS','MAPA','RANC','HERO','KIOS','GLOB','DIVA','NFCX','MIDI','CSAP','MKNT','KOIN','ECII','DAYA','SONA','SKYB','TRIO','UNTR','AKRA','IRRA','MPMX','HEXA','HKMU','SQMI','KAYU','SPTO','KOBX','CLPI','LTLS','BOGA','EPMT','OKAS','DWGL','OPMS','TGKA','TFAS','CARS','BMSR','ZBRA','MICE','SGER','DPUM','FISH','BLUE','SDPC','TURI','WICO','WAPO','INTA','APII','HDIT','PMJS','AYLS','INPS','INTD','TIRA','MDRN','HADE','CNKO','AIMS','AGAR','KONI','KMDS','TRIL','SUGI','GREN','MTDL','ASGR','LUCK','ENVY','MLPT','DCII','DNET','LMAS','DIGI','CASH','ATIC','GLVA','TECH','EDGE','DUCK','PZZA','KPIG','FAST','MAMI','HRME','IKAI','HOME','NATO','PJAA','MAPB','EAST','PANR','NUSA','ICON','MINA','FITT','BUVA','AKKU','CLAY','DFAM','PGLI','BAYU','SHID','JIHD','SOTS','PDES','JSPT','ARTA','PTSP','PSKT','UANG','HOTL','PNSE','CSMI','ESTA','JGLE','PGJO','NASA','MAMIP','PLAN','DYAN','YELO','BOLA','MFMI','ITMA','SOSS','SIMA','INDX','GEMA','RONY','SFAN','UFOE','MIKA','SILO','SAME','HEAL','CARE','PRDA','PRIM','SRAJ','DGNS','PNIN','VINS','MTWI','ASJT','LIFE','LPGI','TUGU','BHAT','AMAG','AHAP','ASRM','ASDM','ASMI','MREI','ASBI','ABDA','JMAS','ADMF','BFIN','IMJS','WOMF','CFIN','POLA','MFIN','TIFA','FINN','VRNA','FUJI','IBFN','HDFA','BBLD','TRUS','DEFI','BPFI','BBRI','BBCA','BMRI','BBNI','BRIS','BBTN','BBKP','BJTM','AGRO','BTPS','BJBR','BNGA','BNLI','BDMN','ARTO','BNII','BANK','BEKS','BTPN','PNBS','BACA','MCOR','PNBN','BGTG','BABP','BNBA','BBHI','INPC','MEGA','BBYB','NISP','BSIM','BVIC','AMAR','BKSW','NOBU','BINA','MAYA','AGRS','BMAS','DNAR','SDRA','BBSI','BBMD','BCIC','BSWD','PANS','TRIM','PADI','RELI','YULE','AMOR','PNLF','BCAP','SMMA','APIC','VICO','LPPS','CASA','GSMF','BPII','ICBP','INDF','MYOR','ULTJ','CLEO','HOKI','AISA','GOOD','TBLA','ROTI','CAMP','CEKA','ADES','FOOD','IKAN','KEJU','MLBI','DLTA','STTP','DMND','BUDI','COCO','PCAR','BTEK','IIKP','PANI','SKBM','SKLT','ENZO','PSDN','ALTO','PMMP','KLBF','KAEF','SIDO','INAF','TSPC','PEHA','PYFA','MERK','DVLA','SOHO','SCPI','GGRM','HMSP','WIIM','ITIC','RMBA','WOOD','KICI','CINT','LMPI','CBMF','SOFA','UNVR','KINO','KPAS','MRAT','TCID','MBTO','VICI','HRTA','TOYS','WSKT','WIKA','ADHI','PTPP','WEGE','SSIA','ACST','TOTL','NRCA','TOPS','CSIS','SKRN','DGIK','JKON','IDPR','PBSA','TAMA','MTRA','PTDU','PWON','CTRA','BSDE','SMRA','KIJA','ASRI','PPRO','APLN','DMAS','LPKR','BEST','BKSL','LPCK','JRPT','DILD','KBAG','BCIP','PAMG','TRIN','DADA','MMLP','MDLN','REAL','RBMS','POSA','GPRA','MYRX','ELTY','POLL','KOTA','RIMO','BAPI','GWSA','CPRI','MTLA','RODA','DUTI','TARA','CITY','GAMA','NZIA','BAPA','BIPP','LAND','URBN','FORZ','ASPI','BBSS','MKPI','INPP','MPRO','MABA','RISE','BKDP','MTSM','RDTX','SMDM','GMTD','POLI','FMII','OMRE','PUDP','ARMY','PLIN','SATU','DART','NIRO','BIKA','AMAN','LCGP','EMDE','COWL','MYRXP','INDO','PURI','ROCK','HOMI','ATAP','SRIL','UCID','PBRX','INDR','SBAT','POLY','STAR','POLU','BELL','TFCO','TRIS','ESTI','ERTX','ZONE','ARGO','SSTM','RICY','MYTX','CNTB','CNTX','HDTX','UNIT','ASII','GJTL','IMAS','AUTO','SMSM','GDYR','INDS','MASA','BOLT','BRAM','LPIN','PRAS','NIPS','BATA','BIMA','KBLI','CCSI','KBLM','SCCO','VOKS','IKBI','JECC','JSKY','PTSN','SLIS','SCNP','GMFI','KPAL','ARKA','AMIN','KRAH','ADRO','PTBA','ITMG','HRUM','INDY','BUMI','DOID','PTRO','FIRE','TRAM','MBAP','BOSS','MYOH','DEWA','TOBA','BYAN','SMMT','BSSR','KKGI','DSSA','ARII','SMRU','GTBO','BORN','GEMS','ANTM','INCO','TINS','MDKA','ZINC','PSAB','DKFT','BRMS','CITA','IFSH','ELSA','MEDC','ENRG','BIPI','WOWS','ARTI','APEX','PKPK','RUIS','SURE','MTFN','MITI','UNIQ','CTTH','FPNI','PBID','ESIP','IPOL','IGAR','EPAC','APLI','IMPC','AKPI','YPAS','SMKL','BRNA','TRST','TALF','INKP','TKIM','SWAT','KDSI','SPMA','ALDO','INRU','FASW','KBRI','KRAS','NIKL','ISSP','PURE','GDST','BTON','BAJA','PICO','TBMS','LION','INAI','GGRP','ALKA','ALMI','LMSH','CTBN','JKSW','MARK','TOTO','ARNA','CAKK','MLIA','KIAS','AMFG','BRPT','TPIA','EKAD','AGII','ESSA','ADMG','TDPM','SRSN','MDKI','INCI','UNIC','DPNS','MOLI','SAMF','ETWA','JPFA','CPIN','MAIN','CPRO','SIPD','WMUU','SMGR','INTP','WSBP','WTON','SMBR','SMCB','BEBS','IFII','SULI','SINI','TIRT','INCF','KMTR','INOV','GIAA','BULL','SOCI','MBSS','ASSA','BIRD','SMDR','DEAL','PURA','TCPI','IPCM','PSSI','LEAD','TMAS','JAYA','RIGS','SDMU','TAMU','SHIP','TRUK','TAXI','TPMA','WINS','TNCA','AKSI','IATA','WEHA','HELI','NELY','LRNA','PORT','CMPP','SAPX','CANI','BPTR','BLTA','MIRA','HITS','BESS','KJEN','BBRM','PTIS','SAFE','PPGL','TRJA','JSMR','IPCC','META','CMNP','CASS','KARW','TEBE','TLKM','EXCL','FREN','ISAT','JAST','BTEL','TOWR','TBIG','PPRE','CENT','MTPS','BUKK','BALI','GOLD','GHON','PTPW','IBST','LCKM','OASA','SUPR','PGAS','POWR','RAJA','TGRA','KEEN','MPOW','KOPI','LAPD']
        self.awal = '0000'
        self.akhir = '0000'

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
            print('hanya menerima file csv, pickel dan json')
            return

    '''
    method utk mendapatkan list kode saham dalam rentang waktu tertentu
    '''
    def getKodeSaham(self):
        # iterate over range
        lstKode = set()
        texts = ','.join([i.lower() for i in self.dffilter['text'] if  isinstance(i,str)])
        for i in self.__listKodeSaham:
            if i.lower() in texts:
                lstKode.add(i)
        lst = list(lstKode)
        lst.sort()
        return lst

    '''
    method utk memfilter data berdasarkan range yg dipilih, disimpan dalam df baru
    '''
    def filter(self, awal = '0000', akhir='0000'):
        is_all = False
        if('0000' in awal and '0000' in akhir):
            pass
        elif('0000' not in awal and '0000' in akhir):
            is_all = True
            self.awal = awal
            d = datetime.datetime.strptime(self.awal, '%Y-%m')
            self.awal = str(d.year)+'-{:02d}'.format(d.month)+'-{:02d}'.format(d.day)
            self.akhir = str(d.year)+'-{:02d}'.format(d.month)+'-{:02d}'.format(calendar.monthrange(d.year, d.month)[1])
        else:
            is_all = True
            da = datetime.datetime.strptime(awal, '%Y-%m')
            self.awal = datetime.datetime.strptime(awal, '%Y-%m')
            #str(da.year)+'-{:02d}'.format(da.month)+'-{:02d}'.format(da.day)
            dk = datetime.datetime.strptime(akhir, '%Y-%m')
            self.akhir = datetime.datetime.strptime(akhir, '%Y-%m')
            #str(dk.year)+'-{:02d}'.format(dk.month)+'-{:02d}'.format(dk.day)
        if is_all:
            self.dffilter = pd.DataFrame([x for x in self.df['messages'] if datetime.datetime.strptime(x['date'][:10], '%Y-%m-%d') >= self.awal and datetime.datetime.strptime(x['date'][:10], '%Y-%m-%d') <= self.akhir])[['date','text']]
        else:
            self.dffilter = pd.DataFrame([x for x in self.df['messages']])[['date','text']]
        return self

    def getCount(self, stockcode):
        print(stockcode)
        counter = DefaultDict(int)
        bydate = DefaultDict(str)
        buffer_date = ''

        for row in self.dffilter.iterrows() :
            try:
                if chats != '':
                    tanggal = chats["date"].split("T")[0]
                    teks = self.dffilter["text"].replace("\n"," ").replace(",", " ").replace("."," ").lower()
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
                    buffer_date = tanggal
                else :
                    continue
            except:
                continue


        mention_counter = [bydate[x][stockcode] for x in bydate]
        mention_date = [x for x in bydate]

        df = pd.DataFrame([mention_date,mention_counter]).transpose()
        df.columns = ('date','mentions')
        print(df.tail())
        return df

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
        return company_name, stock_price, Dataframe(stock_price)

    def sandingData(self, dfa, stockprice):
        dfprice = DataFrame(stock_price)
        # ubah index jadi column
        dfprice['date'] = dfprice.index
        # proses menyandingkan data mentions dengan price berdasarkan tanggal
        dfa_date = dfa['date'].tolist()
        dfp1 = dfprice[dfprice['date'].isin(dfa_date)]
        dfp1['date'] = dfp1['date'].astype(str)
        dfa1 = dfa[dfa['date'].isin(dfp1['date'].tolist())]
        # add new column: price
        dfa1['price'] = dfp1['Adj Close'].tolist()
        # normalisasi
        dfa1['mentions'] = (dfa1['mentions']/dfa1['mentions'].max())*100
        dfa1['price'] = (dfa1['price']/dfa1['price'].max())*100
        return dfa1

    def plot(self, dfa1):
        plt.figure(figsize=(15,6))
        plt.title("Pergerakan Harga Saham "+company_name)
        # plt.plot(stock_price)
        plt.plot( 'date', 'mentions', data=dfa1, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
        plt.plot( 'date', 'price', data=dfa1, marker='', color='olive', linewidth=2)
        # show legend
        plt.legend()
        # show graph
        plt.show()
