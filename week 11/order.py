from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    """A customer order made up of OrderLine objects.

    Composition: the Order CREATES its OrderLines inside add_order_line() and is the
    only thing that holds them. Lines are never passed in from outside, never shared
    with another Order, and are discarded when removed or when the Order goes away.
    """

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id.upper()
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_id(self) -> str:
        """Return the order's ID."""
        return self.__order_id

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    @property
    def order_lines(self) -> list[OrderLine]:
        """Return a copy of the lines, so outside code can't add or remove lines
        without going through add_order_line() / remove_order_line()."""
        return list(self.__order_lines)


    def add_order_line(self, product: Product, quantity: int) -> None:
        """Create a new OrderLine for this product and quantity, and keep it.

        Takes a Product and a number, NOT a ready-made OrderLine: creating the
        part here is what makes this composition rather than aggregation.
        """
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the line for this product. Returns True if a line was removed.

        Unlike Inventory.remove_product(), the removed part is NOT handed back:
        an OrderLine has no meaning outside its Order, so it is simply discarded.
        """
        product_id = product_id.strip().upper()

        for line in self.__order_lines:
            if line.product.product_id == product_id:
                self.__order_lines.remove(line)
                return True

        return False


    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        return self.__discount.apply(self.calculate_subtotal())

    def display_information(self) -> None:
        """Print the order ID, every line, then the subtotal, discount and total."""
        print(f"Order {self.__order_id}")
        print("-" * 48)

        if not self.__order_lines:
            print("No items in this order.")
        else:
            for line in self.__order_lines:
                line.display_information()

        print("-" * 48)
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {type(self.__discount).__name__}")
        print(f"Total: ${self.calculate_total():.2f}")