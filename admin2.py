from tkinter import *
import os

def logout():
    admin_menu.destroy()
    os.system('python admin.py')

def record_history():
    admin_menu.destroy()
    os.system('python record_history.py')

def category():
    admin_menu.destroy()
    os.system('python orders.py')

def orders():
    admin_menu.destroy()
    os.system('python records.py')

def report():
    admin_menu.destroy()
    os.system('python report.py')

admin_menu = Tk()
admin_menu.title('Admin')
admin_menu.geometry('700x400')
admin_menu.config(bg='#CDCDAA')

lbl = Label(text='Admin',bg='#CDCDAA', fg='#FFFFB9', font=('Cooper black', 35))
lbl.place(x=280,y=10)

category_bttn = Button(text='Categories & Products',bd=0,bg='#CDCDAA', fg='#000000', font=("garamond", 20),command=category)
category_bttn.place(x=240,y=120)

orders = Button(text='Pending Orders',bd=0,bg='#CDCDAA', fg='#000000', font=("garamond", 20),command=orders)
orders.place(x=270,y=180)

order_history = Button(text='Order history',bd=0,bg='#CDCDAA', fg='#000000', font=("garamond", 20),command=record_history)
order_history.place(x=280,y=240)

sales_report = Button(text='Sales report',bd=0,bg='#CDCDAA', fg='#000000', font=("garamond", 20),command=report)
sales_report.place(x=290,y=295)

logout = Button(text='Logout',bd=0,bg='#CDCDAA', fg='#000000', font=("garamond", 15),command=logout)
logout.place(x=620,y=360)

admin_menu.mainloop()