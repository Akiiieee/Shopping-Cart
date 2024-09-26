from tkinter import *
import mysql.connector
import os
from tkinter import messagebox, simpledialog
import random
from PIL import Image, ImageTk

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="system"
)
mycursor = mydb.cursor()

quantity_entry = None
restore_items = []

def exit_program():
    menu.withdraw()
    os.system('python main.py')

def open_category(category):
    menu.withdraw()
    display_products(category)

def restore_stock(table_name, product_name, quantity):
    mycursor.execute(f"UPDATE {table_name} SET stock = stock + {quantity} WHERE product_name = '{product_name}'")
    mydb.commit()

def remove_from_cart():
    selection = cart_listbox.curselection()
    if selection:
        index = selection[0]
        removed_item = selected_items[index]
        product_name = removed_item[0]
        price = removed_item[1]
        quantity = removed_item[2]
        category = removed_item[3] if len(removed_item) > 3 else None

        if category:
            # Restore the stock in the table
            table_name = category.lower()
            restore_stock(table_name, product_name, quantity)

        del selected_items[index]
        update_cart()

def deduct_stock(table_name, product_name, quantity):
    mycursor.execute(f"UPDATE {table_name} SET stock = stock - {quantity} WHERE product_name = '{product_name}'")
    mydb.commit()

def calculate_total_cost():
    total_cost = 0
    for item in selected_items:
        price = item[1]
        quantity = item[2]
        total_cost += price * quantity
    total_cost_label.configure(text=f'Total Cost: ₱{total_cost}')

def update_cart():
    cart_listbox.delete(0, END)

    for item in selected_items:
        product_name, price, quantity, category = item
        cart_listbox.insert(END, f"{product_name} - ₱{price} - Quantity: {quantity}")

    calculate_total_cost()

def place_order():
    global customer_name_entry

    customer_name = customer_name_entry.get().strip()
    if not customer_name and not selected_items:
        messagebox.showwarning("Empty Fields", "Please enter the customer name and add items to the cart before placing an order.")
        return

    if not customer_name:
        messagebox.showwarning("Missing Customer Name", "Please enter the customer name.")
        return

    if not selected_items:
        messagebox.showwarning("Empty Cart", "Please add items to the cart before placing an order.")
        return

    order_id = random.randint(1000, 9999)

    for item in selected_items:
        product_name = item[0]
        price = item[1]
        quantity = item[2]

        mycursor.execute("INSERT INTO orders (order_id, customer_name, item_name, quantity, price) VALUES (%s, %s, %s, %s, %s)",
                         (order_id, customer_name, product_name, quantity, price))

    mydb.commit()

    messagebox.showinfo("Order Placed", "The order has been placed successfully.")

    cart_listbox.delete(0, END)
    selected_items.clear()
    customer_name_entry.delete(0, END)
    total_cost_label.configure(text='Total Cost: ₱0')


def add_to_cart(product_name, price, category, quantity):
    # Check if the item is already in the cart
    for item in selected_items:
        if item[0] == product_name and item[3] == category:
            # Update the quantity
            item_quantity = item[2]
            item_quantity += quantity
            item_index = selected_items.index(item)
            selected_items[item_index] = (product_name, price, item_quantity, category)
            break
    else:
        # Item not found in the cart, add it as a new entry
        selected_items.append((product_name, price, quantity, category))

    deduct_stock(category, product_name, quantity)
    update_cart()

def confirm_quantity(product_name, price, category):
    category = category.lower() + "_table"
    mycursor.execute(f"SELECT stock FROM {category} WHERE product_name = '{product_name}'")
    stock = mycursor.fetchone()[0]

    if stock == 0:
        messagebox.showinfo("Out of Stock", "This item is currently out of stock.")
        return

    quantity = simpledialog.askinteger("Quantity", f"Enter the quantity for {product_name}:", minvalue=1,
                                       maxvalue=stock)
    if quantity is not None:
        add_to_cart(product_name, price, category, quantity)


