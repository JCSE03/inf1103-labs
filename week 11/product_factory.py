from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier


class ProductFactory:

    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier,
               weight: float = 0.0, download_size: float = 0.0) -> Product:
        product_type = product_type.strip().lower()

        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, weight)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, download_size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")