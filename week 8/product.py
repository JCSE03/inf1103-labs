class Product:
    """Blueprint for a single product in the inventory."""

    def __init__(self, product_id, name, price, stock):
        """Initializer (constructor): runs automatically when a Product object is created.

        The names in the brackets (product_id, name, ...) are PARAMETERS:
        values passed in from outside.
        The self.__ names below are ATTRIBUTES: data stored inside this object.
        """
        # Double underscore (__) marks the attribute as private
        # Outside code should read these through the getters below and change stock only through methods we add in the next commit.
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