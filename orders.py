from tkinter import *
from tkinter import filedialog
import mysql.connector
from tkinter import messagebox
from tkinter.ttk import Treeview
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="system"
)
mycursor = mydb.cursor()

def back():
    window.destroy()
    os.system('python admin2.py')

def add_category():
    category_name = category_entry.get()
    if category_name:
        table_name = category_name.replace(" ", "_").lower() + "_table"
        sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (product_name VARCHAR(255), price INT, stock INT, img VARCHAR(255))"
        mycursor.execute(sql_create_table)

        sql = "INSERT INTO categories (category_name, table_name) VALUES (%s, %s)"
        val = (category_name, table_name)
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Success", "Category added successfully!")
        category_entry.delete(0, END)
        load_categories()
    else:
        messagebox.showerror("Error", "Please enter a category name.")

def delete_category():
    selected_item = category_tree.focus()
    if selected_item:
        category_name = category_tree.item(selected_item)['values'][0]
        table_name = category_tree.item(selected_item)['values'][1]

        sql_delete_category = "DELETE FROM categories WHERE table_name = %s"
        val = (table_name,)
        mycursor.execute(sql_delete_category, val)
        mydb.commit()

        sql_drop_table = f"DROP TABLE IF EXISTS {table_name}"
        mycursor.execute(sql_drop_table)

        messagebox.showinfo("Success", f"Category '{category_name}' deleted successfully!")
        load_categories()
    else:
        messagebox.showerror("Error", "Please select a category to delete.")

def add_product():
    selected_category = category_tree.item(category_tree.focus())['values'][0]
    product_name = product_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()
    img = img_entry.get()
    if selected_category and product_name and price and stock:

        table_name = selected_category.replace(" ", "_").lower() + "_table"
        sql_insert_product = f"INSERT INTO {table_name} (product_name, price, stock, img) VALUES (%s, %s, %s, %s)"
        val = (product_name, price, stock, img)
        mycursor.execute(sql_insert_product, val)
        mydb.commit()

        messagebox.showinfo("Success", "Product added successfully!")
        product_entry.delete(0, END)  # Clear the entry fields
        price_entry.delete(0, END)
        stock_entry.delete(0, END)
    else:
        messagebox.showerror("Error", "Please select a category, enter a product name, specify a price, and enter the stock quantity.")

def restock_product():
    selected_category = category_tree.item(category_tree.focus())['values'][0]
    table_name = selected_category.replace(" ", "_").lower() + "_table"
    selected_product = products_tree.item(products_tree.focus())['values'][0]
    stock = restock_entry.get()

    if selected_category and selected_product and stock:
        table_name = selected_category.replace(" ", "_").lower() + "_table"
        sql_restock_product = f"UPDATE {table_name} SET stock = stock + %s WHERE product_name = %s"
        val = (stock, selected_product)
        mycursor.execute(sql_restock_product, val)
        mydb.commit()

        messagebox.showinfo("Success", "Product restocked successfully!")
        restock_entry.delete(0, END)  # Clear the entry field
        view_products()
    else:
        messagebox.showerror("Error", "Please select a product and enter a restock quantity.")

def delete_product():
    selected_category = category_tree.item(category_tree.focus())['values'][0]
    table_name = selected_category.replace(" ", "_").lower() + "_table"
    selected_item = products_tree.focus()
    if selected_item:
        selected_product = products_tree.item(selected_item)['values'][0]

        sql_delete_product = f"DELETE FROM {table_name} WHERE product_name = %s"
        val = (selected_product,)
        mycursor.execute(sql_delete_product, val)
        mydb.commit()

        messagebox.showinfo("Success", "Product deleted successfully!")
        view_products()
    else:
        messagebox.showerror("Error", "Please select a product to delete.")

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    img_entry.delete(0, END)
    img_entry.insert(END, file_path)

def load_categories():
    category_tree.delete(*category_tree.get_children())

    mycursor.execute("SELECT category_name, table_name FROM categories")
    categories = mycursor.fetchall()
    for category in categories:
        category_tree.insert("", "end", values=(category[0], category[1]))

