from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from file_handler import load_inventory, save_inventory

## Main program
# Responsibilities: display the menu, get user input, and call the right Inventory/product methods.
# It never reads or changes a product's private data directly; it only uses getters and public methods.


def add_product(inventory):
    """Ask the user for product details, create the right kind of product and add it to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    # Check for a duplicate straight away, so the user isn't asked for details that will be thrown away
    if inventory.search_product(product_id) is not None:
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()

    # Product is abstract now, so the user has to pick a concrete type
    print("Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Choose type (1-2): ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type. Product not added.")
        return

    # One try block covers both kinds of bad input:
    #  - float()/int() fail if the user types text instead of a number
    #  - the product's constructor rejects values like a negative weight
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        # Only ask for the extra detail that this product type actually needs
        if product_type == "1":
            weight = float(input("Weight (kg): "))
            product = PhysicalProduct(product_id, name, price, stock, weight)
        else:
            download_size = float(input("Download Size (MB): "))
            product = DigitalProduct(product_id, name, price, stock, download_size)
    except ValueError as error:
        print(f"Invalid input ({error}). Product not added.")
        return

    # Inventory returns True/False; main decides what message to show
    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory):
    """Find a product by ID and change its stock through update_stock()."""
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

    # Step 2: the product's job is deciding whether that number is ALLOWED (e.g. not negative)
    try:
        product.update_stock(new_stock)
        print("Stock updated successfully!")
    except ValueError as error:
        print(f"{error} Stock not changed.")


def search_product(inventory):
    """Search for one product by ID and display its details, fulfilment and shipping info."""
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: "))

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    product.display_information()  # the subclass's overridden version runs automatically
    print(f"Fulfilment: {product.get_fulfilment_info()}")

    # Only products that signed the CanBeShipped contract have a shipping cost
    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def main():
    """Run the menu loop until the user chooses Exit."""
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    # load_inventory() returns a ready-to-use Inventory filled with Physical/Digital product objects
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