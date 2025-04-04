import sqlite3

def resequence_product_ids():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # Mag-create ng bagong temporary table na may sequence ng IDs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

        # Mag-copy ng data mula sa original products table to temp_products
        cursor.execute('''
            INSERT INTO temp_products (barcode, name, price)
            SELECT barcode, name, price FROM products;
        ''')

        # Tanggalin ang original na table
        cursor.execute('DROP TABLE IF EXISTS products')

        # I-rename ang temp_products table upang maging products ulit
        cursor.execute('ALTER TABLE temp_products RENAME TO products')

        # Commit the changes and close connection
        conn.commit()
        conn.close()

        print("✅ Product IDs resequenced successfully!")

    except sqlite3.Error as e:
        print(f"Error resequencing product IDs: {e}")


def delete_product_from_db(product_id):
    try:
        # Connect to the database
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        # SQL query to delete the product
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

        # Commit and close connection
        conn.commit()

        # Check kung ilan ang rows na affected (deleted)
        if cursor.rowcount == 0:
            print(f"DEBUG: No product found with ID {product_id}. Deletion failed.")
            return False  # No product was deleted
        else:
            print(f"DEBUG: Product with ID {product_id} deleted from database.")
            return True
    except sqlite3.Error as e:
        print(f"Error deleting product from database: {e}")
        return False
    finally:
        conn.close()

def delete_product(product_list, selected_product_id, status_label):
    try:
        # I-delete ang product mula sa database
        if not delete_product_from_db(selected_product_id):
            status_label.config(text="❌ Failed to delete product from database.", foreground="red")
            return

        # Alisin ang product mula sa Treeview
        for item in product_list.get_children():
            if product_list.item(item, "values")[0] == str(selected_product_id):
                product_list.delete(item)
                break

        # Tawagin ang resequencing function pagkatapos ng delete
        resequence_product_ids()

        # I-update ang status_label na may success message
        status_label.config(text="✅ Product deleted and IDs resequenced successfully!", foreground="green")

    except Exception as e:
        print(f"Error deleting product: {e}")
        status_label.config(text="❌ Failed to delete product.", foreground="red")

