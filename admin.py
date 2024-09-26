from tkinter import *
import mysql.connector
from tkinter import messagebox
import os

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='system'
)
def exit():
    admin_window.destroy()

def back():
    admin_window.destroy()
    os.system('python main.py')

def admin_login():
    admin_user = adminuser_entry.get()
    admin_pass = adminpass_entry.get()

    mycursor = mydb.cursor()
    sql = 'SELECT * FROM admin WHERE username=%s AND password=%s'
    vals = (admin_user, admin_pass)
    mycursor.execute(sql, vals)

    result = mycursor.fetchone()

    if result:
        admin_window.destroy()
        os.system('python admin2.py')
    else:
        messagebox.showerror("Error", "Username or password incorrect!!")


admin_window = Tk()
admin_window.config(bg="#CDCDAA")
admin_window.title("Admin Panel")
admin_window.geometry("900x550")
admin_window.resizable(False,False)

admin_frame = Frame(admin_window, bg="khaki4", width=450, height=300)
admin_frame.place(x=240, y=120)

admin_label = Label(admin_frame, text="Admin Login", fg='khaki1', bg='khaki4', font=("impact", 30, 'bold'))
admin_label.place(x=110, y=15)

admin_userlabel = Label(admin_frame, text="User name:",fg='white', font=("garamond", 15), bg="khaki4")
admin_userlabel.place(x=35, y=85)

adminuser_entry = Entry(admin_frame, bd=2)
adminuser_entry.place(x=130, y=85, width=200, height=30)

admin_passlabel = Label(admin_frame, text="Password:",fg='white', font=("garamond", 15), bg="khaki4")
admin_passlabel.place(x=35, y=140)

adminpass_entry = Entry(admin_frame, bd=2,show='*')
adminpass_entry.place(x=130, y=140, width=200, height=30)

admin_button = Button(admin_frame, text="login", bg="#CDCDAA", fg="black", font=("garamond", 15),bd=2, command=admin_login)
admin_button.place(x=130, y=190, width=200, height=45)

home = Button(admin_frame, text="Back to home", bg="#CDCDAA", fg="black", font=("garamond", 15),bd=2, command=back)
home.place(x=130, y=240, width=200, height=45)

home = Button(admin_window, text="Exit",bg="#CDCDAA", fg="black", font=("garamond", 15),bd=0, command=exit)
home.place(x=785, y=500, width=100, height=45)

admin_window.mainloop()