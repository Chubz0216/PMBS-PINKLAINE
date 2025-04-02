from database import get_all_products

def view_product_list(product_list):
    # Kunin ang lahat ng products mula sa database
    products = get_all_products()

    # Linisin ang mga dati nang laman ng Treeview
    product_list.delete(*product_list.get_children())

    # I-loop ang mga products at ilagay sa Treeview
    for product in products:
        try:
            # Siguraduhin na tama ang type ng price at barcode
            price = float(product[2])  # Price (dapat number)
            barcode = str(product[3])  # Barcode (dapat string)
        except ValueError:
            price = 0.00  # Default value kung may error sa conversion
            barcode = "Unknown"

        # Ipakita ang product details sa Treeview
        product_list.insert("", "end", values=(product[0], product[1], barcode, f"₱{price:.2f}"))
