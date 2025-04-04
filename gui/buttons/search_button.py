import sqlite3
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

# Function to search for products based on the keyword
def search_products(keyword):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Search query with LIKE for name, barcode, and price
    query = """
        SELECT id, name, barcode, price FROM products
        WHERE name LIKE ? OR barcode LIKE ? OR price LIKE ?
    """
    wildcard = f"%{keyword}%"
    cursor.execute(query, (wildcard, wildcard, wildcard))
    results = cursor.fetchall()

    conn.close()
    return results


# Step 1: Define the main window (root)
root = tk.Tk()

# Step 2: Define the widgets
search_entry = tk.Entry(root)  # This is the search input field
search_button = tk.Button(root, text="Search")  # This is the search button
validation_label = tk.Label(root, text="")  # This label will show validation messages
product_list_treeview = ttk.Treeview(root, columns=("ID", "Name", "Barcode", "Price"))

# Function to handle the search and update the Treeview
def perform_search(treeview, search_entry, validation_label):
    keyword = search_entry.get().strip()

    if not keyword:
        validation_label.config(text="Please enter a search keyword.", foreground="red")
        validation_label.after(2000, lambda: validation_label.config(text=""))
        return

    results = search_products(keyword)

    # Clear existing Treeview rows
    for row in treeview.get_children():
        treeview.delete(row)

    if results:
        # Insert search results sa Treeview
        for row in results:
            id, name, barcode, price = row
            treeview.insert('', 'end', values=(id, name, barcode, f"₱{float(price):.2f}"))

        validation_label.config(text=f"{len(results)} result(s) found.", foreground="green")
    else:
        validation_label.config(text="No results found.", foreground="orange")

    validation_label.after(2000, lambda: validation_label.config(text=""))

# Attach the search to the button
search_button.config(command=lambda: perform_search(product_list_treeview, search_entry, validation_label))

# Placing the widgets in the window
search_entry.pack()
search_button.pack()
validation_label.pack()
product_list_treeview.pack()

# Run the application
root.mainloop()