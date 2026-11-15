import unittest

from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product_factory import ProductFactory
from order import Order


class TestProductFactory(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "Tech Distributors", "sales@tech.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, self.supplier, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.weight, 1.5)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, self.supplier, download_size=300)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.download_size, 300)

    def test_result_can_be_used_as_a_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 100, self.supplier)
        self.assertIsInstance(product, Product)

    def test_type_text_is_case_and_space_insensitive(self):
        product = ProductFactory.create("  Physical ", "P001", "Lamp", 25.0, 10, self.supplier)
        self.assertIsInstance(product, PhysicalProduct)

    def test_unknown_type_raises_clear_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, self.supplier)
        self.assertIn("Unknown product type: service", str(context.exception))


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "Tech Distributors", "sales@tech.com")

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Lamp", 0, 10, self.supplier)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", -5.0, 10, self.supplier)

    def test_negative_starting_stock_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P001", "Lamp", 25.0, -1, self.supplier)

    def test_zero_stock_is_allowed(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 0, self.supplier)
        self.assertEqual(product.stock, 0)

    def test_update_stock_rejects_negative_for_both_types(self):
        for product_type in ("physical", "digital"):
            product = ProductFactory.create(product_type, "X001", "Item", 10.0, 5, self.supplier)
            with self.assertRaises(ValueError):
                product.update_stock(-1)
            self.assertEqual(product.stock, 5)

    def test_order_line_quantity_must_be_positive(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10, self.supplier)
        order = Order("O001")
        for bad_quantity in (0, -3):
            with self.assertRaises(ValueError):
                order.add_order_line(product, bad_quantity)
        self.assertEqual(order.order_lines, [])


if __name__ == "__main__":
    unittest.main()