from product import Product
from supplier import Supplier

class DigitalProduct(Product):
    """A product delivered as a download, e.g. software or an e-book.

    It has no weight, but it does have a download size, which is the
    one attribute it adds on top of Product.
    """

    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        """Create a digital product: the usual Product details plus a download size (MB)."""
        # Reuse Product's constructor for the shared attributes
        super().__init__(product_id, name, price, stock, supplier)

        if not isinstance(download_size, (int, float)) or isinstance(download_size, bool):
            raise ValueError("Download size must be a number.")
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")

        self.__download_size = download_size

    @property
    def download_size(self) -> float:
        """Return the download size in megabytes."""
        return self.__download_size

    def display_information(self) -> None:
        """Override: show the common product details, then the download size."""
        super().display_information()  # parent prints the shared details
        print(f"    Download Size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        """Digital products are delivered online, so nothing is shipped."""
        return "Delivered digitally via a download link sent to the customer's email."

    # ---------- Conversion helpers (for saving/loading) ----------

    def to_dict(self) -> dict:
        """Extend Product's dictionary with this product's type label and download size.

        The "type" label is what lets file_handler rebuild the right subclass later.
        """
        data = super().to_dict()  # id, name, price, stock
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict, supplier: Supplier) -> "DigitalProduct":
        """Rebuild a DigitalProduct from one JSON entry."""
        return cls(data["id"], data["name"], data["price"], data["stock"], supplier, data["download_size"])