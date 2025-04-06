import barcode
from barcode.writer import ImageWriter

def generate_barcode_image(barcode_input):
    barcode_path = f"E:\\PMBS-PINKLAINE\\barcodes\\{barcode_input}.png"  # Set your path
    try:
        # Create barcode object
        barcode_obj = barcode.get_barcode_class('ean13')
        barcode_instance = barcode_obj(barcode_input, writer=ImageWriter())

        # Save barcode image
        barcode_instance.save(barcode_path)
        print(f"Barcode image saved at: {barcode_path}")
        return barcode_path
    except Exception as e:
        print(f"Error generating barcode image: {e}")
        return None