def display_products(category):
    category_window = Toplevel(menu)
    category_window.title('Products - {}'.format(category))
    category_window.geometry('800x600')
    category_window.config(bg='#CDCDB5')

    def close_category_window():
        category_window.destroy()
        menu.deiconify()

    category_window.protocol("WM_DELETE_WINDOW", close_category_window)

    products_frame = Frame(category_window, bg='#F5F5F5')
    products_frame.place(x=10, y=10, width=780, height=500)

    close_bttn = Button(category_window, text='Close', bd=3, bg='#CDCDB5', font=('georgia', 13),
                        command=close_category_window)
    close_bttn.pack(side=BOTTOM, pady=10)

    # Fetch products for the given category from the database
    mycursor.execute(f"SELECT product_name, price, stock, img FROM {category.lower()}_table")
    products = mycursor.fetchall()

    # Display the products as image buttons
    row = 0
    column = 0
    image_buttons = []  # Store image buttons to prevent garbage collection

    for product in products:
        product_name = product[0]
        price = product[1]
        stocks = product[2]
        image_path = product[3]

        # Load and resize the product image
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        # Create the image button
        button = Button(products_frame, image=photo, text=f"{product_name}\n₱{price}\nStocks: {stocks}",
                        compound='top', bd=0, bg='#F5F5F5', font=('georgia', 11),
                        command=lambda name=product_name, pr=price, cat=category: confirm_quantity(name, pr, cat))
        button.image = photo

        # Position the image button
        button.grid(row=row, column=column, padx=10, pady=10)

        image_buttons.append(button)  # Store the image button

        # Update row and column indices
        column += 1
        if column >= 4:
            row += 1
            column = 0
    category_window.mainloop()

def load_categories():
    mycursor.execute("SELECT category_name FROM categories")
    categories = mycursor.fetchall()

    num_columns = 4
    for i, category in enumerate(categories):
        row = i // num_columns
        column = i % num_columns

        btn = Button(menu_frame, text=category[0], bg='#FFFFFF', bd=2, fg="black", font=("garamond", 15),
                     command=lambda cat=category[0]: open_category(cat))
        btn.grid(row=row, column=column, padx=30, pady=5, sticky="nsew")

    exit_button = Button(menu, text="Exit", bg='#CDCDB7', bd=2, fg="black", font=("garamond", 15), command=exit_program)
    exit_button.place(x=1090, y=600, width=100, height=30)

menu = Tk()
menu.title('Offline Purchase Order Management System')
menu.geometry('1200x640')
menu.config(bg='#EEEED5')
menu.resizable(False, False)

lbl = Label(menu, text="Categories", bg='#EEEED5', fg='#83838B', font=('Cooper black', 35))
lbl.place(x=230, y=20)

cart_lbl = Label(menu, text="Cart", bg='#EEEED5', fg='#83838B', font=('Cooper black', 35))
cart_lbl.place(x=870, y=20)

menu_frame = Frame(bg='#D2D2B4')
menu_frame.place(x=50, y=90, width=600, height=500)

cart_frame = Frame(menu, bg='#D2D2B4')
cart_frame.place(x=700, y=90, width=400, height=500)

selected_items = []

cart_listbox = Listbox(cart_frame, width=60, height=20)
cart_listbox.pack(pady=10)

load_categories()

place_order_button = Button(cart_frame, text="Place Order", bg='#CDCDB7', bd=2, fg="black", font=("garamond", 15),
                           command=place_order)
place_order_button.place(x=0, y=460, width=190, height=40)

remove_button= Button(cart_frame, text="Remove", bg='#CDCDB7', bd=2, fg="black", font=("garamond", 15),
                           command=remove_from_cart)
remove_button.place(x=210, y=460, width=190, height=40)

total_cost_label = Label(cart_frame, text='Total Cost: ₱0', bg='#D2D2B4', font=('georgia', 15))
total_cost_label.pack(pady=10)

customer_name = Label(cart_frame, text='Customer Name:', bg='#D2D2B4', font=('georgia', 13))
customer_name.place(x=5, y=420)

customer_name_entry = Entry(cart_frame, font=('georgia', 13))
customer_name_entry.place(x=140, y=420, width=240, height=25)

menu.mainloop()
