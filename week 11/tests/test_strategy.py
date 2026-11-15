import unittest

from supplier import Supplier
from product_factory import ProductFactory
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)


def make_order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S001", "Tech Distributors", "sales@tech.com")
    chair = ProductFactory.create("physical", "P001", "Chair", 100.0, 10, supplier, weight=5.0)
    ebook = ProductFactory.create("digital", "D001", "E-book", 50.0, 10, supplier, download_size=2.0)

    order = Order("O001", discount)
    order.add_order_line(chair, 2)
    order.add_order_line(ebook, 1)
    return order


class TestDiscountStrategies(unittest.TestCase):

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount_takes_percentage_off(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225)

    def test_bulk_discount_applies_at_or_above_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(250), 230)
        self.assertEqual(BulkDiscount(200, 20).apply(200), 180)

    def test_bulk_discount_ignored_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(150), 150)

    def test_student_discount_is_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(100), 95)

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)

    def test_base_strategy_cannot_be_created(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()


class TestOrderUsesStrategy(unittest.TestCase):

    def test_order_defaults_to_no_discount(self):
        order = make_order_totalling_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_order_with_bulk_discount(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_works_without_changing_order(self):
        order = make_order_totalling_250(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_two_orders_can_share_one_strategy_object(self):
        shared = PercentageDiscount(10)
        order_a = make_order_totalling_250(shared)
        order_b = make_order_totalling_250(shared)
        self.assertIs(order_a.discount, order_b.discount)


if __name__ == "__main__":
    unittest.main()