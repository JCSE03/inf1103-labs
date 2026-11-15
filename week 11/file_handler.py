import os
import csv
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
    If the file is missing or damaged, return an empty Inventory and no suppliers.
    """
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    try:
        with open(INVENTORY_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory, suppliers
    except json.JSONDecodeError:
        backup_file = INVENTORY_FILE + ".damaged"
        os.replace(INVENTORY_FILE, backup_file)
        print(f"inventory.json is damaged and could not be read. It was moved to {backup_file}.")
        print("Starting with an empty inventory.")
        return inventory, suppliers

    print("inventory.json found.")

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


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> int:
    """Load products from a CSV file through the ProductFactory and add them to the inventory.

    Bad rows are reported and skipped, a missing file is reported without crashing,
    and the number of products loaded is returned.
    """
    loaded = 0

    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)

            for line_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id, name, float(price), int(stock), supplier
                    )
                except ValueError as error:
                    print(f"Row {line_number} skipped ({error}): {row}")
                    continue

                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Row {line_number} skipped (duplicate product ID {product.product_id}): {row}")

        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")

    return loaded