from pathlib import Path

orders_file_path = Path("orders.txt")


def load_inventory():
    orders = []
    if not orders_file_path.is_file():
        return orders

    with open(orders_file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",")
                if len(parts) == 3:
                    order_id = int(parts[0].strip())
                    name = parts[1].strip()
                    qty = int(parts[2].strip())
                    orders.append((order_id, name, qty))

    return orders
