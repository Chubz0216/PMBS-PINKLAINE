import sqlite3
import re  # Regular expression module

# Function to validate the barcode
def is_valid_barcode(barcode):
    # Barcode must be exactly digits only — walang space, letra, etc.
    return bool(re.fullmatch(r'\d+', barcode))

def connect_db():
    return sqlite3.connect('products.db')  # Path to your SQLite database file

def add_product_to_db(name_entry, price_entry, barcode_entry, validation_label):
    barcode = barcode_entry.get()  # NO .strip()
    name = name_entry.get().strip()
    price = price_entry.get().strip()

    if not name or not price or not barcode:
        validation_label.config(text="Please fill out all fields.", foreground="red")
        validation_label.after(2000, lambda: validation_label.config(text=""))
        return

    # Reject barcodes with anything other than digits (no space, no letters)
    if not is_valid_barcode(barcode):
        validation_label.config(text="Invalid barcode! Only numbers allowed. No spaces.", foreground="red")
        validation_label.after(2000, lambda: validation_label.config(text=""))
        return

    # Convert price to float
    raw_price = price.replace("₱", "").replace(",", "").strip()
    try:
        price = float(raw_price)
    except ValueError:
        validation_label.config(text="Invalid price. Please enter a number.")
        validation_label.after(2000, lambda: validation_label.config(text=""))
        return

    try:
        # Insert product into the database
        add_product(name, price, barcode)
        validation_label.config(text="Product added successfully!", foreground="green")
        validation_label.after(2000, lambda: validation_label.config(text=""))
    except sqlite3.Error as e:
        validation_label.config(text=f"Error: {e}", foreground="red")
        validation_label.after(2000, lambda: validation_label.config(text=""))

def add_product(name, price, barcode):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Reset the AUTOINCREMENT sequence if needed
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='products'")

        # Create the table if it doesn't exist (with AUTOINCREMENT on id)
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            barcode TEXT NOT NULL
        )''')

        # Insert the new product into the database
        cursor.execute('''INSERT INTO products (name, price, barcode)
            VALUES (?, ?, ?)''', (name, price, barcode))

        # Commit the changes
        conn.commit()
        conn.close()

        print("✅ Product added successfully!")

    except sqlite3.Error as e:
        print(f"Error: {e}")
        raise e

def check_all_products():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        for product in products:
            print(product)

        conn.close()

    except sqlite3.Error as e:
        print(f"Error: {e}")

# Call the function to check the inserted products
check_all_products()
