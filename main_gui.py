import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
import barcode
from barcode.writer import ImageWriter
import tkinter as tk
import gui.buttons.add_button as add_button
from gui.buttons.add_button import add_product_to_db
from tkinter import ttk, Tk
from database import get_all_products
from gui.buttons.clearlist_button import clear_list  # Import the clear_list function
from gui.buttons.view_button import view_product_list
from gui.buttons.update_button import update_product
from utils.utils import load_products_into_treeview
from database import search_products  # Assuming search_products is defined in database.py
from tkinter import PhotoImage
from barcode import get_barcode_class
import barcode
from barcode.writer import ImageWriter
from tkinter import PhotoImage, messagebox
import time





def get_selected_product_id(product_list):
    try:
        selected_item = product_list.selection()
        if selected_item:
            selected_product_id = product_list.item(selected_item[0], "values")[0]  # Assuming ID is the first column
            return selected_product_id
        else:
            print("No product selected.")
            return None
    except Exception as e:
        print(f"Error getting selected product ID: {e}")
        return None



def print_barcode():
    copies = int(print_copies_entry.get()) if print_copies_entry.get().isdigit() else 1
    os.startfile("barcode.png", "print")
    print(f"Printing {copies} copies of the barcode...")



validation_label = None




def on_product_select(event, product_list, product_name_entry, barcode_entry, price_entry):
    selected_item = product_list.selection()
    if selected_item:
        product_id = product_list.item(selected_item[0], "values")[0]  # Assuming ID is the first column
        product_name = product_list.item(selected_item[0], "values")[1]
        barcode = product_list.item(selected_item[0], "values")[2]
        price = product_list.item(selected_item[0], "values")[3]

        # Set the values to input fields
        product_name_entry.delete(0, tk.END)
        product_name_entry.insert(0, product_name)

        barcode_entry.delete(0, tk.END)
        barcode_entry.insert(0, barcode)

        price_entry.delete(0, tk.END)
        price_entry.insert(0, price)

        # Store the selected product ID (you can use this later for updating)
        product_name_entry.selected_product_id = product_id


# end function section

def format_price(event=None):
    raw = price_entry.get().replace("₱", "").replace(",", "").strip()
    try:
        value = float(raw)
        formatted = f"₱{value:,.2f}"
        price_entry.delete(0, tk.END)
        price_entry.insert(0, formatted)
    except ValueError:
        price_entry.delete(0, tk.END)


def perform_search(product_list, search_entry, validation_label):
    keyword = search_entry.get().strip()

    if not keyword:
        validation_label.config(text="Please enter a search keyword.", foreground="red")
        validation_label.after(2000, lambda: validation_label.config(text=""))
        return

    # Perform the search using the search_products function
    results = search_products(keyword)

    # Clear existing rows in the Treeview
    for row in product_list.get_children():
        product_list.delete(row)

    # If results are found, insert them into the Treeview
    if results:
        for row in results:
            id, name, barcode, price = row
            product_list.insert('', 'end', values=(id, name, barcode, f"₱{float(price):.2f}"))

        validation_label.config(text=f"{len(results)} result(s) found.", foreground="green")
    else:
        validation_label.config(text="No results found.", foreground="orange")

    validation_label.after(2000, lambda: validation_label.config(text=""))


def check_and_generate_barcode():
    # Get values from the form (e.g., from Entry widget)
    code = barcode_var.get().strip()  # assuming barcode_var is your Entry variable

    # Check if input is not empty
    if code:
        # Call barcode generation function
        barcode_path = generate_barcode_image(code)

        # Check if barcode image was generated and exists
        if os.path.exists(barcode_path):
            img = Image.open(barcode_path)
            img = img.resize((200, 100))  # Resize as needed
            photo = ImageTk.PhotoImage(img)

            # Update the label with the barcode image
            barcode_placeholder.config(image=photo, text="")
            barcode_placeholder.image = photo  # Keep a reference
        else:
            print(f"Error: Barcode image not found at {barcode_path}")
    else:
        print("Please enter a valid barcode code")




