def clear_list(product_list):
    # Tanggalin ang lahat ng items sa Treeview
    product_list.delete(*product_list.get_children())
    print("DEBUG: Clearing list...")
