def add_product_to_db(name_entry, price_entry, barcode_entry, validation_label):
    name = name_entry.get().strip()
    price = price_entry.get().strip()
    barcode = barcode_entry.get().strip()

    # Validation to check if all fields are filled
    if not name or not price or not barcode:
        validation_label.config(text="Please fill out all fields.", foreground="red")
        return

    # Simulate adding the product to the database
    # Here, you would normally add code to insert into your database

    # After successful addition
    validation_label.config(text="Product added successfully!", foreground="green")