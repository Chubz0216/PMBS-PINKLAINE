import tkinter as tk
from tkinter import messagebox
from gui.buttons.add_button import add_product



def create_product_form():
    def submit():
        name = name_entry.get()
        price = price_entry.get()

        if name and price:
            try:
                price = float(price)
                add_product(name, price)
                messagebox.showinfo("Success", "Product added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid price.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    form = tk.Toplevel()
    form.title("Add Product")

    tk.Label(form, text="Product Name").grid(row=0, column=0)
    tk.Label(form, text="Price").grid(row=1, column=0)

    name_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1)

    price_entry = tk.Entry(form)
    price_entry.grid(row=1, column=1)

    submit_btn = tk.Button(form, text="Add", command=submit)
    submit_btn.grid(row=2, column=1)
