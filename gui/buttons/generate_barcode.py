import io
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageTk

# Function to generate barcode image in-memory (without saving to disk)
def generate_barcode_image_in_memory(code):
    # Create an in-memory bytes buffer to store the image
    buffer = io.BytesIO()

    # Create the barcode image using Code128
    barcode_class = Code128
    barcode_instance = barcode_class(code, writer=ImageWriter())

    # Save the barcode image directly into the buffer instead of a file
    barcode_instance.write(buffer)
    buffer.seek(0)  # Move the pointer to the beginning of the buffer

    # Open the image from the buffer
    img = Image.open(buffer)
    return img

# Function to display barcode on the label in the GUI
def display_barcode(barcode_code, barcode_placeholder):
    img = generate_barcode_image_in_memory(barcode_code)

    # Resize the image to fit the label size
    img = img.resize((200, 100))  # Adjust size as needed

    # Convert the image to a Tkinter-compatible format
    photo = ImageTk.PhotoImage(img)

    # Update the label to show the barcode image
    barcode_placeholder.config(image=photo, text="")

    # Keep a reference to the photo to prevent garbage collection
    barcode_placeholder.image = photo
