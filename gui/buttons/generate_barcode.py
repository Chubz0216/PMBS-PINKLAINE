import io
from barcode import EAN13
from barcode.writer import ImageWriter
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
from tkinter import messagebox
import os
import win32api
import win32print
from tkinter import PhotoImage

# Generate EAN-13 barcode image in-memory with a white background
# Generate EAN-13 barcode image in-memory with a white background (includes barcode, price, and product name)
def generate_barcode_image_in_memory(code, price, product_name):
    buffer = io.BytesIO()

    # Create custom writer settings for size adjustments
    writer = ImageWriter()
    writer.set_options({
        'module_width': 0.2,  # Adjust module width for more length
        'module_height': 20.0,  # Adjust height for better visibility
        'quiet_zone': 10.0,  # Space around the barcode for readability
        'guard_bars': True  # Keep guard bars as part of the barcode
    })

    # Create EAN13 barcode instance
    barcode_class = EAN13
    barcode_instance = barcode_class(code, writer=writer)

    # Save barcode image into memory
    barcode_instance.write(buffer)
    buffer.seek(0)
    barcode_img = Image.open(buffer).convert("RGB")

    # Get barcode image dimensions
    width, height = barcode_img.size
    new_height = height + 180  # Adjusted space for price and product name

    # Create the final image with a pure white background
    final_img = Image.new("RGB", (width, new_height), "white")  # Pure white background
    final_img.paste(barcode_img, (0, 0))

    # Calculate font size for price and product name to match the barcode number width
    draw = ImageDraw.Draw(final_img)
    font = ImageFont.load_default()

    # Calculate the width of the barcode digits
    barcode_digits_width = width - 25  # Subtracting space for margin
    text_width = barcode_digits_width / len(code)  # Scaling based on number of digits

    try:
        # Use bold font for price and product name
        font_price = ImageFont.truetype("arialbd.ttf", 35)  # Arial Bold for price
        font_name = ImageFont.truetype("arialbd.ttf", 30)  # Arial Bold for product name (smaller size)
    except IOError:
        font_price = ImageFont.load_default()
        font_name = ImageFont.load_default()

    # Adjust vertical positioning to bring text even closer to the barcode
    draw.text((70, height + -35), f"{price}", font=font_price, fill="black")  # Moved up closer to barcode

    # Increase the space between price and product name
    draw.text((70, height + 10), product_name.upper(), font=font_name, fill="black")  # Increased space

    return final_img

# Function to print the barcode image with barcode, price, and product name

def print_barcode_image(barcode_img):
    # Save the image to a temporary file for printing
    temp_filename = "temp_barcode_image.png"
    barcode_img.save(temp_filename)

    # Print the image using the default printer
    printer_name = win32print.GetDefaultPrinter()
    win32api.ShellExecute(0, "print", temp_filename, f'/d:"{printer_name}"', ".", 0)

    # Optionally delete the temp file after printing
    os.remove(temp_filename)

# Display barcode image in the GUI label
def display_barcode(code, price, product_name, barcode_placeholder):
    # Validation: Check if the fields are empty
    if not code or not price or not product_name:
        messagebox.showerror("Validation Error", "All fields (Barcode, Price, Product Name) must be filled.")
        return

    # Generate the barcode image
    img = generate_barcode_image_in_memory(code, price, product_name)
    img = img.resize((300, 180))  # Resize for label display (adjust size)

    # Create a frame to contain the barcode image and the print button
    barcode_frame = tk.Frame(barcode_placeholder)

    # Display the barcode in the frame
    photo = ImageTk.PhotoImage(img)
    barcode_label = tk.Label(barcode_frame, image=photo, text="")
    barcode_label.photo = photo  # Store reference to avoid garbage collection
    barcode_label.pack()

    # Load the printer icon image (make sure the icon file is in the same directory as the script)
    try:
        print_icon = PhotoImage(file="printer_icon.png")  # Load the icon file
    except tk.TclError:
        print_icon = None  # In case the icon is not found, fallback to no icon

    # Add the Print button below the barcode image, with the icon
    print_button = tk.Button(barcode_frame, text="Print Barcode", image=print_icon, compound="left",
                             command=lambda: print_barcode_image(img))
    print_button.image = print_icon  # Store the image reference
    print_button.pack(pady=10)  # Padding for some space between image and button

    # Pack the frame inside the placeholder
    barcode_frame.pack(pady=10)

# Function to print the barcode image
def print_barcode_image(barcode_img):
    # Save the image to a temporary file for printing
    temp_filename = "temp_barcode_image.png"
    barcode_img.save(temp_filename)

    # Print the image using the default printer
    printer_name = win32print.GetDefaultPrinter()
    win32api.ShellExecute(0, "print", temp_filename, f'/d:"{printer_name}"', ".", 0)

    # Optionally delete the temp file after printing
    os.remove(temp_filename)

# Display barcode image in the GUI label
def display_barcode(code, price, product_name, barcode_placeholder):
    # Validation: Check if the fields are empty
    if not code or not price or not product_name:
        messagebox.showerror("Validation Error", "All fields (Barcode, Price, Product Name) must be filled.")
        return

    # Generate the barcode image
    img = generate_barcode_image_in_memory(code, price, product_name)
    img = img.resize((300, 180))  # Resize for label display (adjust size)

    # Create a frame to contain the barcode image and the print button
    barcode_frame = tk.Frame(barcode_placeholder)

    # Display the barcode in the frame
    photo = ImageTk.PhotoImage(img)
    barcode_label = tk.Label(barcode_frame, image=photo, text="")
    barcode_label.photo = photo  # Store reference to avoid garbage collection
    barcode_label.pack()

    # Load the printer icon image (make sure the icon file is in the same directory as the script)
    try:
        print_icon = PhotoImage(file="printer_icon.png")  # Load the icon file
    except tk.TclError:
        print_icon = None  # In case the icon is not found, fallback to no icon

    # Add the Print button below the barcode image, with the icon
    print_button = tk.Button(barcode_frame, text="Print Barcode", image=print_icon, compound="left",
                             command=lambda: print_barcode_image(img))
    print_button.image = print_icon  # Store the image reference
    print_button.pack(pady=10)  # Padding for some space between image and button

    # Pack the frame inside the placeholder
    barcode_frame.pack(pady=10)