from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style abstract base class for anything that can be shipped.

    This is a "can-do" relationship rather than an "is-a" one: a guitar is a
    product, and it can also be shipped. Any class that inherits from this is
    signing a contract to provide calculate_shipping_cost().

    It deliberately has no attributes and no product-specific code, so any
    object that can be shipped could implement it, not just products.
    """

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the cost of shipping this item, in dollars.

        Each implementing class decides its own pricing rule.
        """
        pass