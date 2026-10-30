import os
import json

from product import Product
from inventory import Inventory

#File handling
# Single responsibility: load and save inventory data.
# Plain functions (no class needed yet; the lab says a file-handling class is optional).

# ---------- File location ----------
# Folder this script lives in
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Docker sets DATA_DIR=/app/data; when running locally, fall back to the "data" folder next to this script
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(SCRIPT_DIR, "data"))

INVENTORY_FILE = os.path.join(DATA_DIR, "inventory.json")


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

    # Turn each dictionary back into a Product object and add it to the inventory
    for item in data:
        inventory.add_product(Product.from_dict(item))

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    """Write every product in the given Inventory to inventory.json."""
    print("Saving inventory...")

    # Create the data folder if it doesn't exist yet (exist_ok=True means no error if it does)
    os.makedirs(DATA_DIR, exist_ok=True)

    # Turn each Product object into a dictionary, because JSON can't store objects directly
    data = [product.to_dict() for product in inventory.get_all_products()]

    with open(INVENTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)  # indent=4 makes the file readable

    print("Inventory saved successfully to inventory.json.")


# ---------- Quick test ----------
# Only runs when this file is executed directly (python file_handler.py)
if __name__ == "__main__":
    print("Reading from:", INVENTORY_FILE)

    # Load the existing JSON file into Product objects and show them
    inventory = load_inventory()
    inventory.display_all()

    # Save it straight back. the file content should come out identical
    save_inventory(inventory)