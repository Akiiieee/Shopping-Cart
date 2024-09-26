import tkinter as tk
from tkcalendar import DateEntry
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="system"
)
mycursor = mydb.cursor()

total_sales_label = None

def back():
    report_window.destroy()
    os.system('python admin2.py')

def generate_sales_report_graph(start_date, end_date):
    global total_sales_label

    query = "SELECT DATE(date_delivered), SUM(quantity * price) FROM order_records " \
            f"WHERE DATE(date_delivered) BETWEEN '{start_date}' AND '{end_date}' " \
            "GROUP BY DATE(date_delivered)"

    mycursor.execute(query)
    results = mycursor.fetchall()

    dates = []
    total_sales = []

    for row in results:
        dates.append(row[0].strftime('%Y-%m-%d'))  # Convert to string format
        total_sales.append(row[1])

    # Generate the graph
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, total_sales, marker='o', linestyle='-', color='blue')
    ax.set_title('Sales Report', fontsize=14, fontweight='bold', color='black')
    ax.set_xlabel('Date', fontsize=12, color='black')
    ax.set_ylabel('Total Sales', fontsize=12, color='black')
    ax.tick_params(axis='x', rotation=45, colors='black')

    # Set the background color of the graph
    ax.set_facecolor('#F0F0F0')

    # Clear the existing graph frame
    for widget in sales_graph_frame.winfo_children():
        widget.destroy()

    # Create a new graph canvas
    canvas = FigureCanvasTkAgg(fig, master=sales_graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Display total sales
    if total_sales_label:
        total_sales_label.config(text=f'Total Sales: ₱{sum(total_sales)}', fg='black')
    else:
        total_sales_label = tk.Label(sales_report_frame, text=f'Total Sales: ₱{sum(total_sales)}', font=("garamond", 15), bg="white", fg='black')
        total_sales_label.pack()

    # Adjust the position of the total sales label
    total_sales_label.pack(side="bottom", pady=10)

report_window = tk.Tk()
report_window.geometry("800x600")
report_window.title("Sales Report")
report_window.config(bg="#E8E8E8")

sales_report_frame = tk.Frame(report_window, bg="white")
sales_report_frame.pack(fill="both")

sales_graph_frame = tk.Frame(report_window, bg="#FFFFFF")
sales_graph_frame.pack(fill="both", expand=True)

start_date_entry = DateEntry(sales_report_frame,width=12, background='darkblue', font=("garamond", 11),foreground='white', borderwidth=2)
start_date_entry.pack(side="left", padx=5, pady=5)

end_date_entry = DateEntry(sales_report_frame, width=12, background='darkblue', font=("garamond", 11),foreground='white', borderwidth=2)
end_date_entry.pack(side="left", padx=5, pady=5)

exit_button = tk.Button(report_window, text="Go back", font=("garamond", 12),command=back)
exit_button.place(x=715,y=10,width=80)

def generate_sales_report():
    generate_sales_report_graph(start_date_entry.get_date(), end_date_entry.get_date())

generate_report_button = tk.Button(sales_report_frame, text="Filter", font=("garamond", 12),command=generate_sales_report)
generate_report_button.pack(side="left", padx=5, pady=5)

generate_sales_report_graph(start_date_entry.get_date(), end_date_entry.get_date())

report_window.mainloop()
