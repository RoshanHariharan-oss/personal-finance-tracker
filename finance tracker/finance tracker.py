import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime
import os
import getpass

# Constants
username = getpass.getuser()
DATA_FILE = f"data/transactions_{username}.csv"

if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount']).to_csv(DATA_FILE, index=False)

def add_transaction():
    date, t_type, category, amount_str = date_entry.get(), type_var.get(), category_entry.get(), amount_entry.get()

    try:
        datetime.strptime(date, "%Y-%m-%d")
        amount = float(amount_str)
    except ValueError:
        messagebox.showerror("Error", "Invalid Date (YYYY-MM-DD) or Amount.")
        return

    # Append to CSV efficiently
    new_data = pd.DataFrame([[date, t_type, category, amount]])
    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
    
    clear_fields()
    refresh_table()

def refresh_table():
    # Clear existing rows in Treeview
    for item in tree.get_children():
        tree.delete(item)
    
    # Load and populate
    df = pd.read_csv(DATA_FILE)
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    
    # Update Summary
    income = df[df['Type'] == 'Income']['Amount'].sum()
    expense = df[df['Type'] == 'Expense']['Amount'].sum()
    summary_label.config(text=f"Income: ${income:.2f} | Expense: ${expense:.2f} | Balance: ${(income-expense):.2f}")

def clear_fields():
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

# GUI setup
root = tk.Tk()
root.title(f"Finance Tracker - {username}")
root.geometry("600x500")

# Input Frame
input_frame = tk.Frame(root, pady=10)
input_frame.pack()

tk.Label(input_frame, text="Date:").grid(row=0, column=0)
date_entry = tk.Entry(input_frame)
date_entry.grid(row=0, column=1)
date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

tk.Label(input_frame, text="Type:").grid(row=0, column=2)
type_var = tk.StringVar(value="Expense")
tk.OptionMenu(input_frame, type_var, "Expense", "Income").grid(row=0, column=3)

tk.Label(input_frame, text="Category:").grid(row=1, column=0)
category_entry = tk.Entry(input_frame)
category_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Amount:").grid(row=1, column=2)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=1, column=3)

tk.Button(root, text="Add Transaction", command=add_transaction, bg="lightblue").pack(pady=5)

# Summary Label
summary_label = tk.Label(root, text="Income: $0 | Expense: $0 | Balance: $0", font=("Arial", 10, "bold"))
summary_label.pack(pady=5)

# Treeview Table
tree_frame = tk.Frame(root)
tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

tree = ttk.Treeview(tree_frame, columns=("Date", "Type", "Category", "Amount"), show='headings')
for col in ("Date", "Type", "Category", "Amount"):
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(side="left", fill="both", expand=True)

# Add Scrollbar
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

refresh_table() # Initial load
root.mainloop()