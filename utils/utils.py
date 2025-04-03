# utils.py
import sqlite3


def load_products_into_treeview(product_list):
    # Get all products from the database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        # Clear the existing items in the Treeview
        product_list.delete(*product_list.get_children())

        # Add each product to the Treeview
        for product in products:
            try:
                # Ensure that price is a float and barcode is a string
                price = float(product[2])  # Price should be the 3rd element
                barcode = str(product[3])  # Barcode should be the 4th element
            except ValueError:
                price = 0.00  # Default value kung may error sa conversion
                barcode = "Unknown"  # If the barcode is invalid

            print(
                f"DEBUG: Adding product -> ID: {product[0]}, Name: {product[1]}, Barcode: {barcode}, Price: ₱{price:.2f}")

            # Insert the correct values in the right order
            product_list.insert("", "end", values=(product[0], product[1], barcode, f"₱{price:.2f}"))

        conn.close()
    except Exception as e:
        print(f"Error loading products: {str(e)}")
