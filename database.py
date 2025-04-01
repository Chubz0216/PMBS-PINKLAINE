import sqlite3

def add_product(name, price, barcode):
    try:
        # Open a connection to the database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        print(f"Attempting to insert: Name={name}, Price={price}, Barcode={barcode}")  # Debugging line

        # Insert the product into the database
        cursor.execute("INSERT INTO products (name, price, barcode) VALUES (?, ?, ?)", (name, price, barcode))

        # Commit the changes
        conn.commit()

        print("Product successfully added!")  # Debugging line

        # Close the connection
        conn.close()
    except sqlite3.Error as e:
        print(f"Error adding product: {e}")
