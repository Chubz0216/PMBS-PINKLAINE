from database import add_product
import tkinter as tk
from tkinter import messagebox

def add_product_to_db(entry_name, entry_price, entry_barcode, error_label):
    # Get values from the entry fields
    name = entry_name.get().strip()
    price = entry_price.get().strip()
    barcode = entry_barcode.get().strip()

    if not name or not price or not barcode:
        error_label.config(text="⚠️ Please fill out all fields!", foreground="red")
        return

    try:
        price = float(price)
        add_product(name, price, barcode)  # Call to database function
        error_label.config(text="✅ Product added successfully!", foreground="green")

        # Clear the entry fields
        entry_name.delete(0, tk.END)
        entry_price.delete(0, tk.END)
        entry_barcode.delete(0, tk.END)
    except ValueError:
        error_label.config(text="⚠️ Invalid price! Enter a number.", foreground="red")

