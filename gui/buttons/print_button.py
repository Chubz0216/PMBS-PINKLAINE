import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import win32print
import win32ui


def print_barcode_window(parent, barcode_path, product_name, price):
    # New window para sa print settings (Parent window will be passed here)
    print_window = tk.Toplevel(parent)
    print_window.title("Print Barcode")
    print_window.geometry("400x400")

    # Show Barcode Image
    barcode_img = Image.open(barcode_path)
    barcode_img = barcode_img.resize((200, 100))
    img_tk = ImageTk.PhotoImage(barcode_img)

    barcode_label = ttk.Label(print_window, image=img_tk)
    barcode_label.image = img_tk  # Keep reference to prevent GC
    barcode_label.pack(pady=10)

    # Product Name and Price Labels
    product_name_label = ttk.Label(print_window, text=f"Product: {product_name}")
    product_name_label.pack()

    price_label = ttk.Label(print_window, text=f"Price: ₱{price}")
    price_label.pack()

    # Printer Selection
    printer_label = ttk.Label(print_window, text="Select Printer:")
    printer_label.pack(pady=10)

    printers = [printer for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)]
    printer_names = [printer[2] for printer in printers]  # Extract printer names
    printer_combobox = ttk.Combobox(print_window, values=printer_names)
    printer_combobox.set(printer_names[0])  # Default selection
    printer_combobox.pack()

    # Number of Copies Input
    copies_label = ttk.Label(print_window, text="Number of Copies:")
    copies_label.pack(pady=10)

    copies_entry = ttk.Entry(print_window)
    copies_entry.pack()
    copies_entry.insert(0, "1")  # Default number of copies

    # Print Button
    def print_barcode():
        copies = int(copies_entry.get())
        selected_printer = printer_combobox.get()

        # Call the print function
        for _ in range(copies):
            os.startfile(barcode_path, "print")
            print(f"Printing {copies} copies to {selected_printer}...")

        print_window.destroy()  # Close the print window after printing

    print_btn = ttk.Button(print_window, text="Print Barcode", command=print_barcode)
    print_btn.pack(pady=20)


def generate_barcode_display(parent, barcode_value, product_name, price):
    barcode_path = f"{barcode_value}.png"

    # Generate the barcode image (EAN-13)
    ean = barcode.get('ean13', barcode_value, writer=ImageWriter())
    ean.save(barcode_path)

    # Open the new print window (pass parent window as argument)
    print_barcode_window(parent, barcode_path, product_name, price)