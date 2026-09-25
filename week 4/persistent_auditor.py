from pathlib import Path

orders_file_path = Path(__file__).resolve().parent / "inventory.txt"


def load_inventory():
    orders = []
    if not orders_file_path.is_file():
        return orders

    with open(orders_file_path, "r", encoding="utf-8") as file:
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

def save_inventory(orders):
    orders_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(orders_file_path, "w", encoding="utf-8") as file:
        for order_id, name, qty in orders:
            file.write(f"{order_id},{name},{qty}\n")


def display_orders(orders):
    print("Current Orders:\n")
    if not orders:
        print("(No orders found)\n")
    else:
        for order_id, name, qty in orders:
            print(f"{order_id}, {name}, {qty}")
        print()

orders = load_inventory()
display_orders(orders)

while True:
    product_name = input("Enter Product Name (or 'quit' to exit): ").strip()
    
    if product_name.lower() == "quit":
        break

    quantity = input("Enter Quantity: ").strip()

    if quantity.isdigit():
        quantity = int(quantity)

        next_id = orders[-1][0] + 1 if orders else 1001

        new_order = (next_id, product_name, quantity)
        orders.append(new_order)

        print("\nNew Order Added:")
        print(f"{next_id},{product_name},{quantity}\n")

        save_inventory(orders)
        print(f"Order successfully saved to {orders_file_path.name}\n")
    else:
        print("Error: Quantity must be a valid number.\n")