import os
import json

from inventory import Inventory
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(SCRIPT_DIR, "data"))
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")
PRODUCT_TYPES = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}


def load_inventory() -> tuple[Inventory, dict[str, Supplier]]:
    """Read inventory.json and return (filled Inventory, suppliers by ID).

    Suppliers are rebuilt FIRST, then each product is linked to the matching
    Supplier object, so products that share a supplier share the same object.
    If the file doesn't exist yet, return an empty Inventory and no suppliers.
    """
    inventory = Inventory() 
    suppliers: dict[str, Supplier] = {}

    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory, suppliers

    print("inventory.json found.")
    with open(INVENTORY_FILE, "r") as f:
        data = json.load(f)

    for supplier_data in data.get("suppliers", []):
        supplier = Supplier.from_dict(supplier_data)
        suppliers[supplier.supplier_id] = supplier

    for item in data.get("products", []):
        product_class = PRODUCT_TYPES.get(item.get("type"))

        if product_class is None:
            print(f"Skipping {item.get('id', '?')}: unknown product type '{item.get('type')}'.")
            continue

        supplier = suppliers.get(item.get("supplier_id"))
        if supplier is None:
            print(f"Skipping {item.get('id', '?')}: unknown supplier '{item.get('supplier_id')}'.")
            continue

        inventory.add_product(product_class.from_dict(item, supplier))

    print("Inventory loaded successfully.")
    return inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    """Write every supplier and every product to inventory.json."""
    print("Saving inventory...")

    os.makedirs(DATA_DIR, exist_ok=True)

    data = {
        "suppliers": [supplier.to_dict() for supplier in suppliers.values()],
        "products": [product.to_dict() for product in inventory.get_all_products()],
    }

    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("Inventory saved successfully to inventory.json.")