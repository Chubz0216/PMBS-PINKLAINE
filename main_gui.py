
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
import barcode
from barcode.writer import ImageWriter
import tkinter as tk
from gui.buttons.add_button import add_product
from gui.buttons.add_button import add_product_to_db



def print_barcode():
    copies = int(print_copies_entry.get()) if print_copies_entry.get().isdigit() else 1
    os.startfile("barcode.png", "print")
    print(f"Printing {copies} copies of the barcode...")


def generate_barcode_display():
    barcode_value = barcode_entry.get().strip()
    product_name = product_name_entry.get()
    price = price_entry.get()

    # Check if barcode is exactly 12 digits
    if barcode_value.isdigit() and len(barcode_value) == 12:
        try:
            # Generate barcode (EAN-13 automatically adds checksum)
            ean = barcode.get('ean13', barcode_value, writer=ImageWriter())
            barcode_path = "barcode.png"
            ean.save(barcode_path)

            # Load the generated barcode image
            if os.path.exists(barcode_path):
                barcode_img = Image.open(barcode_path)
                barcode_img = barcode_img.resize((200, 100))
                img_tk = ImageTk.PhotoImage(barcode_img)
                barcode_label.config(image=img_tk)
                barcode_label.image = img_tk
                product_name_label.config(text=f"{product_name}")
                price_label.config(text=f"₱{price}")
            else:
                print("Barcode file not found!")

        except Exception as e:
            print(f"Error generating barcode: {e}")
            barcode_label.config(image='')
            product_name_label.config(text="Barcode Error")
            price_label.config(text="")
    else:
        print("Invalid barcode! Must be 12 digits.")
        barcode_label.config(image='')
        product_name_label.config(text="Invalid Barcode")
        price_label.config(text="")


def run_app():
    global barcode_entry, product_name_entry, price_entry, barcode_label, product_name_label, price_label

    root = ttk.Window(themename="journal")  # Light pink theme for soft aesthetics
    root.title("PINKLAINE PRODUCT MANAGEMENT SYSTEM")
    root.geometry("1000x600")
    root.configure(bg="#FDE2E4")  # Soft pastel pink background

    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=BOTH, expand=True)

    # Product Form Frame
    form_frame = ttk.LabelFrame(main_frame, text="Product Details", padding=10)
    form_frame.pack(fill=X, padx=10, pady=10)

    ttk.Label(form_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    product_name_entry = ttk.Entry(form_frame, width=40)
    product_name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Barcode:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    barcode_entry = ttk.Entry(form_frame, width=40)
    barcode_entry.grid(row=1, column=1, padx=5, pady=5)
    barcode_entry.bind("<KeyRelease>", lambda e: generate_barcode_display())

    ttk.Label(form_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    price_entry = ttk.Entry(form_frame, width=40)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    # Barcode Display Area
    barcode_display_frame = ttk.Frame(form_frame, padding=10)
    barcode_display_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=5)

    barcode_label = ttk.Label(barcode_display_frame)
    barcode_label.pack()

    product_name_label = ttk.Label(barcode_display_frame, text="", font=("Arial", 10, "bold"))
    product_name_label.pack()

    price_label = ttk.Label(barcode_display_frame, text="", font=("Arial", 10))
    price_label.pack()

    # Buttons (Below Product Details)
    button_frame = ttk.Frame(form_frame, padding=10)
    button_frame.grid(row=3, column=0, columnspan=3, pady=10)

    add_btn = ttk.Button(button_frame, text="✅ Add Product", bootstyle="success-outline",
                         command=lambda: add_product_to_db(product_name_entry, price_entry, barcode_entry))
    add_btn.pack(side=LEFT, padx=5, fill=X, expand=True)

    update_btn = ttk.Button(button_frame, text="🔄 Update Product", bootstyle="warning-outline")
    update_btn.pack(side=LEFT, padx=5, fill=X, expand=True)

    delete_btn = ttk.Button(button_frame, text="🗑️ Delete Product", bootstyle="danger-outline")
    delete_btn.pack(side=LEFT, padx=5, fill=X, expand=True)

    print_btn = ttk.Button(button_frame, text="🖨️ Print Barcode", bootstyle="success-outline", command=print_barcode)
    print_btn.pack(side=LEFT, padx=5, fill=X, expand=True)

    # Search Section
    search_frame = ttk.LabelFrame(main_frame, text="Search Product", padding=10)
    search_frame.pack(fill=X, padx=10, pady=5)

    search_entry = ttk.Entry(search_frame, width=50)
    search_entry.pack(side=LEFT, padx=5, pady=5)
    search_btn = ttk.Button(search_frame, text="🔍 Search", bootstyle="primary-outline")
    search_btn.pack(side=LEFT, padx=5)

    # Product List Table
    table_frame = ttk.LabelFrame(main_frame, text="Product List", padding=10)
    table_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    product_list = ttk.Treeview(table_frame, columns=("ID", "Name", "Barcode", "Price"), show="headings")
    product_list.heading("ID", text="ID")
    product_list.heading("Name", text="Product Name")
    product_list.heading("Barcode", text="Barcode")
    product_list.heading("Price", text="Price")
    product_list.pack(fill=BOTH, expand=True)

    # Clear List Button
    clear_btn = ttk.Button(table_frame, text="🧹 Clear List", bootstyle="secondary-outline",
                           command=lambda: product_list.delete(*product_list.get_children()))
    clear_btn.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    run_app()
