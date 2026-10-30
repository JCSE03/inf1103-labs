class Product:
    """Blueprint for a single product in the inventory."""

    def __init__(self, product_id, name, price, stock):
        """Initializer (constructor): runs automatically when a Product object is created.

        The names in the brackets (product_id, name, ...) are PARAMETERS:
        values passed in from outside.
        The self.__ names below are ATTRIBUTES: data stored inside this object.
        """
        # Double underscore (__) marks the attribute as private
        # Outside code should read these through the getters below and change stock only through update_stock().
        self.__product_id = product_id.upper()  # keep IDs consistent, e.g. "p001" -> "P001"
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---------- Getters ----------
    # @property lets outside code READ a private attribute like a normal variable (product.name instead of product.get_name()), without being able to assign to it.
    # Trying "product.name = 'x'" raises an AttributeError because there is no setter.

    @property
    def product_id(self):
        """Return the product's ID."""
        return self.__product_id

    @property
    def name(self):
        """Return the product's name."""
        return self.__name

    @property
    def price(self):
        """Return the product's price."""
        return self.__price

    @property
    def stock(self):
        """Return how many units are in stock."""
        return self.__stock

    # ---------- Methods ----------

    def update_stock(self, quantity):
        """Set the stock to a new quantity, but only if the value is valid.

        This is encapsulation in action: outside code can't write any value it likes into __stock.
        It has to go through this method, and the Product decides what is acceptable.
        """
        # bool counts as an int in Python (True == 1), so reject it explicitly
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock must be a whole number.")

        # A shop can't hold a negative number of items
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

        # Value passed every check, so it's safe to store
        self.__stock = quantity

    def display_information(self):
        """Print this product's details on one line."""
        # :.2f shows the price with exactly 2 decimal places
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # ---------- Conversion helpers (for saving/loading) ----------
    # These only CONVERT data; they don't open or write files.
    # File reading/writing stays in file_handler.py (Single Responsibility Principle).

    def to_dict(self):
        """Return this product as a dictionary so it can be written to JSON.

        Uses the same keys as Week 5, so the existing inventory.json still works.
        """
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a new Product from a dictionary (e.g. one entry read from JSON).

        @classmethod means this is called on the class itself: Product.from_dict(...)
        'cls' is the Product class, so cls(...) is the same as Product(...).
        """
        return cls(data["id"], data["name"], data["price"], data["stock"])


# ---------- Quick test ----------
# Only runs when this file is executed directly (python product.py),
# NOT when another file does "from product import Product".
if __name__ == "__main__":
    laptop = Product("p001", "Laptop", 1200.00, 15)

    # Reading values through the getters
    print(laptop.product_id, laptop.name, laptop.price, laptop.stock)  # P001 Laptop 1200.0 15

    # this does NOT change the real private stock, it silently creates a NEW attribute
    laptop.__stock = 50
    print("Real stock is still:", laptop.stock)  # still 15
    # Name mangling: Python actually stores the private attribute under this name
    print("Mangled name:", laptop._Product__stock)  # 15

    # The correct way to change stock: through the public method
    laptop.update_stock(50)
    print("After update_stock(50):", laptop.stock)  # 50

    # Invalid value: the Product refuses it and the stock stays the same
    try:
        laptop.update_stock(-5)
    except ValueError as error:
        print("Rejected:", error)  # Rejected: Stock cannot be negative.
    print("Stock unchanged:", laptop.stock)  # still 50

    # Display the product's information
    laptop.display_information()  # ID: P001 | Name: Laptop | Price: $1200.00 | Stock: 50

    # Convert to a dictionary and back again (round trip)
    print("to_dict:", laptop.to_dict())  # {'id': 'P001', 'name': 'Laptop', 'price': 1200.0, 'stock': 50}
    copy = Product.from_dict(laptop.to_dict())
    copy.display_information()  # same line as above