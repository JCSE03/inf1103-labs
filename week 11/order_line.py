from product import Product


class OrderLine:
    """One line of an order: a product and the quantity requested.

    Composition: an OrderLine is a PART of an Order. Only Order should create it
    (through Order.add_order_line()), it belongs to exactly one Order, and it is
    removed along with that Order. It is never created on its own or moved to another Order.

    Association: the OrderLine refers to a Product but does NOT own it.
    The same Product can also sit in an Inventory or appear in other orders.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        """Store the product reference and how many units were ordered."""
        # bool counts as an int in Python (True == 1), so reject it explicitly
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be a whole number.")

        if quantity <= 0:
            raise ValueError("Quantity must be at least 1.")

        self.__product: Product = product
        self.__quantity: int = quantity

    # ---------- Getters ----------

    @property
    def product(self) -> Product:
        """Return the product this line refers to."""
        return self.__product

    @property
    def quantity(self) -> int:
        """Return how many units were ordered."""
        return self.__quantity

    # ---------- Behaviour ----------

    def calculate_subtotal(self) -> float:
        """Return price x quantity for this line."""
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        """Print this line's product, quantity and subtotal on one line."""
        print(f"{self.__product.product_id} | {self.__product.name} | "
              f"Qty: {self.__quantity} | Subtotal: ${self.calculate_subtotal():.2f}")