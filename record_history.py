import tkinter as tk
from tkinter import ttk
import mysql.connector
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="system"
)
mycursor = mydb.cursor()

def home():
    root1.destroy()
    os.system('python admin2.py')

def record_delivered_items(order_id, customer_name, items):
    for item in items:
        item_name = item['name']
        quantity = item['quantity']
        price = item['price']

        # Insert the delivered item into the order_records table
        mycursor.execute("INSERT INTO order_records (order_id, customer_name, item_name, quantity, price) "
                         "VALUES (%s, %s, %s, %s, %s)",
                         (order_id, customer_name, item_name, quantity, price))
    mydb.commit()

def get_customer_name(order_id):
    mycursor.execute("SELECT customer_name FROM orders WHERE order_id = %s", (order_id,))
    result = mycursor.fetchone()
    if result:
        return result[0]
    return ""

def search():
    search_value = search_entry.get()

    mycursor.execute("SELECT * FROM order_records WHERE order_id = %s", (search_value,))
    data = mycursor.fetchone()

    if data:
        list.delete(*list.get_children())
        list.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4], data[5]))
    else:
        list.delete(*list.get_children())

def refresh():
    mycursor.execute('SELECT * FROM order_records')
    myresult = mycursor.fetchall()

    if len(myresult) != 0:
        list.delete(*list.get_children())
        for data in myresult:
            list.insert("", tk.END, values=data)

    # Schedule the next refresh after 2 seconds
    root1.after(2000, refresh)

root1 = tk.Tk()
root1.geometry('990x600')
root1.title("RECORDS")
root1.resizable(False, False)
root1.config(bg="#CDCDAA")

view_frame = tk.Frame(root1, bg="white")
view_frame.place(x=40, y=50, width=900, height=500)

go_back = tk.Button(root1, text="Go back", bg="#CDCDAA", fg="black", bd=0, font=("garamond", 15), command=home)
go_back.place(x=840, y=560)

search_btn = tk.Button(text="Search", bg="white", fg="black", font=("garamond", 11), command=search)
search_btn.place(x=840, y=15, width=100)

search_entry = tk.Entry()
search_entry.place(x=40, y=15, width=780, height=25)

scrollbar = tk.Scrollbar(view_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

list = ttk.Treeview(view_frame, columns=("order_id", "customer_name", "item_name", "quantity", "price", "date_delivered"),
                    yscrollcommand=scrollbar.set)
list.heading("order_id", text="Order ID")
list.heading("customer_name", text="Customer Name")
list.heading("item_name", text="Item Name")
list.heading("quantity", text="Quantity")
list.heading("price", text="Price")
list.heading("date_delivered", text="Date delivered")
list.pack(fill=tk.BOTH, expand=1)

list['show'] = 'headings'
list.column("order_id", width=30)
list.column("customer_name", width=100)
list.column("item_name", width=100)
list.column("quantity", width=120)
list.column("price", width=90)
list.column("date_delivered", width=90)

scrollbar.config(command=list.yview)

refresh()

root1.mainloop()
