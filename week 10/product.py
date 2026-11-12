from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):
    """Abstract base class for every product in the inventory.

    Holds the data and behaviour that ALL products share (ID, name, price, stock).
    Every product must be either physical or digital, so Product itself cannot be
    instantiated; only its subclasses (PhysicalProduct, DigitalProduct) can.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        """Initializer (constructor): runs automatically when a product object is created.

        The names in the brackets (product_id, name, ...) are PARAMETERS:
        values passed in from outside.
        The self.__ names below are ATTRIBUTES: data stored inside this object.
        Subclasses call this through super().__init__() instead of repeating it.
        """
        self.__product_id = product_id.upper() 
        self.__name = name
        self.__price = price
        self.__stock = stock
        self.__supplier = supplier

    @property
    def product_id(self) -> str:
        """Return the product's ID."""
        return self.__product_id

    @property
    def name(self) -> str:
        """Return the product's name."""
        return self.__name

    @property
    def price(self) -> float:
        """Return the product's price."""
        return self.__price

    @property
    def stock(self) -> int:
        """Return how many units are in stock."""
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        """returns the product's supplier"""
        return self.__supplier


    def update_stock(self, quantity: int) -> None:
        """Set the stock to a new quantity, but only if the value is valid.

        This is encapsulation in action: outside code can't write any value it likes into __stock.
        It has to go through this method, and the Product decides what is acceptable.
        """
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Stock must be a whole number.")

        if quantity < 0:
            raise ValueError("Stock cannot be negative.")

        self.__stock = quantity

    def display_information(self) -> None:
        """Print the details every product has on one line.

        Subclasses override this and call it with super() before adding their own details.
        """
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")


    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a short message describing how this product reaches the customer.

        No implementation here on purpose: a physical product is shipped, a digital
        one is downloaded, so only the subclass knows the right answer.
        """
        pass


    def to_dict(self) -> dict:
        """Return the shared product fields as a dictionary so they can be written to JSON."""
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier_id": self.__supplier.supplier_id,
        }