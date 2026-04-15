def is_between(x, y, z):
    return (x < y and y < z) or (z < y and y < x)


def is_power(a, b):
    if a == 1:
        return True
    if a % b == 0:
        return is_power(a // b, b)
    return False


def main():
    # Testing is_between
    print(f"is_between(1, 2, 3): {is_between(1, 2, 3)}")
    print(f"is_between(3, 2, 1): {is_between(3, 2, 1)}")
    print(f"is_between(1, 3, 2): {is_between(1, 3, 2)}")
    print(f"is_between(2, 3, 1): {is_between(2, 3, 1)}")

    # Testing is_power
    print(f"is_power(65536, 2): {is_power(65536, 2)}")
    print(f"is_power(27, 3): {is_power(27, 3)}")
    print(f"is_power(24, 2): {is_power(24, 2)}")
    print(f"is_power(1, 17): {is_power(1, 17)}")


if __name__ == "__main__":
    main()
