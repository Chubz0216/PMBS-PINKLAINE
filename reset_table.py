import sqlite3

def connect_db():
    return sqlite3.connect('products.db')  # Path to your SQLite database file

def reset_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Drop the existing table if it exists
        cursor.execute("DROP TABLE IF EXISTS products")

        # Recreate the table with AUTOINCREMENT on id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                barcode TEXT NOT NULL
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("✅ Table reset and recreated with AUTOINCREMENT.")

    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    reset_table()  # Call this once at the start to set up the table
