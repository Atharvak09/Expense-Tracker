from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox
import matplotlib.pyplot as plt

# Object for database
data = Database(db='myexpense.db')

# Global variables
count = 0
selected_rowid = 0

def saveRecord():
    global data
    data.insert_record(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get(), category=category.get())
    refreshData()

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')
    category.set('')

def fetch_records():
    f = data.fetch_records('SELECT rowid, * FROM expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3], rec[4]))
        count += 1

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
        category.set(val[4])
    except Exception as ep:
        pass

def update_record():
    global selected_rowid

    selected = tv.focus()
    try:
        data.update_record(namevar.get(), amtvar.get(), dopvar.get(), category.get(), selected_rowid)
        tv.item(selected, text='', values=(namevar.get(), amtvar.get(), dopvar.get(), category.get()))
        refreshData()
    except Exception as ep:
        messagebox.showerror('Error', ep)

    clearEntries()

def totalbalance():
    f = data.fetch_records("SELECT SUM(item_price) FROM expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

def deleteRow():
    global selected_rowid
    data.remove_record(selected_rowid)
    refreshData()

def show_summary():
    summary_win = Toplevel(ws)
    summary_win.title("Spending Summary")
    summary_win.geometry("800x800")

    categories = data.fetch_records("SELECT DISTINCT category FROM expense_record")
    for category in categories:
        category_name = category[0]
        total_spent = data.fetch_records(f"SELECT SUM(item_price) FROM expense_record WHERE category = '{category_name}'")[0][0]
        Label(summary_win, text=f"{category_name}: {total_spent}", font=('Times New Roman', 14)).pack()

def plot_spending_summary():
    categories = data.fetch_records("SELECT DISTINCT category FROM expense_record")
    category_names = [cat[0] for cat in categories]
    spending = [data.fetch_records(f"SELECT SUM(item_price) FROM expense_record WHERE category = '{cat[0]}'")[0][0] for cat in categories]

    fig, ax = plt.subplots()
    ax.pie(spending, labels=category_names, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Spending Summary by Category')
    plt.show()

    fig, ax = plt.subplots()
    ax.bar(category_names, spending)
    ax.set_xlabel('Categories')
    ax.set_ylabel('Total Spending')
    ax.set_title('Spending Summary by Category')
    plt.xticks(rotation=45)
    plt.show()

ws = Tk()
ws.title("Daily Expenses")

f = ('Times New Roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()
category = StringVar()

# Frame widget
f2 = Frame(ws)
f2.pack()

f1 = Frame(ws, padx=10, pady=10)
f1.pack(expand=True, fill=BOTH)

# Label widgets
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)
Label(f1, text='CATEGORY', font=f).grid(row=3, column=0, sticky=W)

# Entry widgets
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)
category_entry = Entry(f1, font=f, textvariable=category)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10,0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10,0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10,0))
category_entry.grid(row=3, column=1, sticky=EW, padx=(10,0))

# Action buttons
cur_date = Button(f1, text='Current Date', font=f, bg='#04C4D9', command=setDate, width=15)
submit_btn = Button(f1, text='Save Record', font=f, command=saveRecord, bg='#42602D', fg='white')
clr_btn = Button(f1, text='Clear Entry', font=f, command=clearEntries, bg='#09B036', fg='white')
quit_btn = Button(f1, text='Exit', font=f, command=lambda: ws.destroy(), bg='#D33532', fg='white')
total_bal = Button(f1, text='Total Balance', font=f, command=totalbalance, bg='#486966', fg='white')
update_btn = Button(f1, text='Update', bg='#c28800', command=update_record, font=f)
del_btn = Button(f1, text='Delete', bg='#BD2A2E', command=deleteRow, font=f)
summary_btn = Button(f1, text='View Summary', font=f, command=show_summary, bg='#4287f5', fg='white')
chart_btn = Button(f1, text='Plot Summary Chart', font=f, command=plot_spending_summary, bg='#FF8C00', fg='white')

# Grid placement
cur_date.grid(row=4, column=1, sticky=EW, padx=(10,0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10,0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10,0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10,0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10,0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10,0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10,0))
summary_btn.grid(row=3, column=3, sticky=EW, padx=(10,0))
chart_btn.grid(row=4, column=3, sticky=EW, padx=(10,0))

# Treeview
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4, 5), show='headings', height=8)
tv.pack(side='left')

# Add heading to treeview
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.column(5, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")
tv.heading(5, text="Category")

# Binding treeview
tv.bind("<ButtonRelease-1>", select_record)

# Style for treeview
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

# Vertical scrollbar
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.configure(yscrollcommand=scrollbar.set)

# Calling function
fetch_records()

# Infinite loop
ws.mainloop()
