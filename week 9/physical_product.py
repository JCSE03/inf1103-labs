from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that physically exists, e.g. a laptop or a guitar.

    It is-a Product, so it inherits the ID, name, price, stock and all of
    Product's methods. The only new data it adds is the weight.

    It also implements the CanBeShipped interface. This is still single
    inheritance: Product is the only parent CLASS, while CanBeShipped is just a
    contract with no data or code of its own.
    """

    # Shipping rule: a flat handling fee plus a charge for every kg.
    # Kept as class constants so the rates are easy to find and change.
    BASE_SHIPPING_FEE = 5.00
    SHIPPING_RATE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        """Create a physical product: the usual Product details plus a weight (kg)."""
        # Hand the shared attributes to Product's constructor instead of
        # setting them again here; Product already knows how to do this
        super().__init__(product_id, name, price, stock)

        # Validate the weight the same way Product validates stock
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise ValueError("Weight must be a number.")
        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        # Private to PhysicalProduct (Python stores it as _PhysicalProduct__weight)
        self.__weight = weight

    @property
    def weight(self):
        """Return the product's weight in kilograms."""
        return self.__weight

    def display_information(self):
        """Override: show the common product details, then the weight.

        Product already prints ID, name, price and stock, so rather than
        repeating that line here we let the parent do its part and only add
        what is unique to a physical product.
        """
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    def get_fulfilment_info(self):
        """Physical products have to be packed and shipped."""
        return "Requires physical shipping to the customer's address."

    def calculate_shipping_cost(self):
        """Fulfil the CanBeShipped contract: shipping = base fee + rate x weight."""
        return self.BASE_SHIPPING_FEE + self.SHIPPING_RATE_PER_KG * self.__weight


# ---------- Quick test ----------
if __name__ == "__main__":
    guitar = PhysicalProduct("p101", "Acoustic Guitar", 350.00, 5, 2.5)

    # Attributes inherited from Product work exactly as before
    print(guitar.product_id, guitar.name, guitar.price, guitar.stock)  # P101 Acoustic Guitar 350.0 5
    print("Weight:", guitar.weight)  # 2.5

    # Inherited method: update_stock() was never written in this class
    guitar.update_stock(8)
    guitar.display_information()
    print("Fulfilment:", guitar.get_fulfilment_info())

    # Shipping cost for a few different weights: $5 + $2/kg
    for kg in (0, 1.5, 10):
        item = PhysicalProduct("P103", "Test Box", 1.00, 1, kg)
        print(f"Shipping for {kg} kg: ${item.calculate_shipping_cost():.2f}")  # $5.00, $8.00, $25.00

    # A negative weight should be rejected by the constructor
    try:
        PhysicalProduct("P102", "Broken Scale", 10.00, 1, -3)
    except ValueError as error:
        print("Rejected:", error)  # Rejected: Weight cannot be negative.