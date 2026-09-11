inventory = 0

while True:
    userInput = input("Enter a stock quantity: (or type 'quit' to quit)")

    if userInput == "quit":
        break

    elif userInput.startswith("-") and userInput[1:].isdigit():
        print("Error: Negative numbers are not allowed.")

    elif userInput.isdigit():
        inventory += int(userInput)

        if inventory > 500:
            print("OVERSTOCK ALERT: Total inventory of "  + str(inventory) + " exceeds limit of 500 units!")
            break

    else:
        print("Error: Invalid entry. Please enter a valid number.")