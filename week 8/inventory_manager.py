import os
import json

## Week 5 Lab Phase 1

# List / Array
inventory = [
    # {"id": "P001", "name": "Laptop",   "price": 1200.00, "stock": 15},
    # {"id": "P002", "name": "Mouse",    "price": 25.50,   "stock": 40},
    # {"id": "P003", "name": "Keyboard", "price": 45.00,   "stock": 25},
]

def find_product(product_id):
    """Helper: return the product dictionary matching the ID, or None."""
    for product in inventory:
        # .upper() makes "p001" and "P001" count as the same ID
        if product["id"] == product_id.upper():
            return product
    return None  # nothing matched


def add_product():
    """Ask the user for details and add a new product to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()

    # Prevent duplicate IDs
    if find_product(product_id):
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

    # Build the new dictionary and append it to the list
    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!")


def update_stock():
    """Find a product by ID and change its stock quantity."""
    print("\nUpdate Stock")
    product = find_product(input("Enter Product ID: ").strip())

    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    try:
        product["stock"] = int(input("New Stock Quantity: "))
        print("Stock updated successfully!")
    except ValueError:
        print("Invalid number entered. Stock not changed.")


def search_product():
    """Search for one product by ID and display its details."""
    print("\nSearch Product")
    product = find_product(input("Enter Product ID: ").strip())

    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")   # :.2f = 2 decimal places
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def display_all():
    """Print every product in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    for p in inventory:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("-" * 48)


## Week 5 lab phase 2
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) # find the current filepath
DATA_DIR = os.environ.get("DATA_DIR", SCRIPT_DIR) # DATA_DIR defaults to the script's folder. Docker can override it with an environment variable
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

def load_inventory():
    """Load inventory.json if it exists, otherwise start with an empty inventory."""
    global inventory  # we are replacing the whole list, so we need to global it

    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        with open(INVENTORY_FILE, "r") as f:
            inventory = json.load(f)   # JSON file -> Python list of dicts
        print("Inventory loaded successfully.")
    else:
        print("inventory.json not found. Starting with an empty inventory.")
        inventory = []

def save_inventory():
    """Write the current inventory to inventory.json."""
    print("Saving inventory...")
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)   # indent=4 makes the file readable
    print("Inventory saved successfully to inventory.json.")

## run once for testing (works)
# if __name__ == "__main__":
    # Start from the three sample products
    # no load_inventory() here, because it would reset the list to empty when no file exists yet
    # inventory = [
    #     {"id": "P001", "name": "Laptop",   "price": 1200.00, "stock": 15},
    #     {"id": "P002", "name": "Mouse",    "price": 25.50,   "stock": 40},
    #     {"id": "P003", "name": "Keyboard", "price": 45.00,   "stock": 25},
    # ]
    # save_inventory()   # writes the 3 products to inventory.json
    # load_inventory()


## main program
def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    load_inventory()   # restore saved data when the program starts

    while True:        # keep showing the menu until the user exits
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
            display_all()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_stock()
        elif choice == "4":
            search_product()
        elif choice == "5":
            save_inventory()
        elif choice == "6":
            print("Saving inventory before exit...")
            save_inventory()
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break      # leave the loop -> program ends
        else:
            print("Invalid option. Please choose 1-6.")


# Only run main() when this file is executed directly
if __name__ == "__main__":
    main()