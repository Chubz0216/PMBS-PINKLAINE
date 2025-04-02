import sqlite3


def check_price_data():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Kunin ang lahat ng products at tingnan ang type ng price
        cursor.execute("SELECT id, name, price, barcode FROM products")
        products = cursor.fetchall()

        for product in products:
            print(f"DEBUG: ID={product[0]}, Name={product[1]}, Type of price={type(product[2])}, Value={product[2]}")

        conn.close()

    except sqlite3.Error as e:
        print(f"Error checking price data: {e}")


def connect_db():
    return sqlite3.connect('products.db')  # Path to your SQLite database file


def add_product(name, price, barcode):
    try:
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

        conn.commit()

    except sqlite3.Error as e:
        print(f"Error: {e}")
        raise e  # Re-raise the exception to be handled by the calling function

    finally:
        conn.close()  # Ensure the connection is always closed


def get_all_products():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        return products
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()


def fix_price_column():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Check if 'price_new' column exists (para hindi mag-error kung na-run na dati)
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]

        if "price_new" not in columns:
            # Gawin nating REAL (float) ang price
            cursor.execute("ALTER TABLE products ADD COLUMN price_new REAL")
            cursor.execute("UPDATE products SET price_new = CAST(price AS REAL)")
            cursor.execute("ALTER TABLE products DROP COLUMN price")
            cursor.execute("ALTER TABLE products RENAME COLUMN price_new TO price")
            conn.commit()
            print("✅ Price column has been fixed!")

        else:
            print("⚠️ Price column is already fixed.")

    except sqlite3.Error as e:
        print(f"Error fixing price column: {e}")

    finally:
        conn.close()


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

    except sqlite3.Error as e:
        print(f"Error updating product: {e}")

    finally:
        conn.close()

import sqlite3

def delete_product_from_db(product_id):
    try:
        # Connect to the database
        conn = sqlite3.connect('products.db')  # Ensure this is the correct database file path
        cursor = conn.cursor()

        # SQL query to delete the product
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

        # Commit and close connection
        conn.commit()
        conn.close()

        print(f"Product with ID {product_id} deleted from database.")
    except sqlite3.Error as e:
        print(f"Error deleting product from database: {e}")

def add_auto_increment_id():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Add 'id' column with auto-increment to products table
        cursor.execute("ALTER TABLE products ADD COLUMN id INTEGER PRIMARY KEY AUTOINCREMENT")

        conn.commit()
        conn.close()
        print("ID column added successfully.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
