
# List / Array
inventory = [
    {"id": "P001", "name": "Laptop",   "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse",    "price": 25.50,   "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00,   "stock": 25},
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

# for testing
if __name__ == "__main__":
    display_all()