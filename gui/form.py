import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from autoCompleteEntry import AutocompleteEntry
from dataclasses import dataclass
import numpy as np
from typing import List

@dataclass
class FormData:
    date: str
    price: float
    company: str
    tags: List[str]
    img: np.ndarray


class FormVariables:
    def __init__(self, master) -> None:
        self.date = tk.StringVar(master)
        self.price = tk.DoubleVar(master)
        self.company = tk.StringVar(master)
        self.tags = tk.StringVar(master)
        self.img = None

        self.reset()

    def reset(self) -> None:
        '''sets all Tk variables to default'''
        self.date.set("")
        self.price.set(0.0)
        self.company.set("")
        self.tags.set("")
        self.img = None

    def toDataClass(self) -> FormData:
        '''returns the tk variables as dataclass'''
        return FormData(
            date=self.date.get(),
            price=self.price.get(),
            company=self.company.get(),
            tags = self.tags.get().split(","),
            img = self.img)


class BillForm(tk.Frame):
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
        b = ttk.Button(master=self, text='Get Bill Photo', command=lambda: print('Camera stuff'), style="TFrame.TButton")
        b.grid(row=r, column=0, columnspan=2, padx=5, pady=5)

        
