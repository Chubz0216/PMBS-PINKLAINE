import tkinter as tk

from database import check_price_data
from database import fix_price_column
from gui.buttons.clearlist_button import clear_list  # Import the clear_list function

# Sa function kung saan tinatawag ang get_all_products()
product_list = get_all_products()

# I-print para makita kung may laman ba
print(f"DEBUG: Retrieved products -> {product_list}")

# Kung may laman, siguraduhin na ang list ay may tamang format


fix_price_column()  # Run once para maayos ang price column

check_price_data()  # Tawagin bago i-load ang products

root = tk.Tk()
root.mainloop()