def run_app():
    global validation_label, barcode_entry, product_name_entry, price_entry

    root = Tk()
    root.title("PINKLAINE PRODUCT MANAGEMENT BARCODE SYSTEM")
    root.geometry("1000x800")
    root.configure(bg="#FDE2E4")

    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=BOTH, expand=True)

    # Configure two columns
    main_frame.columnconfigure(0, weight=2)  # Left (Product Details)
    main_frame.columnconfigure(1, weight=1)  # Right (Barcode)
    main_frame.rowconfigure(2, weight=1)

    # Product Form Frame (LEFT side)
    form_frame = ttk.LabelFrame(main_frame, text="Product Details", padding=10)
    form_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    product_name_entry = ttk.Entry(form_frame, width=40)
    product_name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Barcode:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    barcode_entry = ttk.Entry(form_frame, width=40)
    barcode_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    price_entry = ttk.Entry(form_frame, width=40)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    barcode_frame = ttk.LabelFrame(main_frame, text="Generated Barcode", padding=10)
    barcode_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)






    # Placeholder label for displaying barcode image
    barcode_placeholder = ttk.Label(barcode_frame, text="[ Barcode Image Here ]")
    barcode_placeholder.pack()

    status_label = ttk.Label(form_frame, text="", foreground="red", font=("Arial", 10))  # Define status_label
    status_label.grid(row=4, column=0, columnspan=3, pady=5)


    # Buttons (Below Product Details)
    button_frame = ttk.Frame(form_frame, padding=10)
    button_frame.grid(row=3, column=0, columnspan=3, pady=10)

    add_btn = ttk.Button(button_frame, text="✅ Add Product", bootstyle="success-outline",
                         command=lambda: add_product_to_db(product_name_entry, price_entry, barcode_entry, validation_label))
    add_btn.pack(side=LEFT, padx=5, fill=X, expand=True)




    # Delete Section
    from gui.buttons.delete_button import delete_product

    delete_btn = ttk.Button(button_frame, text="🗑️ Delete Product", bootstyle="danger-outline",
                            command=lambda: delete_product(product_list, get_selected_product_id(product_list),
                                                           status_label))
    delete_btn.pack(side=LEFT, padx=5, fill=X, expand=True)





    # Search Section

    search_frame = ttk.LabelFrame(main_frame, text="Search Product", padding=10)
    search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    search_entry = ttk.Entry(search_frame, width=50)
    search_entry.pack(side=LEFT, padx=5, pady=5)
    search_btn = ttk.Button(search_frame, text="🔍 Search", bootstyle="primary-outline")
    search_btn.pack(side=LEFT, padx=5)
    # Link the search button to the perform_search function
    search_btn.config(command=lambda: perform_search(product_list, search_entry, validation_label))

    # Validation message label
    validation_label = ttk.Label(form_frame, text="", foreground="red", font=("Arial", 10))
    validation_label.grid(row=4, column=0, columnspan=3, pady=5)

    # Product List Table (Treeview)
    table_frame = ttk.LabelFrame(main_frame, text="📦 Product List", padding=10)
    table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    # Create Treeview
    product_list = ttk.Treeview(table_frame, columns=("ID", "Name", "Barcode", "Price"), show="headings", height=10)

    # Column headings (Gawin silang center-aligned)
    product_list.heading("ID", text="ID", anchor="center")
    product_list.heading("Name", text="📌 Product Name", anchor="center")
    product_list.heading("Barcode", text="🔖 Barcode", anchor="center")
    product_list.heading("Price", text="💰 Price", anchor="center")



    # Column width settings (Pantay-pantay na spacing)
    product_list.column("ID", width=50, anchor="center")
    product_list.column("Name", width=300, anchor="center")
    product_list.column("Barcode", width=200, anchor="center")
    product_list.column("Price", width=100, anchor="center")

    # Style for better aesthetics
    style = ttk.Style()
    style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")  # Para may border effect
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#f0f0f0")  # Header styling
    product_list.config(show="headings", selectmode="browse")

    # Add alternating row colors (striped effect)
    product_list.tag_configure("evenrow", background="#f2f2f2")  # Light gray
    product_list.tag_configure("oddrow", background="white")

    product_list.pack(fill=BOTH, expand=True)

    # Load products into Treeview on startup
    product_list.delete(*product_list.get_children())  # Clear Treeview initially


    # Buttons (View List and Clear List)
    buttons_frame = ttk.Frame(table_frame)
    buttons_frame.pack(pady=5)

    view_btn = ttk.Button(buttons_frame, text="👀 View List", bootstyle="primary-outline", width=15,
        command=lambda: view_product_list(product_list))
    view_btn.pack(side=LEFT, padx=5)

    def clear_list():
        # Tanggalin ang lahat ng items sa Treeview
        product_list.delete(*product_list.get_children())
        print("DEBUG: Clearing list...")
        product_list.delete(*product_list.get_children())

    from gui.buttons.clearlist_button import clear_list  # Import the clear_list function

    clear_btn = ttk.Button(buttons_frame, text="🧹 Clear List", bootstyle="secondary-outline", width=15,
                           command=lambda: clear_list(product_list))
    clear_btn.pack(side=LEFT, padx=5)

    # Bind Treeview selection
    product_list.bind("<ButtonRelease-1>",
                      lambda event: on_product_select(event, product_list, product_name_entry, barcode_entry,
                                                      price_entry))
    # Update button
    update_btn = ttk.Button(button_frame, text="🔄 Update Product", bootstyle="warning-outline",
                            command=lambda: update_product(product_list, product_name_entry, price_entry, barcode_entry,
                                                           validation_label))
    update_btn.pack(side=LEFT, padx=5, fill=X, expand=True)

    # Print
    generate_button = ttk.Button(form_frame, text="Generate Barcode", command=check_and_generate_barcode)
    generate_button.grid(row=4, column=0, columnspan=2, pady=10)

    footer_frame = ttk.Frame(root, padding=5)
    footer_frame.pack(side="bottom", fill="x")

    footer_label = ttk.Label(
        footer_frame,
        text="© 2025  Created by: Chubby C. Llamado - All rights reserved",
        font=("Arial", 9),
        foreground="#888"
    )
    footer_label.pack(anchor="center")

    root.mainloop()


if __name__ == "__main__":
    run_app()

