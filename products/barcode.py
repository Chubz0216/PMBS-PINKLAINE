# products/barcode.py

from barcode import Code128
from barcode.writer import ImageWriter
import os
import barcode
from barcode.writer import ImageWriter

def generate_barcode_image(barcode_value):
    # Example of generating barcode and saving it to a specific path
    barcode_path = f"./generated_barcodes/{barcode_value}.png"
    # Logic to generate barcode image...
    # After generating, return the path
    return barcode_path

    # Gumawa ng folder kung wala pa
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # File name na walang extension
    filename = os.path.join(output_folder, barcode_text)

    # Generate barcode as PNG image
    barcode = Code128(barcode_text, writer=ImageWriter())
    barcode.save(filename)  # Ito ang magse-save ng PNG

    # Return file path (with .png)
    return f"{filename}.png"


# products/barcode.py


def generate_barcode(barcode_value, barcode_file):
    # Create a barcode object (for example, a standard 'EAN13' barcode)
    ean = barcode.get_barcode_class('ean13')  # You can change this type if needed
    barcode_instance = ean(barcode_value, writer=ImageWriter())

    # Save the barcode as a PNG file
    barcode_instance.save(barcode_file)
