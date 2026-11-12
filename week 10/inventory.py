from product import Product 

class Inventory:
    """Manages a collection of Product objects.

    Single responsibility: store, add, find, remove and display products.
    It does NOT load/save files, show the menu or ask for input,
    and it never touches a Product's private data directly.
    """

    def __init__(self) -> None:
        """Initializer: every new Inventory starts with an empty list of products."""
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        """Add a Product to the inventory.

        Returns True if it was added, or False if a product with the same ID already exists.
        Returning True/False (instead of printing) lets the main program decide what message to show the user.
        """
        if self.find_product(product.product_id) is not None:
            return False

        self.__products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        """Return the Product with a matching ID, or None if there isn't one.

        Renamed from search_product() to match the Lab 8 design.
        Returns the object instead of printing it, so "Search", "Update Stock"
        and remove_product() can all reuse this method.
        """
        product_id = product_id.strip().upper()

        for product in self.__products:
            if product.product_id == product_id:
                return product

        return None

    def remove_product(self, product_id: str) -> Product | None:
        """Remove a product from this inventory and hand it back, or return None if not found.

        Aggregation: removing only drops the inventory's REFERENCE to the product.
        The product object itself still exists, so it can be added to another inventory.
        """
        product = self.find_product(product_id)

        if product is not None:
            self.__products.remove(product)  

        return product 

    def display_all(self) -> None:
        """Print every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)

        if not self.__products:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()

        print("-" * 48)

    def get_all_products(self) -> list[Product]:
        """Return a copy of the product list (used for saving to JSON).

        A copy is returned so outside code can't add or remove items in the real list
        without going through add_product() / remove_product().
        """
        return list(self.__products)