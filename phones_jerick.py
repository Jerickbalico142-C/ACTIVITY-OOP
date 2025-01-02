import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


def init_db():
    conn = sqlite3.connect("phones.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phone_specs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            price REAL NOT NULL,
            os TEXT NOT NULL,
            ram TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_phone():
    brand = brand_entry.get()
    model = model_entry.get()
    price = price_entry.get()
    os = os_entry.get()
    ram = ram_entry.get()

    if not (brand and model and price and os and ram):
        messagebox.showerror("Error", "All fields must be filled")
        return

    try:
        conn = sqlite3.connect("phones.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO phone_specs (brand, model, price, os, ram) VALUES (?, ?, ?, ?, ?)",
                       (brand, model, float(price), os, ram))
        conn.commit()
        conn.close()
        clear_entries()
        load_data()
        messagebox.showinfo("Success", "Phone added successfully")
    except ValueError:
        messagebox.showerror("Error", "Invalid price value")


def update_phone():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "No phone selected")
        return

    values = tree.item(selected, "values")
    phone_id = values[0]
    
    brand = brand_entry.get()
    model = model_entry.get()
    price = price_entry.get()
    os = os_entry.get()
    ram = ram_entry.get()

    if not (brand and model and price and os and ram):
        messagebox.showerror("Error", "All fields must be filled")
        return

    try:
        conn = sqlite3.connect("phones.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE phone_specs 
            SET brand = ?, model = ?, price = ?, os = ?, ram = ?
            WHERE id = ?
        """, (brand, model, float(price), os, ram, phone_id))
        conn.commit()
        conn.close()
        clear_entries()
        load_data()
        messagebox.showinfo("Success", "Phone updated successfully")
    except ValueError:
        messagebox.showerror("Error", "Invalid price value")


def delete_phone():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "No phone selected")
        return

    values = tree.item(selected, "values")
    phone_id = values[0]

    conn = sqlite3.connect("phones.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM phone_specs WHERE id = ?", (phone_id,))
    conn.commit()
    conn.close()
    clear_entries()
    load_data()
    messagebox.showinfo("Success", "Phone deleted successfully")


def clear_entries():
    brand_entry.delete(0, tk.END)
    model_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    os_entry.delete(0, tk.END)
    ram_entry.delete(0, tk.END)


def load_data():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("phones.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phone_specs")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)


def on_tree_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        clear_entries()
        brand_entry.insert(0, values[1])
        model_entry.insert(0, values[2])
        price_entry.insert(0, values[3])
        os_entry.insert(0, values[4])
        ram_entry.insert(0, values[5])


root = tk.Tk()
root.title("Phone Specifications CRUD")
root.configure(bg="#eb984e") 


fields_frame = ttk.Frame(root)
fields_frame.pack(pady=10, padx=10)

labels = ["Brand", "Model", "Price", "OS", "RAM"]
entries = []
for i, label in enumerate(labels):
    lbl = ttk.Label(fields_frame, text=label)
    lbl.grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
    entry = ttk.Entry(fields_frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)

brand_entry, model_entry, price_entry, os_entry, ram_entry = entries


buttons_frame = ttk.Frame(root)
buttons_frame.pack(pady=10)

add_btn = ttk.Button(buttons_frame, text="Add Phone", command=add_phone)
add_btn.grid(row=0, column=0, padx=5)

update_btn = ttk.Button(buttons_frame, text="Update Phone", command=update_phone)
update_btn.grid(row=0, column=1, padx=5)

delete_btn = ttk.Button(buttons_frame, text="Delete Phone", command=delete_phone)
delete_btn.grid(row=0, column=2, padx=5)

clear_btn = ttk.Button(buttons_frame, text="Clear Fields", command=clear_entries)
clear_btn.grid(row=0, column=3, padx=5)


columns = ("ID", "Brand", "Model", "Price", "OS", "RAM")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=50)

tree.bind("<ButtonRelease-1>", on_tree_select)
tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)


init_db()
load_data()

root.mainloop()
