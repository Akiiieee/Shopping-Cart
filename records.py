from tkinter import *
from tkinter import ttk
import mysql.connector
import os
import datetime
from tkinter import messagebox

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

def deliver():
    selected_items = list.selection()
    if len(selected_items) == 0:
        messagebox.showinfo("Info", "Please select an order.")
        return

    order_id = list.item(selected_items[0], "values")[0]
    customer_name = list.item(selected_items[0], "values")[1]
    items = get_ordered_items(order_id)
    if not items:
        messagebox.showerror("Error", "Failed to retrieve ordered items.")
        return

    total = calculate_total(items)
    show_receipt(order_id, customer_name, items, total)
    delete_order(order_id)
    record_delivered_items(order_id, customer_name, items)
    refresh()

def get_ordered_items(order_id):
    mycursor.execute("SELECT item_name, quantity, price FROM orders WHERE order_id = %s", (order_id,))
    result = mycursor.fetchall()
    items = [{'name': item[0], 'quantity': item[1], 'price': item[2]} for item in result]
    return items

def calculate_total(items):
    total = 0
    for item in items:
        quantity = item['quantity']
        price = item['price']
        item_total = quantity * price
        total += item_total
    return total

def show_receipt(order_id, customer_name, items, total):
    receipt_content = f"Order Receipt\n\n"
    receipt_content += f"Date: {datetime.datetime.now()}\n\n"
    receipt_content += f"Customer Name: {customer_name}\n\n"
    receipt_content += f"Items:\n"
    for item in items:
        item_name = item['name']
        quantity = item['quantity']
        price = item['price']
        item_total = quantity * price
        receipt_content += f"{item_name} (x{quantity}): ₱{item_total}\n"
    receipt_content += f"\nTotal: ₱{total}\n"
    receipt_content += f"Order ID: {order_id}"

    messagebox.showinfo("Receipt", receipt_content)

def delete_order(order_id):
    mycursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))
    mydb.commit()

def record_delivered_items(order_id, customer_name, items):
    for item in items:
        item_name = item['name']
        quantity = item['quantity']
        price = item['price']
        delivered_date = datetime.datetime.now()

        # Insert the delivered item into the order_record table
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

    mycursor.execute("SELECT * FROM orders WHERE order_id = %s", (search_value,))
    data = mycursor.fetchone()

    if data:
        list.delete(*list.get_children())
        list.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4], data[5]))
    else:
        list.delete(*list.get_children())

def refresh():
    mycursor.execute('SELECT * FROM orders')
    myresult = mycursor.fetchall()

    if len(myresult) != 0:
        list.delete(*list.get_children())
        for data in myresult:
            list.insert("", END, values=data)

    # Schedule the next refresh after 2 seconds
    root1.after(2000, refresh)

root1 = Tk()
root1.geometry('1200x600')
root1.title("PENDING ORDERS")
root1.resizable(False, False)
root1.config(bg="#CDCDAA")

view_frame = Frame(root1, bg="white")
view_frame.place(x=250, y=50, width=900, height=500)

deliver_btn = Button(root1, text="Deliver", bg="#CDCDAA", fg="black", font=("garamond", 11), command=deliver)
deliver_btn.place(x=30, y=50, width=200, height=55)

go_back = Button(text="Go back", bg="#CDCDAA", fg="black", bd=0, font=("garamond", 13), command=home)
go_back.place(x=95, y=150)

search_btn = Button(text="Search", bg="white", fg="black", font=("garamond", 11), command=search)
search_btn.place(x=1050, y=15, width=100)

search_entry = Entry()
search_entry.place(x=250, y=15, width=790, height=25)

scrollbar = Scrollbar(view_frame)
scrollbar.pack(side=RIGHT, fill=Y)

list = ttk.Treeview(view_frame, columns=("order_id", "customer_name", "item_name", "quantity", "price", "order_date"),
                    yscrollcommand=scrollbar.set)
list.heading("order_id", text="Order ID")
list.heading("customer_name", text="Customer Name")
list.heading("item_name", text="Item Name")
list.heading("quantity", text="Quantity")
list.heading("price", text="Price")
list.heading("order_date", text="Order Date")
list.pack(fill=BOTH, expand=1)

list['show'] = 'headings'
list.column("order_id", width=30)
list.column("customer_name", width=100)
list.column("item_name", width=100)
list.column("quantity", width=120)
list.column("price", width=90)
list.column("order_date", width=90)

scrollbar.config(command=list.yview)

refresh()

root1.mainloop()
