import sqlite3
from database import update_product_in_db


def update_product(product_list, product_name_entry, price_entry, barcode_entry, validation_label):
    # Kunin ang selected product mula sa Treeview
    selected_item = product_list.selection()
    if not selected_item:
        validation_label.config(text="Please select a product to update.", foreground="red")
        return

    # Kunin ang values ng selected product
    product = product_list.item(selected_item)["values"]
    product_id = product[0]  # Ang ID ng product
    name = product[1]
    price = product[3]
    barcode = product[2]

    # I-set ang mga entry fields sa existing values
    product_name_entry.delete(0, "end")
    product_name_entry.insert(0, name)

    price_entry.delete(0, "end")
    price_entry.insert(0, price)

    barcode_entry.delete(0, "end")
    barcode_entry.insert(0, barcode)

    # Add button will now trigger the update
    def save_updated_product():
        updated_name = product_name_entry.get().strip()
        updated_price = price_entry.get().strip()
        updated_barcode = barcode_entry.get().strip()

        # Call the update function
        update_product_in_db(product_id, updated_name, updated_price, updated_barcode)

        # I-update ang Treeview
        product_list.item(selected_item, values=(product_id, updated_name, updated_barcode, updated_price))

        validation_label.config(text="Product updated successfully!", foreground="green")

    return save_updated_product
