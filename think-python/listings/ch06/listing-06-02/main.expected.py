import math

def is_divisible(x, y):
    return x % y == 0


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dsquared = dx ** 2 + dy ** 2
    result = math.sqrt(dsquared)
    return result


def main():
    # Step 1: Start with a stub that always returns 0
    # Step 2: Add dx, dy computation
    # Step 3: Add dsquared computation
    # Step 4: Use sqrt and return result

    d = distance(1, 2, 4, 6)
    print(f"distance(1, 2, 4, 6) = {d}")

    # Boolean function in a conditional
    if is_divisible(6, 2):
        print("6 is divisible by 2")

    if is_divisible(6, 4):
        print("6 is divisible by 4")
    else:
        print("6 is NOT divisible by 4")


if __name__ == "__main__":
    main()
