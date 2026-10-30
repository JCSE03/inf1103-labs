from product import Product


class PhysicalProduct(Product):
    """A product that physically exists, e.g. a laptop or a guitar.

    It is-a Product, so it inherits the ID, name, price, stock and all of
    Product's methods. The only new data it adds is the weight.
    """

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


# ---------- Quick test ----------
if __name__ == "__main__":
    guitar = PhysicalProduct("p101", "Acoustic Guitar", 350.00, 5, 2.5)

    # Attributes inherited from Product work exactly as before
    print(guitar.product_id, guitar.name, guitar.price, guitar.stock)  # P101 Acoustic Guitar 350.0 5
    print("Weight:", guitar.weight)  # 2.5

    # Inherited method: update_stock() was never written in this class
    guitar.update_stock(8)
    guitar.display_information()

    # A negative weight should be rejected by the constructor
    try:
        PhysicalProduct("P102", "Broken Scale", 10.00, 1, -3)
    except ValueError as error:
        print("Rejected:", error)  # Rejected: Weight cannot be negative.