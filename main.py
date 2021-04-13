from tkinter import Tk, Text, messagebox, BOTH, W, N, E, S, StringVar, IntVar, HORIZONTAL, SOLID, END
from tkinter.ttk import Frame, Button, Label, Style, Checkbutton, Combobox, Separator, Progressbar
from tkinter import filedialog as fd
import pandas as pd
from dataprocessor import DataProcessor
import datetime


class Application(Frame):

    def __init__(self):
        super().__init__()
        self.is_all_data = IntVar()
        self.selected_month_1 = StringVar()
        self.selected_year_1 = StringVar()
        self.selected_month_2 = StringVar()
        self.selected_year_2 = StringVar()
        self.selected_saham = StringVar()
        self.dp = DataProcessor()

        self.initUI()

    def initUI(self):

        self.master.title("Analisa Harga Saham")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.lbl = Label(self, text="Filename: ")
        self.lbl.grid(sticky=W, pady=4, padx=5, columnspan=4)

        self.right_frame = Frame(self, width=800, height=400, borderwidth = 1)
        self.right_frame.grid(row=2, column=1, columnspan=5, rowspan=4,
            padx=5, sticky=E+W+S+N)
        self.right_frame.config(relief=SOLID)
        self.area = Text(self.right_frame, height = 30, width = 40)
        self.area.grid(row=0, column=1,
            padx=5, sticky=W+S+N+E)
        # upload
        # lblUpload = Label(self, text="upload")
        # lblUpload.grid(row=1, column=0, columnspan=2)
        abtn = Button(self, text="Upload", command=self.openFile)
        abtn.grid(row=1, column=0, sticky=W, padx=5)
        self.left_frame = Frame(self, width=200, height=400, borderwidth = 1)
        self.left_frame.grid(row=2, column=0)
        self.left_frame.config(relief=SOLID)
        # self.chkBox = Checkbutton(self.left_frame, text = "All data", variable=self.is_all_data, command=self.cbCallback)
        # self.chkBox.grid(row=1, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=2, columnspan=1, ipadx=75, padx=5, sticky=W)
        self.rangeFrame = self.rangeFrame() #Frame(self.left_frame, borderwidth = 1)
        self.rangeFrame.grid(row=3, column=0, columnspan=2)

        # Button Filter
        btnFilter = Button(self.left_frame, text="Filter", command=self.filter)
        btnFilter.grid(row=4, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=5, columnspan=1, ipadx=75, padx=5, sticky=W)

        # Combobox Pilih Saham
        # self.kodeSaham = []
        # with open('StockList.csv') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)
        #     for row in csv_reader:
        #         self.kodeSaham.append(row['Kode'].upper()) # Kode untuk mengambil data dari stocklist kolom kode
        # self.kodeSaham.sort()
        self.txSaham = Text(self.left_frame)

        self.cbSaham = Combobox(self.left_frame, textvariable=self.selected_saham)
        self.cbSaham['values'] = [] #self.kodeSaham
        self.cbSaham['state'] = 'readonly'  # normal
        self.cbSaham.set('-- Pilih Saham --')
        self.cbSaham.grid(row=7, column=0,padx=5, pady=5)

        # Buton Proses
        btnProses = Button(self.left_frame, text="proses", command=self.proses)
        btnProses.grid(row=8, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=9, columnspan=1, ipadx=75, padx=5, sticky=W)
        # progressbar
        self.pb = Progressbar(
            self.left_frame,
            orient='horizontal',
            mode='indeterminate',
            length=150
        )
        self.pb.start()
        # self.pb.grid(column=0, row=10, columnspan=2, padx=10, pady=20)


    def rangeFrame(self):
        frame = Frame(self.left_frame, borderwidth = 1)
        months = ('01-Jan', '02-Feb', '03-Mar', '04-Apr', '05-May', '06-Jun',
        '07-Jul', '08-Aug', '09-Sep', '10-Oct', '11-Nov', '12-Dec')
        years = (2018, 2019, 2020, 2021)

        lblFrom = Label(frame, text='Dari')
        lblFrom.grid(row=1, column=0, sticky=W, padx=5)
        # start bulan
        month_cb_1 = Combobox(frame, textvariable=self.selected_month_1)
        month_cb_1['values'] = months
        month_cb_1['state'] = 'readonly'  # normal
        month_cb_1.set('-- Pilih bulan --')
        month_cb_1.grid(row=2, column=0,padx=5, pady=5)
        # start tahun
        year_cb_1 = Combobox(frame, textvariable=self.selected_year_1)
        year_cb_1['values'] = years
        year_cb_1['state'] = 'readonly'  # normal
        year_cb_1.set('-- Pilih tahun --')
        year_cb_1.grid(row=3, column=0,padx=5, pady=5)
        lblTo = Label(frame, text='Ke')
        lblTo.grid(row=4, column=0, sticky=W, padx=5)
        # end bulan
        month_cb_2 = Combobox(frame, textvariable=self.selected_month_2)
        month_cb_2['values'] = months
        month_cb_2['state'] = 'readonly'  # normal
        month_cb_2.set('-- Pilih bulan --')
        month_cb_2.grid( row=5, column=0,padx=5, pady=5)
        # end tahun
        year_cb_2 = Combobox(frame, textvariable=self.selected_year_2)
        year_cb_2['values'] = years
        year_cb_2['state'] = 'readonly'  # normal
        year_cb_2.set('-- Pilih tahun --')
        year_cb_2.grid(row=6, column=0,padx=5, pady=5)
        return frame

    # open data file
    def openFile(self):
        name = fd.askopenfilename()
        self.lbl['text'] = self.lbl['text']+' '+name
        self.dp.load(name)

    # show and hide frame
    def cbCallback(self):
        if(self.is_all_data.get() == 1):
            self.rangeFrame.grid_forget()
        else:
            self.rangeFrame.grid()

    '''
    filter data berdasarkan bulan dipilih
    '''
    def filter(self):
        if self.dp.df is None:
            messagebox.showerror("Error", "Data kosong")
            return
        if(self.is_all_data.get()==1):
            self.dp.filter(awal = '0000', akhir='0000')
        else:
            if('Pilih' not in ''.join([self.selected_year_1.get(),self.selected_month_1.get()]) and 'Pilih' in ''.join([self.selected_year_2.get(),self.selected_month_2.get()])):
                self.dp.filter(awal = str(self.selected_year_1.get())+'-'+self.selected_month_1.get()[:2], akhir = '0000')
            else:
                awal = str(self.selected_year_1.get())+'-'+self.selected_month_1.get()[:2]
                akhir = str(self.selected_year_2.get())+'-'+self.selected_month_2.get()[:2]
                if datetime.datetime.strptime(awal, '%Y-%m') > datetime.datetime.strptime(akhir, '%Y-%m'):
                    messagebox.showerror("Error", "Waktu awal > Waktu akhir")
                    return
                self.dp.filter(awal = awal, akhir = akhir)
        print(self.dp.dffilter)
        lst = self.dp.getKodeSaham()
        self.cbSaham['values'] = lst

    '''
    sanding data dari 2 paket data: mentions counter dan price dari yfinance
    plot line graph
    '''
    def proses(self):
        if self.dp.dffilter is None:
            messagebox.showerror("Error", "Data kosong")
            return
        stockcode = self.cbSaham.get()
        '''if(len(self.txSaham.get())>0):
            stockcode = self.txSaham.get()'''
        # menghitung frekuensi mentions saham di chat
        dfa = self.dp.getCount(stockcode)
        print(dfa.shape)
        # mendapatkan stock price's series from yahoo finance
        company_name, stockprice, dfstock = self.dp.getPergerakanHargaSaham(stockcode)
        print(dfstock.shape)
        # sanding data
        dfnorm, dfbefnorm = self.dp.sandingData(dfa, stockprice)
        self.area.delete('1.0', END)
        self.area.insert(END, 'correlation {0}\n\n {1}'.format(self.dp.corr(dfnorm), dfbefnorm))
        # plot
        self.dp.plot(self.right_frame, dfnorm, company_name)

def main():

    root = Tk()
    root.geometry("1450x550+300+300")
    app = Application()
    root.mainloop()


if __name__ == '__main__':
    main()
