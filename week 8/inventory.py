class Inventory:
    """Manages a collection of Product objects.

    Single responsibility: store, add, search and display products.
    It does NOT load/save files, show the menu or ask for input,
    and it never touches a Product's private data directly.
    """

    def __init__(self):
        """Initializer: every new Inventory starts with an empty list of products."""
        # Private list that holds Product objects (not dictionaries like in Week 5)
        self.__products = []

    def add_product(self, product):
        """Add a Product to the inventory.

        Returns True if it was added, or False if a product with the same ID already exists.
        Returning True/False (instead of printing) lets the main program decide what message to show the user.
        """
        # Prevent duplicate IDs: reuse search_product() rather than repeating the loop here
        if self.search_product(product.product_id) is not None:
            return False

        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with a matching ID, or None if there isn't one.

        Replaces Week 5's find_product() helper.
        Returns the object instead of printing it, so both "Search" and "Update Stock" in the menu can use this method.
        """
        # .strip() removes accidental spaces, .upper() makes "p001" match "P001"
        product_id = product_id.strip().upper()

        for product in self.__products:
            # Read the ID through the Product's getter, not its private attribute
            if product.product_id == product_id:
                return product

        return None  # nothing matched

    def display_all(self):
        """Print every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)

        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products:
                # Each Product knows how to display itself, so Inventory doesn't need to know the format
                product.display_information()

        print("-" * 48)

    def get_all_products(self):
        """Return a copy of the product list (used later for saving to JSON).

        A copy is returned so outside code can't add or remove items in the real list without going through add_product().
        """
        return list(self.__products)


# ---------- Quick test ----------
# Only runs when this file is executed directly (python inventory.py)
if __name__ == "__main__":
    # Imported here because only the test needs to CREATE products;
    # the Inventory class itself just works with whatever Product objects it is given
    from product import Product

    # Same example as the lab sheet (section 2.6)
    inventory = Inventory()                              # create the inventory object
    product1 = Product("P001", "Laptop", 1200.00, 15)    # create products via __init__
    product2 = Product("P002", "Mouse", 25.50, 40)

    print("Add P001:", inventory.add_product(product1))  # True
    print("Add P002:", inventory.add_product(product2))  # True

    # Duplicate ID should be refused
    duplicate = Product("p001", "Another Laptop", 999.00, 1)
    print("Add duplicate P001:", inventory.add_product(duplicate))  # False

    # Search works with lowercase and extra spaces
    found = inventory.search_product(" p002 ")
    print("\nSearch ' p002 ':")
    found.display_information()  # ID: P002 | Name: Mouse | Price: $25.50 | Stock: 40

    # Searching for something that doesn't exist returns None
    print("Search P999:", inventory.search_product("P999"))  # None

    # Display everything
    inventory.display_all()