def view_products():
    selected_category = category_tree.item(category_tree.focus())['values'][0]
    table_name = selected_category.replace(" ", "_").lower() + "_table"

    products_window = Toplevel(window)
    products_window.geometry('500x450')
    products_window.title(f"Products in {selected_category}")

    global products_tree
    products_tree = Treeview(products_window, columns=("product_name", "price", "stock"), show="headings")
    products_tree.heading("product_name", text="Product Name")
    products_tree.heading("price", text="Price")
    products_tree.heading("stock", text="Stock")
    products_tree.pack(fill=BOTH, expand=True)

    mycursor.execute(f"SELECT product_name, price, stock FROM {table_name}")
    products = mycursor.fetchall()

    for product in products:
        products_tree.insert("", "end", values=(product[0], product[1], product[2]))

    restock_lbl = Label(products_window, text='Restock Quantity:', font=("garamond", 14))
    restock_lbl.pack()
    global restock_entry
    restock_entry = Entry(products_window, font=("garamond", 14), width=10)
    restock_entry.pack()
    restock_btn = Button(products_window, text='Restock', font=("garamond", 14), command=restock_product)
    restock_btn.pack()

    delete_btn = Button(products_window, text='Delete Product', font=("garamond", 14), command=delete_product)
    delete_btn.pack()

window = Tk()
window.geometry('1200x700')
window.title('Categories & Products')
window.resizable(False, False)
window.config(bg='#A9A9A9')

order_lbl = Label(window, text='Adding Categories, Products and Restocking', font=("garamond", 17), bg='#FFFFB9')
order_lbl.place(x=0, y=5, width='1200', height=40)

back_lbl = Button(window,text="Go back", bg="#A9A9A9", fg="black", bd=0, font=("garamond", 15), command=back)
back_lbl.place(x=120,y=60)

frm = Frame(window, bg='#FFFF8C')
frm.place(x=120, y=90, width=950, height=550)

category_lbl = Label(frm, text='Category Name:', font=("garamond", 14), bg='#FFFF8C')
category_lbl.place(x=170, y=50)

category_entry = Entry(frm, font=("garamond", 14), width=20)
category_entry.place(x=300, y=50)

category_btn = Button(frm, text='Add Category', font=("garamond", 14), command=add_category)
category_btn.place(x=500, y=50,height=30)

category_tree = Treeview(frm, columns=("category_name", "table_name"), show="headings")
category_tree.heading("category_name", text="Category Name")
category_tree.heading("table_name", text="Table Name")
category_tree.place(x=170, y=100, width=600, height=225)

delete_btn = Button(frm, text='Delete Category', font=("garamond", 14), command=delete_category)
delete_btn.place(x=630, y=50,height=30)

product_lbl = Label(frm, text='Product Name:', font=("garamond", 14), bg='#FFFF8C')
product_lbl.place(x=170, y=350)

product_entry = Entry(frm, font=("garamond", 14), width=20)
product_entry.place(x=300, y=350)

img_bbtn = Label(frm, text='Image path:', font=("garamond", 14), bg='#FFFF8C')
img_bbtn.place(x=170, y=400)

img_entry = Entry(frm, font=("garamond", 14), width=20)
img_entry.place(x=300, y=400)

browse_btn = Button(frm, text='Browse', font=("garamond", 14), command=browse_image)
browse_btn.place(x=300, y=440,height=30,width=180)

price_lbl = Label(frm, text='Price:', font=("garamond", 14), bg='#FFFF8C')
price_lbl.place(x=500, y=350)

price_entry = Entry(frm, font=("garamond", 14), width=15)
price_entry.place(x=630, y=350)

stock_lbl = Label(frm, text='Stock Quantity:', font=("garamond", 14), bg='#FFFF8C')
stock_lbl.place(x=500, y=400)

stock_entry = Entry(frm, font=("garamond", 14), width=15)
stock_entry.place(x=630, y=400)

product_btn = Button(frm, text='Add Product', font=("garamond", 15), command=add_product)
product_btn.place(x=500, y=440,height=30)

view_btn = Button(frm, text='View Products', font=("garamond", 15), command=view_products)
view_btn.place(x=640, y=440,height=30)

load_categories()

window.mainloop()
