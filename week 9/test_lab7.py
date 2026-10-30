"""Lab 7 test script: checks each point in section 7 (Testing and review).

Run with:  python test_lab7.py
Each check prints PASS, or stops with an AssertionError explaining what broke.
"""
import os
import tempfile

# Point file_handler at a throwaway folder BEFORE importing it,
# so the save/load test never overwrites the real data/inventory.json
os.environ["DATA_DIR"] = tempfile.mkdtemp()

from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handler import load_inventory, save_inventory


def check(description, condition):
    """Print PASS for a passing check; stop the script on a failing one."""
    assert condition, f"FAIL: {description}"
    print(f"PASS: {description}")


laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, 2.2)
ebook = DigitalProduct("D001", "Python E-book", 29.90, 50, 12.5)

# 1 & 2: each subclass stores its own extra attribute
check("Physical products store their weight", laptop.weight == 2.2)
check("Digital products store their download size", ebook.download_size == 12.5)

# 3: both subclasses implement the abstract method with their own message
check("PhysicalProduct implements get_fulfilment_info()", "shipping" in laptop.get_fulfilment_info())
check("DigitalProduct implements get_fulfilment_info()", "digitally" in ebook.get_fulfilment_info())

# 4: Product is abstract, so creating one directly must raise a TypeError
try:
    Product("X001", "Generic", 1.00, 1)
    abstract_blocked = False
except TypeError:
    abstract_blocked = True
check("Product cannot be instantiated directly", abstract_blocked)

# 5: shipping = $5 base + $2 per kg  ->  5 + 2 * 2.2 = 9.40
check("Physical products calculate shipping cost", round(laptop.calculate_shipping_cost(), 2) == 9.40)

# 6: digital products never signed the CanBeShipped contract
check("Digital products don't implement CanBeShipped", not isinstance(ebook, CanBeShipped))

# 7: Inventory still works with a mix of subclasses
inventory = Inventory()
check("Inventory adds both product types", inventory.add_product(laptop) and inventory.add_product(ebook))
check("Inventory rejects duplicate IDs", not inventory.add_product(PhysicalProduct("p001", "Copy", 1.0, 1, 1.0)))
check("Inventory search still works", inventory.search_product(" d001 ") is ebook)

# 8: save, load into a brand-new Inventory, and confirm the types came back correctly
save_inventory(inventory)
reloaded = load_inventory()
loaded_laptop = reloaded.search_product("P001")
loaded_ebook = reloaded.search_product("D001")
check("JSON restores PhysicalProduct with its weight",
      isinstance(loaded_laptop, PhysicalProduct) and loaded_laptop.weight == 2.2)
check("JSON restores DigitalProduct with its download size",
      isinstance(loaded_ebook, DigitalProduct) and loaded_ebook.download_size == 12.5)

print("\nAll Lab 7 checks passed.")