from tkinter import Tk, Text, BOTH, W, N, E, S, StringVar, IntVar, HORIZONTAL
from tkinter.ttk import Frame, Button, Label, Style, Checkbutton, Combobox, Separator
from tkinter import filedialog as fd
import pandas as pd


class Application(Frame):

    def __init__(self):
        super().__init__()
        self.is_all_data = IntVar()
        self.selected_month_1 = StringVar()
        self.selected_year_1 = StringVar()
        self.selected_month_2 = StringVar()
        self.selected_year_2 = StringVar()
        self.selected_saham = StringVar()
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

        area = Text(self)
        area.grid(row=1, column=2, columnspan=3, rowspan=4,
            padx=5, sticky=E+W+S+N)
        # upload
        # lblUpload = Label(self, text="upload")
        # lblUpload.grid(row=1, column=0, columnspan=2)
        abtn = Button(self, text="Upload", command=self.openFile)
        abtn.grid(row=1, column=0, sticky=W, padx=5)
        self.left_frame = Frame(self, width=200, height=400, borderwidth = 1)
        self.left_frame.grid(row=2, column=0)
        self.chkBox = Checkbutton(self.left_frame, text = "All data", variable=self.is_all_data, command=self.cbCallback)
        self.chkBox.grid(row=1, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=2, columnspan=1, ipadx=75, padx=5, sticky=W)
        self.rangeFrame = self.rangeFrame() #Frame(self.left_frame, borderwidth = 1)
        self.rangeFrame.grid(row=3, column=0, columnspan=2)
        btnFilter = Button(self.left_frame, text="Filter", command=self.filter)
        btnFilter.grid(row=4, column=0, sticky=W, padx=5)
        Separator(self.left_frame,orient=HORIZONTAL).grid(row=5, columnspan=1, ipadx=75, padx=5, sticky=W)
        cbSaham = Combobox(self.left_frame, textvariable=self.selected_saham)
        cbSaham['values'] = []
        cbSaham['state'] = 'readonly'  # normal
        cbSaham.set('-- Pilih Saham --')
        cbSaham.grid(row=6, column=0,padx=5, pady=5)
        btnProses = Button(self.left_frame, text="proses", command=self.proses)
        btnProses.grid(row=7, column=0, sticky=W, padx=5)

        # month_cb.bind('<<ComboboxSelected>>', month_changed)

        # cbtn = Button(self.left_frame, text="Close")
        # cbtn.grid(row=2, column=0, pady=4)

        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

    def rangeFrame(self):
        frame = Frame(self.left_frame, borderwidth = 1)
        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
        years = (2018, 2019, 2020, 2021)

        lblFrom = Label(frame, text='Dari')
        lblFrom.grid(row=1, column=0, sticky=W, padx=5)
        month_cb_1 = Combobox(frame, textvariable=self.selected_month_1)
        month_cb_1['values'] = months
        month_cb_1['state'] = 'readonly'  # normal
        month_cb_1.set('-- Pilih bulan --')
        month_cb_1.grid(row=2, column=0,padx=5, pady=5)
        year_cb_1 = Combobox(frame, textvariable=self.selected_year_1)
        year_cb_1['values'] = years
        year_cb_1['state'] = 'readonly'  # normal
        year_cb_1.set('-- Pilih tahun --')
        year_cb_1.grid(row=3, column=0,padx=5, pady=5)
        lblTo = Label(frame, text='Ke')
        lblTo.grid(row=4, column=0, sticky=W, padx=5)
        month_cb_2 = Combobox(frame, textvariable=self.selected_month_2)
        month_cb_2['values'] = months
        month_cb_2['state'] = 'readonly'  # normal
        month_cb_2.set('-- Pilih bulan --')
        month_cb_2.grid( row=5, column=0,padx=5, pady=5)
        year_cb_2 = Combobox(frame, textvariable=self.selected_year_2)
        year_cb_2['values'] = years
        year_cb_2['state'] = 'readonly'  # normal
        year_cb_2.set('-- Pilih tahun --')
        year_cb_2.grid(row=6, column=0,padx=5, pady=5)
        return frame

    def openFile(self):
        name = fd.askopenfilename()
        self.lbl['text'] = self.lbl['text']+' '+name
        print(self.is_all_data.get())

    def cbCallback(self):
        if(self.is_all_data.get() == 1):
            self.rangeFrame.grid_forget()
        else:
            self.rangeFrame.grid()
    def filter(self):
        if(self.is_all_data.get()==1):
            print('pilihan semua')
    def proses(self):
        print('ini dari proses')



def main():

    root = Tk()
    root.geometry("650x450+300+300")
    app = Application()
    root.mainloop()


if __name__ == '__main__':
    main()
