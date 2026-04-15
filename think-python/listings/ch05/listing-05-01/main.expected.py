def main():
    # Integer division and modulus
    minutes = 105
    hours = minutes // 60
    print(f"Minutes: {minutes}")
    print(f"Hours: {hours}")
    print()

    # Remainder via subtraction
    remainder = minutes - hours * 60
    print(f"Remainder (subtraction): {remainder}")

    # Remainder via modulus operator
    remainder2 = minutes % 60
    print(f"Remainder (modulus): {remainder2}")
    print()

    # Extract rightmost digits
    x = 123
    print(f"x = {x}")
    print(f"x % 10 = {x % 10}")
    print(f"x % 100 = {x % 100}")
    print()

    # Clock arithmetic
    start = 11
    duration = 3
    end = (start + duration) % 12
    print(f"Start: {start} AM")
    print(f"Duration: {duration} hours")
    print(f"End: {12 if end == 0 else end} PM")

    # Divisibility check
    y = 15
    print()
    print(f"Is {y} divisible by 3? {y % 3 == 0}")
    print(f"Is {y} divisible by 4? {y % 4 == 0}")


if __name__ == "__main__":
    main()
