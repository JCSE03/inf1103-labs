from product import Product
from file_handler import load_inventory, save_inventory

## Main program
# Responsibilities: display the menu, get user input, and call the right Inventory methods.
# It never reads or changes a Product's private data directly; it only uses getters and public methods.


def add_product(inventory):
    """Ask the user for product details, create a Product object and add it to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    # Check for a duplicate straight away, so the user isn't asked for details that will be thrown away
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()

    # try/except stops the program crashing if the user types text instead of a number
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Product not added.")
        return

    # Create a Product OBJECT (Week 5 built a dictionary here instead)
    product = Product(product_id, name, price, stock)

    # Inventory returns True/False; main decides what message to show
    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory):
    """Find a product by ID and change its stock through Product.update_stock()."""
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: "))

    if product is None:
        print("Product not found.")
        return

    # Read values through the getters (product.name, product.stock), not the private attributes
    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    # Step 1: main's job is checking the input IS a whole number
    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Stock not changed.")
        return

    # Step 2: the Product's job is deciding whether that number is ALLOWED (e.g. not negative)
    try:
        product.update_stock(new_stock)
        print("Stock updated successfully!")
    except ValueError as error:
        print(f"{error} Stock not changed.")


def search_product(inventory):
    """Search for one product by ID and display its details."""
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: "))

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    product.display_information()  # the Product displays itself
    print("-" * 48)


def main():
    """Run the menu loop until the user chooses Exit."""
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # load_inventory() returns a ready-to-use Inventory object filled with Product objects
    inventory = load_inventory()

    while True:  # keep showing the menu until the user exits
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        choice = input("Enter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break  # leave the loop -> program ends
        else:
            print("Invalid option. Please choose 1-6.")


# Only run main() when this file is executed directly
if __name__ == "__main__":
    main()