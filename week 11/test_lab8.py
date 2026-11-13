
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def section(title: str) -> None:
    """Print a clear heading so each test is easy to find in the output."""
    print(title)


section("2.2 ASSOCIATION: Supplier and Product")

supplier = Supplier("S001", "Tech Distributors", "sales@techdistributors.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.2)
ebook = DigitalProduct("D001", "Python E-book", 29.90, 50, supplier, 12.5)

print("Laptop's supplier:")
laptop.supplier.display_information()
print("E-book's supplier:")
ebook.supplier.display_information()


print("\nSupplier and products are separate objects:", supplier is not laptop and supplier is not ebook)
print("Both products share one Supplier object:", laptop.supplier is ebook.supplier)


del supplier  
print("\nAfter `del supplier`, the laptop can still show its supplier:")
laptop.supplier.display_information()


section("3.2 AGGREGATION: Inventory and Product")

mouse = PhysicalProduct("P002", "Mouse", 25.50, 60, laptop.supplier, 0.1)
inventory_a = Inventory()
inventory_b = Inventory()


print("Added to Inventory A:", inventory_a.add_product(mouse))

removed = inventory_a.remove_product("P002")
print("Removed from Inventory A, still in A?", inventory_a.find_product("P002") is not None)
print("Removed product still usable:")
removed.display_information()

print("\nAdded to Inventory B:", inventory_b.add_product(removed))
print("Inventory B holds the same object as before:", inventory_b.find_product("P002") is mouse)

inventory_b.remove_product("P002")
print("\nInventory B emptied:")
inventory_b.display_all()
print("Mouse object still exists:", mouse.name, "| stock:", mouse.stock)


section("4.3 COMPOSITION: Order and OrderLine")

order_1 = Order("O001")
order_1.add_order_line(laptop, 2)  
order_1.add_order_line(ebook, 3)  
order_1.add_order_line(mouse, 1)  
order_1.display_information()

order_2 = Order("O002")
order_2.add_order_line(laptop, 1)

line_in_order_1 = order_1.order_lines[0] 
line_in_order_2 = order_2.order_lines[0]  

print("\nSame laptop added to Order O001 and Order O002:")
print("Same OrderLine object?", line_in_order_1 is line_in_order_2)
print("Same Product object?  ", line_in_order_1.product is line_in_order_2.product)
print(f"OrderLine ids: {id(line_in_order_1)} vs {id(line_in_order_2)}")
print(f"Product ids:   {id(line_in_order_1.product)} vs {id(line_in_order_2.product)}")

print("\nRemoving the e-book line from O001:", order_1.remove_order_line("D001"))
order_1.display_information()
print("E-book product still exists:", ebook.name)


del order_2
print("\nAfter `del order_2`, its line is gone with it, but the laptop remains:", laptop.name)


section("6.2 LSP: any Product can stand in for Product")


def show_product_details(product: Product) -> None:
    """Uses only behaviour that EVERY Product promises, so any subclass must work here."""
    product.display_information()
    print(product.get_fulfilment_info())


show_product_details(laptop)
print()
show_product_details(ebook)

print("\nupdate_stock() behaves the same for both product types:")
for product in (laptop, ebook):
    original_stock = product.stock 
    product.update_stock(0)
    try:
        product.update_stock(-5)
    except ValueError as error:
        print(f"{product.product_id}: stock set to {product.stock}, -5 rejected ({error})")
    product.update_stock(original_stock)



section("7.2 POLYMORPHISM: one loop, no isinstance()")

shop = Inventory()
shop.add_product(laptop)
shop.add_product(ebook)
shop.add_product(mouse)

for product in shop.get_all_products():
    product.display_information()
    print("Fulfilment:", product.get_fulfilment_info())
    print()

print("All Lab 8 demonstrations finished.")