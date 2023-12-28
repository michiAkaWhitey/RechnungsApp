import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
from tkinter.filedialog import askopenfile
from tkinter import messagebox
from billApplication.model.camera import getBill

import cv2
from ..view.autoCompleteEntry import AutocompleteEntry


class FormVariables:
    def __init__(self, master) -> None:
        self.date = tk.StringVar(master)
        self.price = tk.DoubleVar(master)
        self.company = tk.StringVar(master)
        self.tags = tk.StringVar(master)
        self.img = None
        self.imgFilename = None

        self.reset()

    def reset(self) -> None:
        '''sets all Tk variables to default'''
        self.date.set(date.today().strftime(r"%d.%m.%y"))
        self.price.set(0.0)
        self.company.set("")
        self.tags.set("")
        self.img = None
        self.imgFilename = None
        
    def asDict(self) -> dict:
        '''returns the tk variables as dataclass'''
        t = self.tags.get().split(",")
        if self.tags.get() == "": t = None
        return {"date": self.date.get(),
            "price": self.price.get(),
            "company": self.company.get(),
            "tags": t,
            "img": self.img}


class BillFrame(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(master=self.parent)

        self.columnconfigure((0, 1), weight=1)
        self.configure(highlightbackground="black", highlightthickness=1, padx=10, pady=10)

        self.data = FormVariables(master=parent)

        r = 0
        ttk.Label(master=self, text="Date", style="TFrame.TLabel").grid(row=r, column=0)
        DateEntry(self,selectmode='day',textvariable=self.data.date, locale="de", style="TFrame.TEntry").grid(row=r, column=1, sticky="w")

        r = 1
        ttk.Label(master=self, text="Price", style="TFrame.TLabel").grid(row=r, column=0)
        ttk.Entry(master=self, textvariable=self.data.price, style="TFrame.TEntry").grid(row=r, column=1)

        r = 2
        ttk.Label(master=self, text="Company", style="TFrame.TLabel").grid(row=r, column=0)
        eComp = AutocompleteEntry(master=self, textvariable=self.data.company, style="TFrame.TEntry")
        eComp.set_completion_list(["Hofer", "OBI", "Billa"])
        eComp.grid(row=r, column=1)

        r = 3
        ttk.Label(master=self, text="Tags", style="TFrame.TLabel").grid(row=r, column=0)
        eTag = AutocompleteEntry(master=self, textvariable=self.data.tags, style="TFrame.TEntry")
        eTag.set_completion_list(["Tanken", "Haushalt", "Etc"])
        eTag.grid(row=r, column=1)

        r = 4
        self.b = ttk.Button(master=self, text="Get Bill Photo", command=self.getImage, style="TFrame.TButton")
        self.b.grid(row=r, column=0, columnspan=2, padx=5, pady=5)

        self.update()

    def getImage(self):
        self.data.img = getBill()

    def update(self):
        if self.data.img is not None:
            s = str(self.data.imgFilename).split('/')[-1]
            self.b.config(text=s)
        else:
            self.b.config(text="Get Bill Photo")
        self.after(100, self.update)    
