inventory = 0

while True:
    userInput = input("Enter a stock quantity: (or type 'quit' to quit)")

    if userInput == "quit":
        break

    else:
        if userInput.isdigit():
            inventory = int(userInput)