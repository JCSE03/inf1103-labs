import os
import json

from inventory import Inventory
from supplier import Supplier
from product_factory import ProductFactory


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(SCRIPT_DIR, "data"))
INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


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
        supplier = suppliers.get(item.get("supplier_id"))
        if supplier is None:
            print(f"Skipping {item.get('id', '?')}: unknown supplier '{item.get('supplier_id')}'.")
            continue

        try:
            product = ProductFactory.create(
                item.get("type", ""), item["id"], item["name"], item["price"],
                item["stock"], supplier,
                weight=item.get("weight", 0.0),
                download_size=item.get("download_size", 0.0),
            )
        except (ValueError, KeyError) as error:
            print(f"Skipping {item.get('id', '?')}: {error}")
            continue

        inventory.add_product(product)

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