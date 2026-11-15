import os
import tempfile
import unittest
from unittest.mock import patch

from supplier import Supplier
from inventory import Inventory
from input_helpers import get_positive_float
from file_handler import load_products

LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


class TestGetPositiveFloat(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_keeps_asking_until_valid(self, mock_input, mock_print):
        result = get_positive_float("Price: ")

        self.assertEqual(result, 12.50)
        self.assertEqual(mock_input.call_count, 3)
        mock_print.assert_any_call("Please enter a valid number, e.g. 12.50")
        mock_print.assert_any_call("Please enter a number greater than zero.")


class TestLoadProducts(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()
        self.supplier = Supplier("S001", "Tech Distributors", "sales@tech.com")
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_csv(self, text: str) -> str:
        path = os.path.join(self.temp_dir.name, "products.csv")
        with open(path, "w", newline="") as f:
            f.write(text)
        return path

    @patch("builtins.print")
    def test_bad_rows_skipped_and_good_rows_loaded(self, mock_print):
        loaded = load_products(self.write_csv(LAB_CSV), self.inventory, self.supplier)

        self.assertEqual(loaded, 3)
        for product_id in ("P001", "D001", "P003"):
            self.assertIsNotNone(self.inventory.find_product(product_id))
        for product_id in ("S001", "P002"):
            self.assertIsNone(self.inventory.find_product(product_id))
        mock_print.assert_any_call("3 products loaded.")
        mock_print.assert_any_call("Load attempt finished.")

    @patch("builtins.print")
    def test_missing_file_handled_gracefully(self, mock_print):
        missing_path = os.path.join(self.temp_dir.name, "does_not_exist.csv")

        loaded = load_products(missing_path, self.inventory, self.supplier)

        self.assertEqual(loaded, 0)
        self.assertEqual(self.inventory.get_all_products(), [])
        mock_print.assert_any_call(f"Products file not found: {missing_path}")
        mock_print.assert_any_call("Load attempt finished.")


if __name__ == "__main__":
    unittest.main()