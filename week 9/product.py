from abc import ABC, abstractmethod


class Product(ABC):
    """Abstract base class for every product in the inventory.

    Holds the data and behaviour that ALL products share (ID, name, price, stock).
    Every product must be either physical or digital, so Product itself cannot be
    instantiated; only its subclasses (PhysicalProduct, DigitalProduct) can.
    """

    def __init__(self, product_id, name, price, stock):
        """Initializer (constructor): runs automatically when a product object is created.

        The names in the brackets (product_id, name, ...) are PARAMETERS:
        values passed in from outside.
        The self.__ names below are ATTRIBUTES: data stored inside this object.
        Subclasses call this through super().__init__() instead of repeating it.
        """
        # Double underscore (__) marks the attribute as private
        # Outside code should read these through the getters below and change stock only through update_stock().
        self.__product_id = product_id.upper()  # keep IDs consistent, e.g. "p001" -> "P001"
        self.__name = name
        self.__price = price
        self.__stock = stock

    # ---------- Getters ----------
    # @property lets outside code READ a private attribute like a normal variable (product.name instead of product.get_name()), without being able to assign to it.
    # Subclasses also use these, since they can't see Product's private attributes directly.

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

    # ---------- Concrete methods (shared by every subclass) ----------

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
        """Print the details every product has on one line.

        Subclasses override this and call it with super() before adding their own details.
        """
        # :.2f shows the price with exactly 2 decimal places
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # ---------- Abstract method (each subclass MUST implement) ----------

    @abstractmethod
    def get_fulfilment_info(self):
        """Return a short message describing how this product reaches the customer.

        No implementation here on purpose: a physical product is shipped, a digital
        one is downloaded, so only the subclass knows the right answer.
        """
        pass

    # ---------- Conversion helper (for saving) ----------
    # Only CONVERTS data; file reading/writing stays in file_handler.py (Single Responsibility Principle).
    # from_dict() has moved into the subclasses: Product can no longer be created
    # directly, and each subclass needs its own extra value (weight / download size).

    def to_dict(self):
        """Return the shared product fields as a dictionary so they can be written to JSON."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }


# ---------- Quick test ----------
# Only runs when this file is executed directly (python product.py)
if __name__ == "__main__":
    # Product is abstract, so creating one directly should fail with a TypeError
    try:
        generic = Product("P001", "Mystery Item", 10.00, 1)
    except TypeError as error:
        print("Cannot create a plain Product:")
        print(error)