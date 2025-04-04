import sqlite3

def resequence_product_ids():
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS temp_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT NOT NULL,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO temp_products (barcode, name, price)
            SELECT barcode, name, price FROM products;
        ''')

        cursor.execute('DROP TABLE IF EXISTS products')

        cursor.execute('ALTER TABLE temp_products RENAME TO products')

        conn.commit()
        conn.close()

        print("✅ Product IDs resequenced successfully!")

    except sqlite3.Error as e:
        print(f"Error resequencing product IDs: {e}")


def delete_product_from_db(product_id):
    try:
        conn = sqlite3.connect('products.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))

        conn.commit()

        if cursor.rowcount == 0:
            print(f"DEBUG: No product found with ID {product_id}. Deletion failed.")
            return False
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
        # I-clear muna ang validation label bago mag-proceed
        status_label.config(text="", foreground="black")

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

        # I-clear ang status label agad after 2 seconds
        status_label.after(2000, lambda: status_label.config(text=""))

    except Exception as e:
        print(f"Error deleting product: {e}")
        status_label.config(text="❌ Failed to delete product.", foreground="red")
        # I-clear ang error message after 2 seconds
        status_label.after(2000, lambda: status_label.config(text=""))
