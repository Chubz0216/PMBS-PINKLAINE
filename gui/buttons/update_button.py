import sqlite3
from utils.utils import load_products_into_treeview
import re  # Regular expression module

# Function to validate the barcode

def is_valid_barcode(barcode):
    # Walang space at digits lang dapat
    return bool(re.fullmatch(r'^\d+$', barcode))


# Function to get the selected product ID from the Treeview
def get_selected_product_id(product_list):
    selected_item = product_list.selection()
    if selected_item:
        # Retrieve the product ID (assuming it's the first column)
        product_id = product_list.item(selected_item[0])['values'][0]
        return product_id
    return None


# Update product function
def update_product(product_list, product_name_entry, price_entry, barcode_entry, validation_label):
    selected_product_id = get_selected_product_id(product_list)  # Get the selected product ID

    if selected_product_id:
        new_name = product_name_entry.get().strip()
        new_price = price_entry.get().strip()
        new_barcode = barcode_entry.get().strip()

        if new_name and new_price and new_barcode:
            # Validate the barcode
            if not is_valid_barcode(new_barcode):
                validation_label.config(text="Barcode must be numeric and contain no spaces.", foreground="red")
                validation_label.after(3000, lambda: validation_label.config(text=""))
                return

            try:
                # Clean up price input to ensure the Peso sign is only added once
                raw_price = new_price.replace("₱", "").replace(",", "").strip()

                # Connect to the database and update product
                conn = sqlite3.connect('products.db')
                cursor = conn.cursor()

                # Update the product in the database
                cursor.execute("""
                    UPDATE products
                    SET name = ?, price = ?, barcode = ?
                    WHERE id = ?
                """, (new_name, raw_price, new_barcode, selected_product_id))

                conn.commit()  # Commit the transaction to save the changes

                # Clear input fields and validation message
                product_name_entry.delete(0, 'end')
                price_entry.delete(0, 'end')
                barcode_entry.delete(0, 'end')
                validation_label.config(text="✅ Product updated successfully!", foreground="green")

                # Set a timer to clear the validation label after 3 seconds
                validation_label.after(3000, lambda: validation_label.config(text=""))

                # Now, update the selected product row in Treeview without reloading all data
                selected_item = product_list.selection()  # Get selected item
                if selected_item:
                    # Format price with Peso sign
                    product_list.item(selected_item,
                                      values=(selected_product_id, new_name, new_barcode, f"₱{float(raw_price):.2f}"))

                # Refresh the product list to reflect the updates
                # Instead of loading all data again, update just the modified item
                for item in product_list.get_children():
                    if product_list.item(item, "values")[0] == str(selected_product_id):
                        product_list.item(item, values=(selected_product_id, new_name, new_barcode, f"₱{float(raw_price):.2f}"))

                conn.close()  # Close the database connection
            except Exception as e:
                validation_label.config(text=f"❌ Error: {e}", foreground="red")
                validation_label.after(3000, lambda: validation_label.config(text=""))
        else:
            validation_label.config(text="❌ All fields are required!", foreground="red")
            validation_label.after(3000, lambda: validation_label.config(text=""))
    else:
        validation_label.config(text="❌ No product selected!", foreground="red")
        validation_label.after(3000, lambda: validation_label.config(text=""))