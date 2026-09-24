from pathlib import Path

inventory_file_path = Path("inventory.txt")

def load_inventory():
    if not inventory_file_path.isfile():
        return 0, []

    inventory = 0
    history = []

    with open(inventory_file_path, "r") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

        if lines:
            inventory = int(lines[0])
            history = [int(val) for val in lines[1:]]

    return inventory, history

def save_inventory(inventory, history):
    with open(inventory_file_path, "w") as file:
        file.write(f"{inventory}\n")

        for item in history:
            file.write(f"{item}\n")

    print("Inventory data sucessfully saved to inventory.txt")

def get_valid_inputs():
    global failed_entries
    while True:
        userInput = input("Enter a stock quantity: (or type 'quit' to quit)")
        if userInput == "quit":
            return "quit"
        
        elif userInput.startswith("-") and userInput[1:].isdigit():
            print("Error: Negative numbers are not allowed.")
            failed_entries += 1

        elif userInput.isdigit():
            return int(userInput)
        
        else:
            print("Error: Invalid entry. Please enter a valid number.")
            failed_entries += 1

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print("Total Deliveries Processed: " + str(total_units))
    print("Number of Failed/Rejected Entries: " + str(failed_attempts))



inventory = 0
failed_entries = 0 

while True:
    val = get_valid_inputs()

    if val == "quit":
        break

    tax = calculate_tax(val)
    print("Tax for this delivery (10%): " + str(tax))
     
    inventory = process_delivery(inventory, val)

    if inventory > 500:
        print("OVERSTOCK ALERT: Total inventory of " + str(inventory) + " exceeds limit of 500 units!")
        break

generate_report(inventory, failed_entries)


