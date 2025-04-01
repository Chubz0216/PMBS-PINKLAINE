import sqlite3

def connect_db():
    return sqlite3.connect('products.db')  # Path to your SQLite database file

def add_product(name, price, barcode):
    try:
        # Establish connection to the database
        conn = connect_db()
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                barcode TEXT NOT NULL
            )
        ''')

        # Insert the new product into the database
        cursor.execute('''
            INSERT INTO products (name, price, barcode)
            VALUES (?, ?, ?)
        ''', (name, price, barcode))

        # Commit the changes
        conn.commit()
        conn.close()  # Close the connection

    except sqlite3.Error as e:
        print(f"Error: {e}")
        raise e  # Re-raise the exception so it can be handled in the calling function

def get_all_products():
    try:
        # Establish connection to the database
        conn = connect_db()
        cursor = conn.cursor()

        # Retrieve all products from the database
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        conn.close()  # Close the connection
        return products

    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []

def update_product_in_db(product_id, name, price, barcode):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Update ang product sa database gamit ang ID
            cursor.execute('''
                UPDATE products
                SET name = ?, price = ?, barcode = ?
                WHERE id = ?
            ''', (name, price, barcode, product_id))

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            print(f"Error updating product: {e}")
