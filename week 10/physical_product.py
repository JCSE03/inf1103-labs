from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


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
    BASE_SHIPPING_FEE: float = 5.00
    SHIPPING_RATE_PER_KG: float = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        """Create a physical product: the usual Product details plus a weight (kg)."""
        # Hand the shared attributes to Product's constructor instead of
        # setting them again here; Product already knows how to do this
        super().__init__(product_id, name, price, stock, supplier)

        # Validate the weight the same way Product validates stock
        if not isinstance(weight, (int, float)) or isinstance(weight, bool):
            raise ValueError("Weight must be a number.")
        if weight < 0:
            raise ValueError("Weight cannot be negative.")

        # Private to PhysicalProduct (Python stores it as _PhysicalProduct__weight)
        self.__weight = weight

    @property
    def weight(self) -> float:
        """Return the product's weight in kilograms."""
        return self.__weight

    def display_information(self) -> None:
        """Override: show the common product details, then the weight.

        Product already prints ID, name, price and stock, so rather than
        repeating that line here we let the parent do its part and only add
        what is unique to a physical product.
        """
        super().display_information()
        print(f"    Weight: {self.__weight} kg")

    def get_fulfilment_info(self) -> str:
        """Physical products have to be packed and shipped."""
        return "Requires physical shipping to the customer's address."

    def calculate_shipping_cost(self) -> float:
        """Fulfil the CanBeShipped contract: shipping = base fee + rate x weight."""
        return self.BASE_SHIPPING_FEE + self.SHIPPING_RATE_PER_KG * self.__weight

    # ---------- Conversion helpers (for saving/loading) ----------

    def to_dict(self) -> dict:
        """Extend Product's dictionary with this product's type label and weight.

        The "type" label is what lets file_handler rebuild the right subclass later.
        """
        data = super().to_dict()  # id, name, price, stock
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "PhysicalProduct":
        """Rebuild a PhysicalProduct from one JSON entry."""
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["weight"])
