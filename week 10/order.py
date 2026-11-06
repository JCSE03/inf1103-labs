from product import Product  # only used for type hints
from order_line import OrderLine


class Order:
    """A customer order made up of OrderLine objects.

    Composition: the Order CREATES its OrderLines inside add_order_line() and is the
    only thing that holds them. Lines are never passed in from outside, never shared
    with another Order, and are discarded when removed or when the Order goes away.
    """

    def __init__(self, order_id: str) -> None:
        """Every new Order starts with an ID and no lines."""
        self.__order_id: str = order_id.upper()  # keep IDs consistent, e.g. "o001" -> "O001"
        self.__order_lines: list[OrderLine] = []

    # ---------- Getters ----------

    @property
    def order_id(self) -> str:
        """Return the order's ID."""
        return self.__order_id

    @property
    def order_lines(self) -> list[OrderLine]:
        """Return a copy of the lines, so outside code can't add or remove lines
        without going through add_order_line() / remove_order_line()."""
        return list(self.__order_lines)

    # ---------- Managing its own parts ----------

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this product and quantity, and keep it.

        Takes a Product and a number, NOT a ready-made OrderLine: creating the
        part here is what makes this composition rather than aggregation.
        """
        order_line = OrderLine(product, quantity)  # the Order creates its own part
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Returns True if a line was removed.

        Unlike Inventory.remove_product(), the removed part is NOT handed back:
        an OrderLine has no meaning outside its Order, so it is simply discarded.
        """
        # .strip() / .upper() so " p001 " still matches "P001"
        product_id = product_id.strip().upper()

        for line in self.__order_lines:
            if line.product.product_id == product_id:
                self.__order_lines.remove(line)
                return True

        return False  # no line for that product

    # ---------- Behaviour ----------

    def calculate_total(self) -> float:
        """Return the order total by asking each line for its own subtotal."""
        # Order doesn't do price x quantity itself; each OrderLine knows its own subtotal
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        """Print the order ID, every line, then the total."""
        print(f"Order {self.__order_id}")
        print("-" * 48)

        if not self.__order_lines:
            print("No items in this order.")
        else:
            for line in self.__order_lines:
                line.display_information()  # each line displays itself

        print("-" * 48)
        print(f"Total: ${self.calculate_total():.2f}")