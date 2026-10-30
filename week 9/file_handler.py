import os
import json

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

# File handling
# Single responsibility: load and save inventory data.
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


def load_inventory():
    """Read inventory.json and return a filled Inventory object.

    If the file doesn't exist yet, return an empty Inventory instead.
    """
    inventory = Inventory()  # start empty, then fill it from the file

    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    print("inventory.json found.")
    with open(INVENTORY_FILE, "r") as f:
        data = json.load(f)  # JSON file -> Python list of dictionaries

    for item in data:
        # Use the saved type label to pick the right subclass
        product_class = PRODUCT_TYPES.get(item.get("type"))

        # Skip anything we don't recognise rather than crashing the whole load
        if product_class is None:
            print(f"Skipping {item.get('id', '?')}: unknown product type '{item.get('type')}'.")
            continue

        inventory.add_product(product_class.from_dict(item))

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Write every product in the given Inventory to inventory.json."""
    print("Saving inventory...")

    # Create the data folder if it doesn't exist yet (exist_ok=True means no error if it does)
    os.makedirs(DATA_DIR, exist_ok=True)

    # Each product converts itself, so the subclass's to_dict() adds its own type and extra field
    data = [product.to_dict() for product in inventory.get_all_products()]

    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)  # indent=4 makes the file readable

    print("Inventory saved successfully to inventory.json.")


# ---------- Quick test ----------
# Only runs when this file is executed directly (python file_handler.py)
if __name__ == "__main__":
    print("Reading from:", INVENTORY_FILE)

    # Load the JSON file into the correct product subclasses and show them
    inventory = load_inventory()
    inventory.display_all()

    # Save it straight back; the file content should come out identical
    save_inventory(inventory)