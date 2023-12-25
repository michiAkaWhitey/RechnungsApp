import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from view.dataEntry.form import BillForm 

class App(tk.Tk):
    def __init__(self) -> None:
        '''Application GUI to same a bill to a db'''
        super().__init__()

        self.title('Bill GUI')
        self.resizable(0, 0)
        self.bind('<Escape>', lambda x: self.destroy())

        # UI options
        paddings = {'padx': 5, 'pady': 5}
        #entry_font = {'font': ('Helvetica', 11)}

        # Widgets
        self.label = ttk.Label(self, text='Bill Application')
        self.bill = BillForm(parent=self)
        self.commitButton = ttk.Button(self, text='Commit Form', command=self.commit)
        self.resetButton = ttk.Button(self, text='Reset Form', command=self.bill.data.reset)

        # Style
        self.style = ttk.Style(self)

        self.style.configure('TLabel', font=('Arial', 20))
        self.style.configure('TButton', font=('Helvetica', 14))
        
        self.style.configure('TFrame.TLabel', font=('Helvetica', 12))
        self.style.configure('TFrame.TButton', font=('Helvetica', 12))
        self.style.configure('TFrame.TEntry', font=('Helvetica', 12))

        # Layout        
        self.label.pack(**paddings)
        self.bill.pack(**paddings)
        self.commitButton.pack(fill='both')
        self.resetButton.pack(fill='both')

    def commit(self):
        '''checks data and pass them to the dB'''
        data = self.bill.data.asDict()
        print(data)

        # # validate input data
        # if data.isDefault():
        #     messagebox.showerror('Input Error', 'Error: You have to insert all necessary data!')
        #     return
        
        # access to database
        # to be done

        # Reset Form
        self.bill.data.reset()
