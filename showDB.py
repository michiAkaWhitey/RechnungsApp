from tkinter import *
from tkinter import ttk
from billApplication.model.dbHandler import DatabaseHandler


handler = DatabaseHandler()
handler.connectToDb(dbName=r"app/bills.db")

columnNames = handler.getColumnNames()
columnNames = [x.upper() for x in columnNames]



# Create an instance of tkinter frame
win = Tk()

# Set the size of the tkinter window
win.geometry("700x350")

# Create an object of Style widget
style = ttk.Style()
style.theme_use('clam')

# Add a Treeview widget
tree = ttk.Treeview(win, column=columnNames, show='headings', height=20)

for i,c in enumerate(columnNames):
    tree.column(f"# {i+1}", anchor=CENTER)
    tree.heading(f"# {i+1}", text=c)

data = handler.returnMetaData()
print(data)
# # Insert the data in Treeview widget
for d in data:
    tree.insert('', 'end', text="1", values=d)


tree.pack()

win.mainloop()