from tkinter import Tk, Text, BOTH, W, N, E, S, StringVar
from tkinter.ttk import Frame, Button, Label, Style, Checkbutton, Combobox
from tkinter import filedialog as fd
import pandas as pd


class Application(Frame):

    def __init__(self):
        super().__init__()

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
        abtn.grid(row=1, column=0)
        self.left_frame = Frame(self, width=200, height=400)
        self.left_frame.grid(row=2, column=0)
        chkBox = Checkbutton(self.left_frame, text = "All data")
        chkBox.grid(row=1, column=0)
        self.rangeFrame = Frame(self.left_frame)
        self.rangeFrame.grid(row=2, column=0, columnspan=2)
        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

        selected_month = StringVar()

        month_cb_1 = Combobox(self.rangeFrame, textvariable=selected_month)
        month_cb_1['values'] = months
        month_cb_1['state'] = 'readonly'  # normal
        month_cb_1.grid(row=1, column=0,padx=5, pady=5)
        month_cb_2 = Combobox(self.rangeFrame, textvariable=selected_month)
        month_cb_2['values'] = months
        month_cb_2['state'] = 'readonly'  # normal
        month_cb_2.grid( row=3, column=0,padx=5, pady=5)

        # month_cb.bind('<<ComboboxSelected>>', month_changed)

        # cbtn = Button(self.left_frame, text="Close")
        # cbtn.grid(row=2, column=0, pady=4)

        hbtn = Button(self, text="Help")
        hbtn.grid(row=5, column=0, padx=5)

        obtn = Button(self, text="OK")
        obtn.grid(row=5, column=3)

    def openFile(self):
        name = fd.askopenfilename()
        self.lbl['text'] = self.lbl['text']+' '+name



def main():

    root = Tk()
    root.geometry("650x300+300+300")
    app = Application()
    root.mainloop()


if __name__ == '__main__':
    main()
