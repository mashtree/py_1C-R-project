from tkinter import Tk, Text, messagebox, BOTH, W, N, E, S, StringVar, IntVar, HORIZONTAL, SOLID, END, Toplevel, Label as Lbl, NORMAL, DISABLED
from tkinter.ttk import Frame, Button, Label, Style, Checkbutton, Combobox, Separator, Progressbar
from tkinter import filedialog as fd
import pandas as pd
from dataprocessor import DataProcessor
import datetime
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

'''
moving Toplevel ref:
- https://stackoverflow.com/questions/4055267/tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
'''
class Application(Frame):

    def __init__(self):
        super().__init__()
        self.is_all_data = IntVar()
        self.selected_month_1 = StringVar()
        self.selected_year_1 = StringVar()
        self.selected_month_2 = StringVar()
        self.selected_year_2 = StringVar()
        self.selected_saham = StringVar()
        self.finished = False
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
        self.splash = Toplevel(self.right_frame)
        self.splash.overrideredirect(True)
        self.splash.geometry('200x23+100+100')
        self.splash.overrideredirect(1)
        # self.splash.bind("<B1-Motion>", self.move_window)
        self.splash.attributes('-topmost', 'true')
        window_height = 23
        window_width = 400

        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.splash.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.splash.withdraw()
        pb = Progressbar(self.splash,
                orient=HORIZONTAL,
                length=400)
        pb.config(mode='indeterminate')
        pb.start(10)
        pb.grid(row=1, column=1, sticky=W+E+S+N)
        # self.splash.withdraw()
        self.dp = DataProcessor()
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
        self.btnFilter = Button(self.left_frame, text="Filter", command=self.callFilter)
        self.btnFilter.grid(row=4, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=5, columnspan=1, ipadx=75, padx=5, sticky=W)

        self.txSaham = Text(self.left_frame)

        self.cbSaham = Combobox(self.left_frame, textvariable=self.selected_saham)
        self.cbSaham['values'] = [] #self.kodeSaham
        self.cbSaham['state'] = 'readonly'  # normal
        self.cbSaham.set('-- Pilih Saham --')
        self.cbSaham.grid(row=7, column=0,padx=5, pady=5)

        # Buton Proses
        self.btnProses = Button(self.left_frame, text="proses", command=self.callProses)
        self.btnProses.grid(row=8, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=9, columnspan=1, ipadx=75, padx=5, sticky=W)


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
        self.splash.deiconify()
        msg = self.dp.load(name)
        self.splash.withdraw()
        messagebox.showinfo("Info", msg)

    # show and hide frame
    def cbCallback(self):
        if(self.is_all_data.get() == 1):
            self.rangeFrame.grid_forget()
        else:
            self.rangeFrame.grid()

    def disableButton(self, disable=True):
        if disable:
            self.btnFilter['state'] = DISABLED
            self.btnProses['state'] = DISABLED
        else:
            self.btnFilter['state'] = NORMAL
            self.btnProses['state'] = NORMAL

    '''
    filter data berdasarkan bulan dipilih
    '''
    def filter(self):
        self.disableButton()
        self.splash.deiconify()
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
        self.splash.withdraw()
        messagebox.showinfo("Info", "filter selesai")
        self.disableButton(False)

    def callFilter(self):
        threading.Thread(target=self.filter).start()

    '''
    sanding data dari 2 paket data: mentions counter dan price dari yfinance
    plot line graph
    '''
    def proses(self):

        if self.dp.dffilter is None:
            messagebox.showerror("Error", "Data kosong")
            return
        self.disableButton()
        self.splash.deiconify()
        stockcode = self.cbSaham.get()
        '''if(len(self.txSaham.get())>0):
            stockcode = self.txSaham.get()'''
        # menghitung frekuensi mentions saham di chat
        dfa = self.dp.getCount(stockcode)
        print('dfa ',dfa.shape)
        # mendapatkan stock price's series from yahoo finance
        self.company_name, stockprice, dfstock = self.dp.getPergerakanHargaSaham(stockcode)
        print('dfstock ', dfstock.shape)
        # sanding data
        self.dfnorm, dfbefnorm = self.dp.sandingData(dfa, stockprice)
        print('sandingData--- ')
        self.area.delete('1.0', END)
        self.area.insert(END, 'correlation {0}\n\n {1}'.format(self.dp.corr(self.dfnorm), dfbefnorm))
        # # plot
        # self.plot(self.right_frame, self.dfnorm, self.company_name)
        self.finished = True
        self.disableButton(False)
        self.splash.withdraw()


    def callProses(self):
        # kami memanfaatkan link ini untuk mengetahui bahwa thread sudah selesai
        # https://stackoverflow.com/a/56010976
        POLLING_DELAY = 250  # ms
        lock = threading.Lock()  # Lock for shared resources.
        def check_status():
            with lock:
                if not self.finished:
                    self.after(POLLING_DELAY, check_status)  # Keep polling.
                else:
                    self.plot(self.right_frame, self.dfnorm, self.company_name)
        with lock:
            self.finished = False
        t = threading.Thread(target=self.proses)
        t.daemon = True
        self.after(POLLING_DELAY, check_status)  # Start polling.
        t.start()

    def move_window(self, e):
        self.splash.geometry(f'+{e.x_root}+{e.y_root}')

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

def main():

    root = Tk()
    root.geometry("1450x550+300+300")
    app = Application()
    root.mainloop()


if __name__ == '__main__':
    main()
