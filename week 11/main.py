from inventory import Inventory
from supplier import Supplier
from can_be_shipped import CanBeShipped
from product_factory import ProductFactory
from input_helpers import get_positive_float, get_non_negative_int
from file_handler import load_inventory, save_inventory



def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    """List the known suppliers and return the one the user picks, or None if invalid."""
    if not suppliers:
        print("No suppliers available.")
        return None

    print("Suppliers:")
    for supplier in suppliers.values():
        supplier.display_information()

    supplier_id = input("Choose Supplier ID: ").strip().upper()
    return suppliers.get(supplier_id)


def add_product(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    """Ask the user for product details, create the right kind of product and add it to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    if inventory.find_product(product_id) is not None:
        print("A product with that ID already exists.")
        return

    name = input("Product Name: ").strip()

    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("Supplier not found. Product not added.")
        return

    print("Product Type:")
    print("1. Physical Product")
    print("2. Digital Product")
    menu_to_type = {"1": "physical", "2": "digital"}
    product_type = menu_to_type.get(input("Choose type (1-2): ").strip())

    if product_type is None:
        print("Invalid product type. Product not added.")
        return

    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_positive_float("Weight (kg): ")
    else:
        download_size = get_positive_float("Download Size (MB): ")

    try:
        product = ProductFactory.create(product_type, product_id, name, price, stock,
                                        supplier, weight=weight, download_size=download_size)
    except ValueError as error:
        print(f"Invalid product ({error}). Product not added.")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("A product with that ID already exists.")


def update_stock(inventory: Inventory) -> None:
    """Find a product by ID and change its stock through update_stock()."""
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: "))

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product.name}")
    print(f"Current Stock: {product.stock}")

    try:
        new_stock = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid number entered. Stock not changed.")
        return

    try:
        product.update_stock(new_stock)
        print("Stock updated successfully!")
    except ValueError as error:
        print(f"{error} Stock not changed.")


def search_product(inventory: Inventory) -> None:
    """Search for one product by ID and display its details, supplier, fulfilment and shipping info."""
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: "))

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    product.display_information()

    print("Supplied by:", end=" ")
    product.supplier.display_information()

    print(f"Fulfilment: {product.get_fulfilment_info()}")

    if isinstance(product, CanBeShipped):
        print(f"Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def main() -> None:
    """Run the menu loop until the user chooses Exit."""
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory, suppliers = load_inventory()

    while True:
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
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory, suppliers)
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory(inventory, suppliers)
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()