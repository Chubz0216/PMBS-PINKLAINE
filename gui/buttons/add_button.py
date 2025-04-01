from database import add_product
import tkinter as tk
from tkinter import messagebox

def add_product_to_db(entry_name, entry_price, entry_barcode):
    name = entry_name.get()
    price = entry_price.get()
    barcode = entry_barcode.get()

    if name and price and barcode:
        try:
            price = float(price)  # Convert price to float
            add_product(name, price, barcode)  # Call to add_product function to save in DB
            messagebox.showinfo("Success", "Product added successfully!")
            # Clear the entry fields after successful addition
            entry_name.delete(0, tk.END)
            entry_price.delete(0, tk.END)
            entry_barcode.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price.")
    else:
        messagebox.showerror("Error", "Please fill out all fields.")
