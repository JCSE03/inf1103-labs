def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
            continue

        if value <= 0:
            print("Please enter a number greater than zero.")
            continue

        return value


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a whole number, e.g. 10")
            continue

        if value < 0:
            print("Please enter a number that is 0 or more.")
            continue

        return value