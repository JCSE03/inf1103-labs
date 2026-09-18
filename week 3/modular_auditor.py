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


inventory = 0
failed_entries = 0 

while True:
    val = get_valid_inputs()

    if val == "quit":
        break

    inventory = process_delivery(inventory, val)

    if inventory > 500:
        print("OVERSTOCK ALERT: Total inventory of " + str(inventory) + " exceeds limit of 500 units!")
        break


print("Total Units Processed: " + str(inventory))
print("Number of Failed/Rejected Entries: "  +str(failed_entries))