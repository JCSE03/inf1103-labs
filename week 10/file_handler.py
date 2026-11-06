import os
import json

from inventory import Inventory
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# File handling
# Single responsibility: load and save inventory data (products AND the suppliers they point to).
# Plain functions (no class needed yet; the lab says a file-handling class is optional).

# ---------- File location ----------
# Folder this script lives in
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Docker sets DATA_DIR=/app/data; when running locally, fall back to the "data" folder next to this script
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(SCRIPT_DIR, "data"))

INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")

# ---------- Product types ----------
# Maps the "type" label stored in JSON to the class that should be rebuilt.
# Using a lookup table instead of an if/elif chain means a new product type
# only needs one extra line here.
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
    inventory = Inventory()  # start empty, then fill it from the file
    suppliers: dict[str, Supplier] = {}

    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory, suppliers

    print("inventory.json found.")
    with open(INVENTORY_FILE, "r") as f:
        data = json.load(f)  # JSON file -> Python dictionary with "suppliers" and "products" lists

    # Step 1: rebuild every supplier once and file it under its ID
    for supplier_data in data.get("suppliers", []):
        supplier = Supplier.from_dict(supplier_data)
        suppliers[supplier.supplier_id] = supplier

    # Step 2: rebuild each product and connect it to its supplier
    for item in data.get("products", []):
        # Use the saved type label to pick the right subclass
        product_class = PRODUCT_TYPES.get(item.get("type"))

        # Skip anything we don't recognise rather than crashing the whole load
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

    # Create the data folder if it doesn't exist yet (exist_ok=True means no error if it does)
    os.makedirs(DATA_DIR, exist_ok=True)

    data = {
        "suppliers": [supplier.to_dict() for supplier in suppliers.values()],
        "products": [product.to_dict() for product in inventory.get_all_products()],
    }

    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)  # indent=4 makes the file readable

    print("Inventory saved successfully to inventory.json.")